**Title:** From Tailscale to Printer: A Journey Through Subnet Routing on Ubuntu

**Subtitle:** Adventures in Remote Access, IP Forwarding, and Getting the Family Scanner to Behave

---

Sometimes, all you want to do is scan a document. But in the age of VLANs, containers, and zero-trust networks, that can turn into a bit of a puzzle. This is the story of how we got remote access to a network printer on a LAN behind an Ubuntu NAS, using Tailscale as our digital sherpa. Along the way, we learned a lot about how subnet routing works, how to wrangle Linux networking, and how to use troubleshooting tools effectively.

### The Goal: Remote Access to a LAN Printer

Our target was simple: access a network printer at `192.168.178.11` from a remote laptop, connected via Tailscale. The printer was reachable locally but invisible to Tailscale-connected devices.

We already had Tailscale running on a server (`nas04`) at `192.168.178.52`, and we could SSH into it via its Tailscale IP `100.87.99.119`. So, we needed to turn `nas04` into a subnet router that could relay traffic from Tailscale clients to LAN devices.

### The Network Landscape

`nas04` runs Ubuntu and is connected to the LAN via a bridged interface `br0`, with a static IP of `192.168.178.52`. It also runs containers and has Docker bridges, but our focus was on routing traffic from the `tailscale0` interface to the LAN via `br0`.

### Step 1: Installing and Confirming Tailscale

We began by ensuring `tailscale` was installed and working on `nas04`:

```bash
sudo tailscale status
```

This confirmed that `nas04` was connected, and its Tailscale IP was visible. A good start.

### Step 2: Enabling Subnet Routing

We ran:

```bash
sudo tailscale up --advertise-routes=192.168.178.0/24
```

This told Tailscale to advertise the local subnet to the rest of the network. The result was a prompt to approve the route in the admin panel.

> **Admin Console Tip:** Go to [https://login.tailscale.com/admin/machines](https://login.tailscale.com/admin/machines), find the device, and click “Approve” next to the advertised route.

### Step 3: Nothing Works Yet

Despite the route being approved, remote clients still couldn't reach the printer. We tried pinging `192.168.178.11` from a remote laptop on Tailscale, but no response.

Time to troubleshoot.

### Step 4: IP Forwarding

Our first theory: the Linux server wasn’t forwarding packets between `tailscale0` and `br0`. We checked:

```bash
cat /proc/sys/net/ipv4/ip_forward
```

It returned `0`. Bingo.

To enable it:

```bash
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

This change made IP forwarding persistent and immediately effective.

### Step 5: Firewall Rules

Still no luck. The next theory: the firewall was blocking routed traffic. We use UFW, so we needed to allow Tailscale to forward packets.

```bash
sudo ufw allow in on tailscale0
sudo ufw allow from 100.0.0.0/8
sudo ufw route allow in on tailscale0 out on br0
```

This explicitly allowed traffic from Tailscale to reach the LAN.

### Step 6: The Moment of Truth

We returned to our remote laptop and ran:

```bash
ping 192.168.178.11
```

Success! A glorious chorus of ICMP replies. Even better, we could load the printer’s web UI in the browser. Remote scanning was now possible.

### Summary of Learnings

- **Tailscale subnet routing** allows clients to access non-Tailscale devices on your LAN.
    
- **IP forwarding** must be enabled to relay traffic.
    
- **Firewall configuration** is essential for allowing routed traffic.
    
- **The Tailscale admin console** is where routes must be approved.
    
- **Troubleshooting tools** like `ping`, `tailscale status`, and `/proc/sys/net/ipv4/ip_forward` are invaluable.
    

### Tools Used

- `tailscale status`: Confirm connection and route advertisement
    
- `ping`: Check host reachability
    
- `ip a`: Show interfaces and IPs
    
- `sysctl -p`: Reload kernel settings
    
- `ufw route allow`: Permit routed traffic
    

### Final Thoughts

This journey was a great reminder that simple goals (like accessing a printer) often require deeper understanding of how the system is wired. It turned into a valuable exploration of Linux routing, firewall behavior, and how Tailscale stitches it all together. Next time the printer stops responding, at least we know where to look first.