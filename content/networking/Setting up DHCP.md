+++
title = "Setting Up DHCP"
date = "2025-07-09"
draft = true
description = "tags: blog_post dhcp flash_cards Absolutely! Below is a blog-style narrative of your setup, including the _why_, the _pain_, and the final _working state_ — plus a complete set of 25 Anki flashcards b..."
tags = ['bsd', 'debugging', 'dhcp', 'dns', 'firewall', 'freebsd', 'iptables', 'linux', 'nat', 'networking', 'nixos', 'security', 'tutorial', 'ubuntu', 'unix']
categories = ["technical"]
+++

tags: #blog*post #dhcp #flash_cards
Absolutely! Below is a blog-style narrative of your setup, including the \_why*, the _pain_, and the final _working state_ — plus a complete set of 25 Anki flashcards based on the setup.

---

## **🧵 Blog Post: Building a Dual-Subnet Lab Router with DHCP and NAT on Ubuntu**

### **🛠️ The Setup**

As part of building a home test lab for experimenting with networking, I created a dual-subnet environment behind a Linux router (rtr02) using Ubuntu Server 24.04. The router connects to:

- The **production LAN** (192.168.178.0/24) via enp4s0
- **Test Lab 1** (192.168.0.0/24) via enp3s0f1
- **Test Lab 2** (10.0.0.0/24) via enp3s0f0

The lab hosts included:

- A NixOS laptop in 192.168.0.0/24
- A FreeBSD box (tb02) in 10.0.0.0/24

My goal was:

- Enable DHCP on the router for both subnets
- Provide NAT to allow internet access from both lab subnets
- Allow lab hosts to ping each other and the outside world

### **🧱 DHCP Configuration**

I used isc-dhcp-server on Ubuntu (rtr02) with the following key sections:

```
subnet 192.168.0.0 netmask 255.255.255.0 {
  range 192.168.0.100 192.168.0.200;
  option routers 192.168.0.1;
  option domain-name-servers 192.168.178.52;
}

subnet 10.0.0.0 netmask 255.255.255.0 {
  range 10.0.0.100 10.0.0.50;
  option routers 10.0.0.1;
  option domain-name-servers 192.168.178.52;
}
```

These provided IPs, default gateways, and DNS to lab clients.

### **🔥 The Trouble**

Initially, I tried using the RFC3442 classless static routes option like this:

```
option rfc3442-classless-static-routes 0,0,0,0,192,168,0,1, 24,10,0,0,192,168,0,1;
```

But this led to:

- **Syntax errors** on FreeBSD’s dhclient.conf
- **Invalid lease parsing**: “incorrect subnet with ; 168”
- **No routes added**, or default route missing
- **Inconsistent behavior across clients**

I realized that FreeBSD’s dhclient didn’t gracefully handle complex RFC3442 arrays like Linux’s does.

### **❌ What Didn’t Work**

- Manually adding route codes in dhclient.conf
- Editing /etc/rc.conf to hard-code routes
- Using both option routers and rfc3442-classless-static-routes together

Every combination led to errors, or inconsistent routes.

### **✅ What Worked**

I simplified:

- Removed all rfc3442-classless-static-routes directives
- Kept only the default gateway (option routers) in each subnet
- Let the router do what routers do: route packets!

Each host was told only to default route via its local router interface. rtr02 already knew how to route between the subnets and NAT to the internet.

💡 This not only worked but aligned better with real-world practices. Most hosts don’t need to know about every subnet—they just need a default route.

### **🧼 Firewall and NAT**

On rtr02, I used iptables to enable forwarding and NAT:

```
## Enable forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

## Allow traffic from both test subnets
iptables -A FORWARD -i enp3s0f0 -o enp4s0 -j ACCEPT
iptables -A FORWARD -i enp3s0f1 -o enp4s0 -j ACCEPT

## NAT out through production LAN
iptables -t nat -A POSTROUTING -o enp4s0 -j MASQUERADE
```

Now everything Just Works™.
