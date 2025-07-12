+++
title = "Setting Up DHCP"
date = "2025-07-09"
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
# Enable forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Allow traffic from both test subnets
iptables -A FORWARD -i enp3s0f0 -o enp4s0 -j ACCEPT
iptables -A FORWARD -i enp3s0f1 -o enp4s0 -j ACCEPT

# NAT out through production LAN
iptables -t nat -A POSTROUTING -o enp4s0 -j MASQUERADE
```

Now everything Just Works™.

---

## **🧠 Anki Flashcards**

Here are 25 cards formatted for Anki, covering the essentials:

---

START

Basic

TARGET DECK: Linux Lab Router Setup

What command enables IP forwarding on Linux?

Back: echo 1 > /proc/sys/net/ipv4/ip_forward

Tags: linux routing

<!--ID: 1745614900044-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What iptables rule enables NAT on Ubuntu to the external network?

Back: iptables -t nat -A POSTROUTING -o enp4s0 -j MASQUERADE

Tags: nat iptables

<!--ID: 1745614900047-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What are the three subnets in the test lab setup?

Back: 192.168.178.0/24 (production), 192.168.0.0/24 (lab1), 10.0.0.0/24 (lab2)

Tags: subnet lab

<!--ID: 1745614900048-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

Why was rfc3442-classless-static-routes problematic in this setup?

Back: FreeBSD’s dhclient couldn’t parse it correctly, causing lease errors.

Tags: dhcp freebsd

<!--ID: 1745614900049-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What is the role of option routers in DHCP configuration?

Back: It provides the default gateway to clients.

Tags: dhcp routing

<!--ID: 1745614900050-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What DHCP server was used on the Ubuntu router?

Back: isc-dhcp-server

Tags: dhcp ubuntu

<!--ID: 1745614900051-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What Linux command installs isc-dhcp-server?

Back: sudo apt install isc-dhcp-server

Tags: dhcp install

<!--ID: 1745614900052-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

How many interfaces did rtr02 have?

Back: Three — enp4s0 (WAN), enp3s0f0 (lab2), enp3s0f1 (lab1)

Tags: router interfaces

<!--ID: 1745614900053-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What file contains DHCP subnet configurations?

Back: /etc/dhcp/dhcpd.conf

Tags: dhcp config

<!--ID: 1745614900054-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What error did FreeBSD show when parsing classless routes?

Back: incorrect subnet with ; 168

Tags: freebsd error

<!--ID: 1745614900055-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

How was this error solved: “incorrect subnet with ; 168”?

Back: By removing rfc3442-classless-static-routes and using only option routers.

Tags: troubleshooting freebsd

<!--ID: 1745614900056-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

Why is NAT required in this setup?

Back: To allow private lab subnets to access the internet via the production LAN.

Tags: nat internet

<!--ID: 1745614900057-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

How were hosts in different lab subnets able to communicate?

Back: They routed traffic through rtr02, which had routes for both subnets.

Tags: routing lab

<!--ID: 1745614900058-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What interface did the FreeBSD host connect to?

Back: enp3s0f0, on subnet 10.0.0.0/24

Tags: freebsd subnet

<!--ID: 1745614900059-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What interface did the NixOS laptop connect to?

Back: enp3s0f1, on subnet 192.168.0.0/24

Tags: nixos subnet

<!--ID: 1745614900060-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What range of IPs was assigned in the 192.168.0.0/24 subnet?

Back: 192.168.0.100 to 192.168.0.200

Tags: dhcp range

<!--ID: 1745614900061-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What is the primary advantage of using only a default gateway for routing?

Back: Simpler configuration and better cross-platform compatibility

Tags: networking routing

<!--ID: 1745614900062-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What was the reason for removing rfc3442-classless-static-routes?

Back: Compatibility issues and errors on FreeBSD’s DHCP client

Tags: dhcp workaround

<!--ID: 1745614900063-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What is the default lease time set in dhcpd.conf?

Back: 600 seconds

Tags: dhcp lease

<!--ID: 1745614900064-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What command restarts the DHCP service on Ubuntu?

Back: sudo systemctl restart isc-dhcp-server

Tags: dhcp service

<!--ID: 1745614900065-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

How do you verify DHCP leases on Ubuntu?

Back: Check /var/lib/dhcp/dhcpd.leases

Tags: dhcp verify

<!--ID: 1745614900066-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

How does the router know how to route between lab subnets?

Back: It has interfaces in both subnets and IP forwarding enabled.

Tags: router forwarding

<!--ID: 1745614900067-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

Why don’t the lab clients need to know routes to other subnets?

Back: Because their default route points to the router which handles it.

Tags: dhcp simplicity

<!--ID: 1745614900068-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

How can you make IP forwarding permanent on Ubuntu?

Back: Add net.ipv4.ip_forward=1 to /etc/sysctl.conf

Tags: sysctl forwarding

<!--ID: 1745614900069-->

END

START

Basic

TARGET DECK: Linux Lab Router Setup

What system is used to assign IPs dynamically to clients?

Back: DHCP

Tags: dhcp basics

<!--ID: 1745614900070-->

END

---

Want me to format this for import into an actual .apkg file or help you upload it into AnkiWeb?
