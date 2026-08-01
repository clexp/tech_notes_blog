+++
title = "Ubuntu, FreeBSD and NixOS"
date = "2025-07-09"
draft = true
description = "This guide walks through the process of creating and verifying a routed network lab using Ubuntu (with Netplan), FreeBSD, and NixOS. We'll configure interfaces, default routes, and routing between two..."
tags = ['bsd', 'dhcp', 'dns', 'firewall', 'freebsd', 'linux', 'nat', 'networking', 'nixos', 'security', 'tutorial', 'ubuntu', 'unix', 'vlan']
categories = ["technical"]
+++

## Inter-Subnet Routing Lab: Ubuntu, FreeBSD, and NixOS

This guide walks through the process of creating and verifying a routed network lab using Ubuntu (with Netplan), FreeBSD, and NixOS. We'll configure interfaces, default routes, and routing between two subnets, all reboot-proof. Let's dive in.

---

## 🌐 Network Overview

We have a router (`rtr02`) with two NICs:

- **enp3s0f0** → `10.0.0.1/24` (FreeBSD `tb02`, `10.0.0.2`)
- **enp3s0f1** → `192.168.0.1/24` (NixOS laptop, `192.168.0.2`)

Each client system has:

- A static IP in its subnet
- A default gateway pointing to the router’s respective interface

---

## 🖥️ Interface Setup

### Ubuntu (router - `rtr02`)

Edit Netplan (e.g. `/etc/netplan/40-lab.yaml`):

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp3s0f0:
      dhcp4: no
      addresses: [10.0.0.1/24]
    enp3s0f1:
      dhcp4: no
      addresses: [192.168.0.1/24]
```

Apply:

```bash
sudo netplan apply
```

### FreeBSD (`tb02`)

Edit `/etc/rc.conf`:

```conf
ifconfig_re0="inet 10.0.0.2 netmask 255.255.255.0"
defaultrouter="10.0.0.1"
static_routes="labnet"
route_labnet="-net 192.168.0.0/24 10.0.0.1"
```

Bring up:

```sh
## service netif restart
## service routing restart
```

### NixOS

`configuration.nix`:

```nix
networking.useNetworkd = true;
networking.interfaces.enp0s13f0u2.ipv4.addresses = [ {
  address = "192.168.0.2";
  prefixLength = 24;
} ];
networking.defaultGateway.interface = "enp0s13f0u2";
networking.defaultGateway.address = "192.168.0.1";
```

Rebuild:

```bash
sudo nixos-rebuild switch
```

---

## 🚪 Default Routes & 0.0.0.0

The default route is the path packets take when there's no specific route for the destination. It's represented as:

```none
0.0.0.0/0 via <gateway> dev <iface>
```

This means: "send all packets not destined for local subnets to this gateway." It’s not an actual machine, just shorthand for the default.

---

## 🧮 Subnet Ranges

Common LAN ranges:

- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

We’re using:

- `10.0.0.0/24` for FreeBSD lab
- `192.168.0.0/24` for NixOS lab

---

## 🔁 Enabling Inter-Subnet Routing on Ubuntu

Edit `/etc/sysctl.conf` or set live:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Make it permanent:

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

**Note:** This is routing — not NAT. The router is simply passing packets between subnets, not modifying IPs.

---

## 🧭 Default Routes per Subnet

### Ubuntu

Handled via Netplan’s static IP config:

```yaml
routes:
  - to: 0.0.0.0/0
    via: <gateway>
```

### FreeBSD

```conf
defaultrouter="10.0.0.1"
static_routes="labnet"
route_labnet="-net 192.168.0.0/24 10.0.0.1"
```

Reload:

```sh
## service routing restart
```

### NixOS

In `configuration.nix`:

```nix
networking.defaultGateway.interface = "enp0s13f0u2";
networking.defaultGateway.address = "192.168.0.1";
```

---

## 🔍 Testing Connectivity

### Ping test:

```sh
ping 192.168.0.2   # From FreeBSD to NixOS
ping 10.0.0.2      # From NixOS to FreeBSD
```

### Tcpdump (on rtr02):

```bash
sudo tcpdump -i enp3s0f0 icmp
sudo tcpdump -i enp3s0f1 icmp
```

You'll see packets arriving and being forwarded. If it’s one-way, check routing tables (`netstat -rn`, `ip route show`) and gateways.

---

## ✅ Summary

We’ve:

- Brought up NICs on 3 OSes
- Set static IPs and default gateways
- Understood the role of `0.0.0.0` in routing
- Connected two subnets via a Linux router
- Verified the path using `ping` and `tcpdump`

This is foundational networking knowledge, and you now have a working test lab to build from — whether learning firewalling, DNS, or VLANs.

More to come!
