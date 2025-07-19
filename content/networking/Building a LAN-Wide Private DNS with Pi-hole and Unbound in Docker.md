+++
title = "Building a LAN-Wide Private DNS with Pi-hole and Unbound in Docker"
date = "2025-07-09"
description = "This guide walks through the process of deploying a private, filtered, and locally cached DNS infrastructure using Pi-hole and Unbound, running in Docker on a central Ubuntu-based server (nas-server). The ..."
tags = ['backup', 'containers', 'debugging', 'devops', 'dhcp', 'dns', 'docker', 'firewall', 'iptables', 'linux', 'nat', 'networking', 'security', 'storage', 'troubleshooting', 'tutorial', 'ubuntu', 'vlan']
categories = ["technical"]
+++

This guide walks through the process of deploying a private, filtered, and locally cached DNS infrastructure using **Pi-hole** and **Unbound**, running in **Docker** on a central **Ubuntu-based server** (`nas-server`). The DNS service is made available across:

- The main LAN (`192.168.1.0/24`)
- A lab VLAN (`192.168.2.0/24`)
- A backup subnet behind a second interface on `nas-server`
- Remote clients via **Tailscale**

The goal: provide all clients with a **fast, reliable, privacy-preserving DNS resolver**, immune to ISP tampering and capable of blocking ads/malware domains.

---

## Goals

- Internal clients (LAN, lab, backup, and Tailscale) can query DNS at `192.168.1.52`
- Pi-hole filters domains using community and custom blocklists
- Unbound performs DNSSEC-validating recursive resolution
- All services run in Docker for portability and simplicity

---

## Network Structure

### Server (`nas-server`) Interfaces

- `enp3s0` - LAN (192.168.1.52)
- `enp4s0` - Backup subnet gateway (192.168.2.1)
- `br-<id>` - Docker bridge (172.20.0.0/24)
- `tailscale0` - Remote access (Tailscale)

### Docker DNS Services

- `pihole` (172.20.0.3)
- `unbound` (172.20.0.2)

---

## docker-compose.yml

```yaml
services:
  pihole:
    image: pihole/pihole:latest
    ports:
      - "192.168.1.52:53:53/udp"
      - "192.168.1.52:53:53/tcp"
      - "8081:80"
    environment:
      TZ: Europe/London
      WEBPASSWORD: yourpassword
      FTLCONF_dns_listeningMode: "all"
    volumes:
      - "./etc-pihole:/etc/pihole"
      - "./etc-dnsmasq.d:/etc/dnsmasq.d"
    depends_on:
      - unbound
    dns:
      - 172.20.0.2
    networks:
      net:
        ipv4_address: 172.20.0.3

  unbound:
    image: mvance/unbound:latest
    networks:
      net:
        ipv4_address: 172.20.0.2

networks:
  net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/24
```

---

## Common Problems and Their Fixes

### 1. **Pi-hole not answering LAN clients**

**Error**: `dig @192.168.1.52 example.com` times out from LAN clients.

**Root Cause**: Pi-hole's `dnsmasq` restricts queries to local interfaces.

**Fix**:

```conf
## etc-dnsmasq.d/99-allow-remote.conf
local-service=0
```

Add this file, then restart the container:

```bash
docker compose restart pihole
```

---

### 2. **Pi-hole not listening on Docker's published IP**

**Investigation**:

```bash
ss -tulnp | grep :53
```

Expected:

```
udp   UNCONN 0 0 192.168.1.52:53 0.0.0.0:* users:("docker-proxy")
```

If missing, Docker isn't forwarding to the container.

**Fix**:  
Ensure `docker-compose.yml` maps port 53 **specifically**:

```yaml
ports:
  - "192.168.1.52:53:53/udp"
  - "192.168.1.52:53:53/tcp"
```

---

### 3. **Packet replies from container not routed back correctly**

**Symptom**: Packet enters container but no response seen from client.

**Fix**: Add a NAT MASQUERADE rule:

