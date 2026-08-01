# Debugging Dockerized DNS (Pi-hole/Unbound) on Ubuntu with systemd-resolved and Tailscale

### Introduction

This post documents a complex debugging session trying to expose a Dockerized Pi-hole DNS server running on Ubuntu 24.04, coexisting with Tailscale, systemd-resolved, and a firewall managed by `iptables`. The goal was to allow internal and LAN DNS queries via Pi-hole, hosted at `192.168.178.52`, port 53 (later switched to 1053 due to conflicts).

Despite following best practices and documented setups, DNS queries from the host or LAN kept timing out. This post walks through the tools and approaches used to debug and work around the issue.

---

## Problem Summary

Pi-hole (with Unbound) was containerized and configured to:

- Serve DNS queries via port 53
    
- Listen on `172.20.0.3` in its Docker bridge network
    
- Be exposed externally on host IP `192.168.178.52`, initially on port 53, later port 1053
    

However, DNS queries to Pi-hole from the host or LAN kept timing out.

---

## Tools Used

### 1. `ss`, `netstat`, and `lsof`

Used to inspect what processes were bound to port 53:

```bash
ss -tulnp | grep :53
lsof -i :53
```

Findings:

- `systemd-resolved` was bound to `127.0.0.53:53`
    
- Docker proxy was bound to `192.168.178.52:53` (or later 1053)
    
- No one bound to `0.0.0.0:53` after port remap
    

### 2. `dig`

Used to check DNS functionality from various interfaces:

```bash
dig @127.0.0.1 example.com
dig @172.20.0.3 example.com
dig @192.168.178.52 -p 1053 example.com
```

Findings:

- `127.0.0.1` would sometimes work via stub listener
    
- `172.20.0.3` (Pi-hole's bridge IP) worked reliably
    
- `192.168.178.52` on port 53/1053 consistently failed
    

### 3. `iptables`/`nftables`

Used to inspect and control firewall behavior:

```bash
sudo iptables -t nat -L -n -v
sudo iptables -L -n -v
sudo iptables -A INPUT -p udp --dport 1053 -j ACCEPT
```

Findings:

- Chains like `DOCKER`, `POSTROUTING`, and `PREROUTING` existed but traffic never hit `INPUT` rules for 1053
    
- Adding logging showed no DNS traffic hitting the firewall
    

### 4. `docker network inspect`

To verify container IPs:

```bash
docker network inspect pi_bnd_net
```

Confirmed:

- Pi-hole at `172.20.0.3`
    
- Unbound at `172.20.0.2`
    

---

## Workarounds and Observations

### 1. Port Binding Conflict

- Tailscale and systemd-resolved rely on `127.0.0.53` and local port 53.
    
- Binding Pi-hole to `0.0.0.0:53` causes conflict
    
- Switched Docker to expose only `192.168.178.52:1053:53`
    

### 2. systemd-resolved Forwarding

Configured `/etc/systemd/resolved.conf`:

```ini
[Resolve]
DNS=192.168.178.52
FallbackDNS=1.1.1.1 8.8.8.8
DNSStubListener=yes
```

Forwarding failed when using `192.168.178.52`, but succeeded via `127.0.0.1` or `172.20.0.3`

### 3. Docker Network Isolation

Attempted to modify:

```bash
iptables -D DOCKER-ISOLATION-STAGE-2 -o br-XXXX -j DROP
iptables -A DOCKER-ISOLATION-STAGE-2 -o br-XXXX -j RETURN
```

Result: No improvement

### 4. DNS traffic forwarding to 1053

Even with:

```bash
iptables -A INPUT -p udp --dport 1053 -j ACCEPT
```

No packets hit the firewall (checked with `journalctl -f | grep DNS_IN`)

---

## Additional Issues

### SSH Key Errors

SSH to the backup server failed due to a key mismatch:

```bash
ssh-keygen -f "/home/infra/.ssh/known_hosts" -R "192.168.177.2"
ssh infra@192.168.177.2
```

Eventually accepted new key, but still hit `Permission denied` due to missing password authentication.

### Docker Compose Confusion

Docker only allows a single host-to-container port mapping per container port. Attempting multiple host IPs for `:53` will result in only the last one taking effect.

---

## Key Takeaways

1. **systemd-resolved and Tailscale**: Expect DNS port 53 conflicts.
    
2. **Use dedicated host IPs or high ports** to avoid 127.0.0.1 collisions.
    
3. **Container bridge IPs work reliably**, but aren't exposed externally without NAT.
    
4. **Docker’s userland proxy/NAT can silently fail**, even with correct port bindings.
    
5. **Firewall debugging requires correct toolset (`iptables-legacy` vs `nft`)** and packet logging.
    

---

## Final Thoughts

Modern Linux networking with containers, DNS stub listeners, split DNS, and software like Tailscale is a complex ecosystem. Getting a simple DNS server like Pi-hole working on port 53 inside Docker—without colliding with other system services—is non-trivial.

Even with `iptables` open, port bindings set, and services responding, something subtle (like userland proxy, interface isolation, or NAT not firing) can break functionality.

Further work might explore:

- Bypassing Docker proxy entirely with host networking
    
- Running Pi-hole outside Docker
    
- Using a separate VM or LXD container
    

---

> If you've been down this rabbit hole too, you're not alone. And if not yet—strap in.