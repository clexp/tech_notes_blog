+++
title = "Setting Up a Firewall on the Router"
date = "2025-07-09"
description = "This is a follow-up to [Part 1: Subnet Routing and DHCP](link-to-part-1), where we set up our Ubuntu Server (rtr02) as a home lab router with DHCP, NAT, and routing between two test subnets. Here, we ..."
tags = ['architecture', 'bsd', 'debugging', 'dhcp', 'dns', 'firewall', 'freebsd', 'iptables', 'linux', 'nat', 'networking', 'nixos', 'security', 'troubleshooting', 'ubuntu', 'unix']
categories = ["technical"]
+++

## Firewall Rules on rtr02: Narrated Walkthrough with iptables and NAT

This is a follow-up to [Part 1: Subnet Routing and DHCP](link-to-part-1), where we set up our Ubuntu Server (rtr02) as a home lab router with DHCP, NAT, and routing between two test subnets. Here, we dive into the firewall configuration using `iptables`, explore chain logic (INPUT, FORWARD, NAT), interpret each rule line-by-line in English, and highlight useful tools for inspection and debugging.

### Context Recap (Short)

- **rtr02** is the Ubuntu router.
- NICs:
  - `enp4s0` — connects to production LAN (`192.168.178.0/24`), IP: `192.168.178.80`
  - `enp3s0f0` — connects to test box tb02 (`10.0.0.0/24`), IP: `10.0.0.1`
  - `enp3s0f1` — connects to NixOS laptop (`192.168.0.0/24`), IP: `192.168.0.1`

We wanted:

- To allow traffic between lab subnets.
- To allow lab clients access to the internet via NAT.
- To secure rtr02 with a default DROP policy.

### iptables Chains Explained

- **INPUT** — for traffic *to* rtr02 itself.
- **FORWARD** — for traffic *through* rtr02, e.g., between subnets or out to the internet.
- **OUTPUT** — for traffic *from* rtr02 itself.
- **NAT POSTROUTING** — for masquerading IP addresses.

### Our iptables Rules (with English Translations)

#### Set Default Policies

```bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT
```

**English:** Drop everything by default except traffic sent by rtr02.

#### Accept Loopback and Established Traffic

```bash
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```

**English:**

- Allow internal system communication (loopback).
- Allow replies to connections rtr02 or a client initiated.

#### Allow DHCP and DNS Requests to rtr02

```bash
iptables -A INPUT -p udp --dport 67:68 --sport 67:68 -j ACCEPT
iptables -A INPUT -p udp --dport 53 -j ACCEPT
iptables -A INPUT -p tcp --dport 53 -j ACCEPT
```

**English:**

- Allow clients to contact rtr02 for DHCP.
- Allow DNS queries to pass if rtr02 is doing local DNS.

#### Allow Pings to rtr02

```bash
iptables -A INPUT -p icmp -j ACCEPT
```

**English:** Allow ping to rtr02 (useful for testing).

#### Allow Forwarding Between Subnets and to Internet

```bash
iptables -A FORWARD -i enp3s0f0 -o enp3s0f1 -j ACCEPT
iptables -A FORWARD -i enp3s0f1 -o enp3s0f0 -j ACCEPT
iptables -A FORWARD -i enp3s0f0 -o enp4s0 -j ACCEPT
iptables -A FORWARD -i enp3s0f1 -o enp4s0 -j ACCEPT
```

**English:**

- Let lab machines reach each other.
- Let lab machines access the production LAN or the internet.

#### Enable NAT (Masquerade) on Production NIC

```bash
iptables -t nat -A POSTROUTING -o enp4s0 -j MASQUERADE
```

**English:**

- Rewrites lab clients’ source IPs to 192.168.178.80 when going out to the internet.

### Verifying the Rules

Check rules by chain:

```bash
iptables -L -v -n
iptables -t nat -L -v -n
```

View packet counters, interfaces, and hit counts.

### nftables Note

Ubuntu uses **nftables** under the hood now. When you use iptables, you’re actually calling the **iptables-nft** compatibility layer. Rules are stored in the nftables backend.

You can verify nftables state with:

```bash
nft list ruleset
```

Or check the backend type:

```bash
update-alternatives --display iptables
```

### Tools for Debugging

- `ping` — verify basic connectivity
- `dig` / `nslookup` — test DNS
- `tcpdump -i <iface>` — see live traffic
- `conntrack -L` — list connection tracking table

### What Didn’t Work

- Using complex `rfc3442-classless-static-routes` options caused issues with FreeBSD’s `dhclient`.
- Initially, we tried specifying subnet-to-subnet routes via DHCP, which led to malformed lease data or dropped traffic.

### What Did Work

- A simpler design: each client gets just a default gateway (rtr02’s local NIC).
- rtr02 handles inter-subnet routing and internet NAT.
- Firewall rules allow only what’s necessary.

### Summary

We built a secure, functional firewall with just a few clear `iptables` rules. Masquerading enables internet access. Each rule was chosen for a specific need — DHCP, DNS, ping, routing — and tested with standard tools. Knowing how nftables and iptables interact gave us confidence in how the system behaves underneath.

Next time: Logging and rate-limiting for bad traffic!