```bash
sudo iptables -t nat -A POSTROUTING -s 172.20.0.0/24 -d 192.168.1.0/24 -j MASQUERADE
```

**Explanation**: Docker containers return replies with their `172.20.x.x` source IP. Without NAT, the LAN client drops the packet.

---

### 4. **Systemd-resolved confusion**

**Problem**: `127.0.0.53` is bound by `systemd-resolved`, intercepting local DNS.

**Diagnose**:

```bash
resolvectl status
```

**Fix**: Either:

- Stop `systemd-resolved` entirely and manage `/etc/resolv.conf`
- Or configure resolved to use Pi-hole:

```ini
## /etc/systemd/resolved.conf
DNS=192.168.1.52
FallbackDNS=1.1.1.1 8.8.8.8
DNSStubListener=no
```

Setting `DNS=192.168.1.52` in `resolved.conf` can cause local resolution on the host (`nas-server`) to fail. Although `192.168.1.52` is mapped to Pi-hole via Docker's published port, the Linux kernel may short-circuit queries to that address internally via the `lo` interface instead of routing them through Docker's userland proxy. This causes DNS queries from the host to time out or be intercepted by `systemd-resolved` itself if it is still listening.

To avoid this, you can point systemd-resolved to Pi-hole's internal Docker IP (`172.20.0.3`), which reliably routes through the bridge interface.

```ini
## /etc/systemd/resolved.conf
DNS=172.20.0.3
FallbackDNS=1.1.1.1 8.8.8.8
DNSStubListener=no
```

Then:

```bash
sudo systemctl restart systemd-resolved
```

---

### 5. **Confirming Container Routing**

Use `tcpdump` to trace:

```bash
sudo tcpdump -i any port 53 -n
```

Example:

```
192.168.1.67.61714 > 172.20.0.3.53: A? example.com.
```

This confirms the Docker NAT and bridge are working correctly.

Use `conntrack` to diagnose packet flow:

```bash
sudo conntrack -L | grep dport=53
```

---

## Result

LAN and lab clients now query `192.168.1.52` and receive DNS answers filtered by Pi-hole, resolved recursively via Unbound, without leaks to upstream DNS.

All interfaces (Tailscale, Docker, LAN) are secured and plumbed to work together with NAT, firewall, and listener configuration correct.

---

## Bonus: Tools Reference

| Tool         | Purpose                   | Example                          |
| ------------ | ------------------------- | -------------------------------- |
| `dig`        | Test DNS resolution       | `dig @192.168.1.52 example.com`  |
| `ss`         | View listening ports      | `ss -tulnp                       |
| `tcpdump`    | Trace packets             | `sudo tcpdump -i any port 53 -n` |
| `conntrack`  | View NAT/connection state | `conntrack -L                    |
| `resolvectl` | Inspect systemd-resolved  | `resolvectl status`              |

---

## What I Learned

This project taught me the importance of **DNS architecture planning**. I initially thought I could just drop Pi-hole into Docker and it would work everywhere, but the reality was more complex. The key insight was understanding how Docker networking interacts with system DNS resolution - something that's rarely discussed in simple tutorials.

I also learned that **RFC 1035** (the DNS specification) becomes much more relevant when you're building your own resolver. Understanding how DNS queries flow through different interfaces helped me troubleshoot issues that seemed mysterious at first.

**Next time I would**: Set up DNS monitoring from the start. While I can see queries in Pi-hole's web interface, having proper logging and alerting would have helped me catch the systemd-resolved conflict much earlier.

---

## Security Considerations

While this setup provides privacy benefits over ISP DNS, I'm aware that running your own DNS resolver can introduce new attack vectors. I've configured basic firewall rules to restrict DNS access to trusted subnets, but proper production deployments would need more comprehensive security monitoring.

---

## Next Steps

- Add DoH or DNS-over-TLS with Unbound
- Enable Pi-hole's DHCP to integrate hostname resolution
- Extend to IPv6

---

> **Note**: This post documents a lab environment setup. Real production networks should use different IP ranges and follow your organization's security policies.
