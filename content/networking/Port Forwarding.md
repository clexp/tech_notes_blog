+++
title = "Port Forwarding"
date = "2025-07-09"
draft = true
description = "When setting up my home lab, one of my goals was to be able to SSH into a FreeBSD test machine (tb02) on a private subnet, even though it’s not directly reachable from my main production network. To d..."
tags = ['bsd', 'firewall', 'freebsd', 'iptables', 'linux', 'nat', 'networking', 'security', 'ssh', 'ubuntu', 'unix']
categories = ["technical"]
+++

## **🔧 Port Forwarding vs Masquerading: Routing SSH into My FreeBSD Lab Box**

When setting up my home lab, one of my goals was to be able to SSH into a FreeBSD test machine (tb02) on a private subnet, even though it’s not directly reachable from my main production network. To do this, I had already built a custom Linux router (rtr02) that connects the production LAN to two test subnets: 192.168.0.0/24 and 10.0.0.0/24.

I had already set up NAT so that the FreeBSD box could _initiate_ outbound connections and reach the internet. But now, I wanted to _receive_ an SSH connection from my main network and forward it into the lab. That’s where **port forwarding** (a.k.a. DNAT) came into play.

---

### **🧭 My Network Context**

- rtr02 (Ubuntu router):
  - enp4s0: 192.168.178.80 (Production LAN)
  - enp3s0f0: 10.0.0.1 (Test LAN A)
  - enp3s0f1: 192.168.0.1 (Test LAN B)
- tb02 (FreeBSD test machine): 10.0.0.50
- Goal: SSH from any machine in 192.168.178.0/24 (e.g. 192.168.178.10) into tb02

---

## **🔀 Understanding NAT: Masquerading vs Port Forwarding**

These are both forms of **Network Address Translation (NAT)**, but they serve different purposes.

### **✅ Masquerading (SNAT)**

- Happens when a machine in a private subnet initiates a connection to the internet.
- The router **replaces the source IP** with its public IP (e.g. 192.168.178.80), so that reply packets come back correctly.
- This is called **Source NAT** (SNAT).

### **✅ Port Forwarding (DNAT)**

- Happens when a machine on the outside initiates a connection **to** a private address.
- The router **redirects a destination port** to a host on an internal network.
- This is called **Destination NAT** (DNAT).
- Example: traffic to rtr02:2222 → goes to tb02:22

---

## **🧪 The Actual Rules**

Here are the iptables rules I added to rtr02:

```
sudo iptables -t nat -A PREROUTING -p tcp -i enp4s0 --dport 2222 -j DNAT --to-destination 10.0.0.50:22
sudo iptables -A FORWARD -p tcp -d 10.0.0.50 --dport 22 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
```

### **🔍 What they mean in plain English**

1. **PREROUTING Rule (DNAT):**

   > “If a packet comes in on enp4s0 (production LAN), using TCP, and targeting port 2222, then redirect it to 10.0.0.50:22.”

2. **FORWARD Rule (Allow Forwarding):**

   > “If a forwarded TCP packet is going to 10.0.0.50 on port 22, and is part of a new or established connection, allow it.”

### **❗ Why do we need both?**

- **PREROUTING** handles the _translation_.
- **FORWARD** handles the _permission_.
- Without the FORWARD rule, the packet would be dropped even if translated correctly.

---

## **🧩 Questions and Clarifications**

### **🤔 Why PREROUTING?**

PREROUTING is used for DNAT because it rewrites the destination address **before** routing decisions are made.

### **🤔 What about replies?**

The connection tracking in iptables (via ESTABLISHED,RELATED) takes care of return packets.

### **🤔 Will this interfere with my own SSH into rtr02?**

Not unless you also use port 2222 to connect to the router. I SSH into rtr02 using port 22, so there’s no conflict.

---

## **💾 Saving the Rule for Reboot**

To make the rules persistent:

```
sudo apt install iptables-persistent
sudo iptables-save | sudo tee /etc/iptables/rules.v4 > /dev/null
```

---

## **🏁 Result: Seamless SSH Access**

I can now do this from any machine on my production LAN:

```
ssh -p 2222 user@192.168.178.80
```

And I land on the FreeBSD box tb02 at 10.0.0.50.

No need to mess with the FreeBSD console anymore 🎉
