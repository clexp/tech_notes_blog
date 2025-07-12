# Enabling NAT and Routing Between Networks on Ubuntu

This post walks through how to enable routing and NAT on an Ubuntu Server (rtr02) to allow two internal subnets (FreeBSD and NixOS machines) to access the wider internet via the main production LAN.

## 🛠️ Goals

- Enable packet forwarding on Ubuntu.
    
- Configure iptables for NAT (masquerading).
    
- Make changes reboot-proof.
    
- Verify with ping and tcpdump.
    

---

## 1. Kernel IP Forwarding

First, ensure the Ubuntu server is set to forward IP packets:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Make this permanent by editing `/etc/sysctl.conf` or creating a `.conf` in `/etc/sysctl.d/`:

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-ipforward.conf
sudo sysctl --system
```

---

## 2. iptables NAT Rules

If your WAN interface is `enp4s0` and LAN interfaces are `enp3s0f0` (to FreeBSD) and `enp3s0f1` (to NixOS):

```bash
sudo iptables -t nat -A POSTROUTING -o enp4s0 -j MASQUERADE
sudo iptables -A FORWARD -i enp3s0f0 -o enp4s0 -j ACCEPT
sudo iptables -A FORWARD -i enp3s0f1 -o enp4s0 -j ACCEPT
```

### In Plain English:

- **POSTROUTING** (after routing): Change the source IP to rtr02's public IP when packets leave `enp4s0`.
    
- **FORWARD + ACCEPT**: Allow forwarding of packets from each test subnet interface to the external one.
    

---

## 3. Make iptables Rules Persistent

Install and configure persistence:

```bash
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

This saves and reloads rules on reboot.

---

## 4. Validate with tcpdump and ping

From FreeBSD (`10.0.0.2`) and NixOS (`192.168.0.2`), try:

```bash
ping 1.1.1.1
```

On rtr02, use:

```bash
sudo tcpdump -i enp4s0 icmp
```

You should now see traffic flowing and pings succeeding.

---

## ❓FAQ Summary

- **Is forwarding done by both kernel and iptables?** Yes. Kernel (via `ip_forward`) allows routing. iptables allows/controls which packets get through and applies NAT.
    
- **Why is NAT needed?** Because private IPs aren’t routable on the public internet. NAT rewrites source IPs so replies return.
    
- **Did external systems see my internal IPs?** No. Without NAT, replies can't return. NAT makes it look like the packets come from the router.
    
- **Why install `iptables-persistent`?** Ubuntu doesn't save iptables rules by default. This package enables that.
    

---

You've now routed and NAT-ed between subnets and the internet — on three different OSes. 💪

Up next: managing firewall security and logging.