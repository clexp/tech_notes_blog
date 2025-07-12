+++
title = "Building A Dual Stack Lab  Ipv6 Setup From Tunnel To Lan"
date = "2025-07-09"
description = "_By clexp, documenting a real home lab deployment_"
tags = ['bsd', 'debugging', 'dhcp', 'dns', 'firewall', 'freebsd', 'iptables', 'linux', 'nat', 'networking', 'nixos', 'security', 'tunnel', 'tutorial', 'ubuntu', 'unix', 'vlan']
categories = ["technical"]
+++

# Building a Dual-Stack Lab: IPv6 Setup from Tunnel to LAN

_By clexp, documenting a real home lab deployment_

---

## Overview

IPv6 brings immense promise: an end to NAT, direct global addressing, and a cleaner internet. But setting it up in a home lab with legacy hardware and multiple OSes (FreeBSD, NixOS, Ubuntu) is not plug-and-play. This blogpost documents how I configured IPv6 from my ISP tunnel endpoint, through my custom Ubuntu router (`rtr02`), to two test subnets and clients. I describe key concepts, working configurations, and gotchas.

---

## Goals

- Use native or tunneled IPv6 from ISP
    
- Configure Ubuntu (`rtr02`) to route and advertise IPv6 on internal subnets
    
- Ensure clients on VLANs (FreeBSD and NixOS) get global IPv6 addresses via SLAAC
    
- Set up ip6tables/nftables firewalling
    
- Enable name resolution and demonstrate IPv6 connectivity end-to-end
    

---

## Topology

```
[Internet / ISP Router (FritzBox)]
        |
  (Tunnel or Prefix Delegation)
        |
      [rtr02 - Ubuntu 24.04]
        |           |
   vlan1 (192.168.0.0/24 + IPv6 /64)   vlan2 (10.0.0.0/24 + IPv6 /64)
        |                               |
    [NixOS Laptop]               [FreeBSD tb02]
```

- `rtr02` connects to the FritzBox which acts as a 6in4 tunnel endpoint with Hurricane Electric.
    
- `rtr02` receives a routed /64 or /48 (e.g., `2a02:8012:2217::/48`) from the ISP.
    
- Internal VLANs are routed with their own /64 prefixes.
    

---

## Step 1: Verify IPv6 from the ISP

My FritzBox reports:

```bash
IPv6 address: 2a02:8011:d017:3091::1/64
IPv6 prefix: 2a02:8012:22a7::/48
```

On `rtr02`, I confirmed receipt with:

```bash
ip -6 addr show dev enp4s0
```

---

## Step 2: Assign IPv6 to Router Interfaces

Using Netplan (`/etc/netplan/99-ipv6.yaml`):

```yaml
network:
  version: 2
  ethernets:
    enp3s0f0:  # Connected to tb02
      addresses:
        - 2a02:8012:2217:10::1/64
    enp3s0f1:  # Connected to NixOS
      addresses:
        - 2a02:8012:2217:2::1/64
```

Apply with:

```bash
sudo netplan apply
```

---

## Step 3: Configure `radvd` for SLAAC

Install and configure `radvd` on `rtr02`:

`/etc/radvd.conf`:

```conf
interface vlan1 {
    AdvSendAdvert on;
    prefix 2a02:8012:2217:2::/64 {
        AdvOnLink on;
        AdvAutonomous on;
    };
};

interface vlan2 {
    AdvSendAdvert on;
    prefix 2a02:8012:2217:10::/64 {
        AdvOnLink on;
        AdvAutonomous on;
    };
};
```

Enable and start:

```bash
sudo systemctl enable --now radvd
```

🔧 **Bug fix**: A missing `};` caused a syntax error, which `journalctl -xeu radvd.service` helped uncover.

---

## Step 4: SLAAC on Clients

### NixOS

NixOS auto-configures IPv6 via SLAAC by default. After `radvd` was fixed:

```bash
ip -6 addr show
```

Returned:

```bash
2a02:8012:2217:2:db8f:a465:8daa:3bca/64
```

### FreeBSD (tb02)

Initially no IPv6 address appeared:

```bash
ifconfig igb0
```

Showed only a link-local `fe80::` address.

### Troubleshooting:

- `nd6` flags showed `IFDISABLED` — fix via:
    
    ```bash
    sysctl net.inet6.ip6.accept_rtadv=1
    ```
    
- Confirm `radvd` packets via:
    
    ```bash
    sudo tcpdump -i igb0 icmp6
    ```
    
- Manually assign for testing:
    
    ```bash
    sudo ifconfig igb0 inet6 2a02:8012:2217:10::50 prefixlen 64
    ping6 2a02:8012:2217:10::1
    ```
    

---

## Step 5: Firewalling with nftables

Ubuntu 24.04 prefers `nftables`. Here's a basic IPv6 rule set:

```nft
table inet filter {
    chain input {
        type filter hook input priority 0;
        policy drop;

        ct state established,related accept
        ip6 nexthdr icmpv6 accept
        iifname "lo" accept
    }

    chain forward {
        type filter hook forward priority 0;
        policy drop;

        ct state established,related accept
        ip6 nexthdr icmpv6 accept
    }

    chain output {
        type filter hook output priority 0;
        policy accept;
    }
}
```

Load it with:

```bash
sudo nft -f /etc/nftables.conf
```

---

## Step 6: DNS + IPv6

### Pi-hole + Unbound on server (s04):

- Consider running Pi-hole with IPv6 enabled to handle AAAA lookups.
    
- Set your clients’ DNS to `s04` or `rtr02`.
    

### Problems:

- NixOS could ping IPv6 IPs but not domain names → DNS wasn’t working yet.
    
- `rtr02` must allow UDP/53 on IPv6 if forwarding DNS.
    

### Fix:

Add to nftables:

```nft
udp dport 53 accept
```

---

## Conclusion

This journey through IPv6 setup in a home lab highlighted:

- The importance of RA (Router Advertisements) and SLAAC
    
- FreeBSD-specific quirks (nd6, manual sysctl tuning)
    
- The transition from iptables to nftables
    
- DNS being a required pillar in making IPv6 usable
    

A working IPv6 setup for modern labs involves coordination between:

- ISP configuration or tunneling (e.g. Hurricane Electric 6in4)
    
- Router advertisement (`radvd`) and correct interface assignments
    
- Host OS configuration, including accepting RAs
    
- A reliable IPv6-compatible DNS resolver
    
- A carefully permissive but secure firewall configuration
    

---

_Next steps:_ Enable dynamic DNS for IPv6, integrate DHCPv6 if needed, and explore reverse DNS for internal lab domains.

---
