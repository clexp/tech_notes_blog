+++
title = "How I Built a VLAN-Aware Linux Router with DHCP, NAT, and a Touch of Fire"
date = "2025-07-09"
description = "A practical guide to building a professional-grade VLAN setup at home using Ubuntu Server, ISC DHCP, and iptables. Learn network segmentation, troubleshooting methodology, and real-world networking concepts."
tags = ['bsd', 'debugging', 'dhcp', 'dns', 'firewall', 'freebsd', 'iptables', 'linux', 'nat', 'networking', 'nixos', 'security', 'troubleshooting', 'tutorial', 'ubuntu', 'unix', 'vlan']
categories = ["technical"]
+++

_April 2025_

---

## 🛠️ Project Goal

I wanted a real lab setup at home, the kind you'd see in small businesses:

- VLANs for network segmentation
- DHCP on each VLAN
- NAT routing to the internet
- A real firewall
- Real troubleshooting All running on **Ubuntu Server 24.04** with **netplan**, **iptables**, and **ISC DHCP Server**.

---

## 🧬 The Setup

**Router (router):**

- Ubuntu Server 24.04
- Three NICs:
  - `enp4s0` (production LAN, 192.168.1.x network)
  - `enp3s0f0` (test network 10.10.0.x)
  - `enp3s0f1` (for VLANs!)

**Switch:**

- Netgear GS305E (VLAN-capable, web management)

**Clients:**

- FreeBSD box
- NixOS laptop

---

## 📋 Step 1: Setting Up Static IPs and VLANs in Netplan

At first, only flat networks. But then I needed VLANs. Here's the working `/etc/netplan/40-static-ip.yaml`:

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp3s0f0:
      dhcp4: no
      addresses:
        - 10.10.0.1/24
    enp3s0f1:
      dhcp4: no
      addresses: []
  vlans:
    vlan1:
      id: 1
      link: enp3s0f1
      addresses: [192.168.1.1/24]
    vlan2:
      id: 2
      link: enp3s0f1
      addresses: [192.168.2.1/24]
    vlan3:
      id: 3
      link: enp3s0f1
      addresses: [192.168.3.1/24]
    vlan4:
      id: 4
      link: enp3s0f1
      addresses: [192.168.4.1/24]
    vlan99:
      id: 99
      link: enp3s0f1
      addresses: [192.168.99.1/24]
```

**Key point:**

- `enp3s0f1` becomes a _parent interface_. It **does not** get an IP itself.
- VLAN interfaces (`vlan1`, `vlan2`, etc.) each have their own IPs.

**Troubleshooting Tip:** Always `sudo netplan apply` after changes — and check `ip a` to confirm new interfaces appear.

---

## 📋 Step 2: Configuring ISC DHCP Server for Multiple VLANs

My `/etc/default/isc-dhcp-server` needed this:

```bash
INTERFACESv4="enp3s0f0 enp3s0f1 vlan1 vlan2 vlan3 vlan4 vlan99"
```

**Important:** Even though `enp3s0f1` doesn't have an IP, it still needs to be listed! DHCP listens at Layer 2.

In `/etc/dhcp/dhcpd.conf`, I added:

```bash
option domain-name-servers 192.168.1.52;
```

(Yes, that's a _global option_. Needed for DNS to work properly on clients later.)

And subnet declarations for each VLAN, for example:

```bash
subnet 192.168.2.0 netmask 255.255.255.0 {
  range 192.168.2.100 192.168.2.200;
  option routers 192.168.2.1;
}
```

---

## 🐛 Snag #1: Clients Couldn't Resolve DNS

Even after getting an IP, my NixOS laptop had `/etc/resolv.conf` looking empty except for:

```
options edns0
```

No DNS servers = no browsing. 💀

**The fix:** Setting the global `option domain-name-servers` in `dhcpd.conf`, then:

```bash
sudo systemctl restart isc-dhcp-server
nmcli con down production-dhcp
nmcli con up production-dhcp
```

**Result:** `/etc/resolv.conf` now showed `nameserver 192.168.1.52` and browsing worked.

---

## 🔍 Tools I Used to Troubleshoot

| Tool                                  | Purpose                                      |
| :------------------------------------ | :------------------------------------------- |
| `tcpdump -i vlan2 port 67 or port 68` | Watching DHCP traffic directly               |
| `ip a`                                | Checking if VLANs were up and assigned       |
| `iptables -L INPUT -v -n              | grep icmp`                                   |
| `nmcli`                               | Managing NetworkManager connections on NixOS |
| `ping`, `dig`, `nslookup`             | Testing reachability and DNS                 |

**Tcpdump** showed me that requests were arriving and replies were being sent — super valuable!

---

## 📋 Step 3: Firewall (iptables) - Only Allow What's Needed

I kept a **default DROP** policy, but allowed:

```bash
iptables -A INPUT -i enp3s0f0 -p icmp --icmp-type 8 -j ACCEPT
iptables -A INPUT -i enp3s0f1 -p icmp --icmp-type 8 -j ACCEPT
```

**Key thing:**

- ICMP (ping) is useful for troubleshooting, but that's it.
- No unnecessary open ports!

I didn't modify FORWARD chain yet — clients can ping out because of established NAT rules.

---

## 🐛 Snag #2: Can't Ping the Router from VLAN Clients?

At first, from 192.168.2.100 (laptop), I couldn't ping 192.168.2.1.

It made me suspicious, but remember:

- Router firewall might block pings
- Not all VLAN traffic is switched the same
- It's _OK_ if clients can't ping 192.168.1.1 or 192.168.0.1 — **segmentation is the point!**

---

## ✅ Final Result

✔️ VLAN separation working  
✔️ DHCP giving correct IPs + DNS  
✔️ Internet access from VLANs  
✔️ Firewall under control  
✔️ Tools ready for future debugging

---

## 🧠 Lessons Learned

- Always trust **tcpdump** over assumptions.
- VLAN tagging works even with dumb switches, if they're **802.1Q aware**.
- DHCP needs **global DNS** settings if you want clients to surf the web without manual config.
- Small, focused firewall rules = good security hygiene even in a lab.
- Netplan, once you get used to it, is actually clean and powerful!

---

## What I Learned

This project taught me the importance of **methodical troubleshooting**. I initially thought VLANs would be plug-and-play, but the reality required understanding Layer 2 vs Layer 3 concepts. The key insight was learning to trust packet-level tools like `tcpdump` over assumptions about what "should" work.

I also learned that **RFC 2131** (DHCP specification) becomes much more relevant when you're configuring multiple subnets. Understanding how DHCP discover/offer/request/ack flows work helped me debug the DNS issue that seemed unrelated at first.

**Next time I would**: Set up VLAN monitoring from the start. While I can see traffic in `tcpdump`, having proper logging and alerting would help me catch configuration issues much earlier.

---

## Security Considerations

While VLANs provide network segmentation, I'm aware that they're not a complete security solution. I've configured basic firewall rules to restrict inter-VLAN traffic, but proper production deployments would need more comprehensive access controls and monitoring.

---

## 📡 What's Next?

I'm planning to:

- Add inter-VLAN routing (maybe selectively)
- Build captive portal for guest VLAN
- Maybe OSPF dynamic routing between routers?

Stay tuned. 😎

---

> **Note**: This post documents a lab environment setup. Real production networks should use different IP ranges and follow your organization's security policies.
