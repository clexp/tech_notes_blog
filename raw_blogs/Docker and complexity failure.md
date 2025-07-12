Here's a blog post draft in Markdown, capturing the journey, tools used, findings, and reflections on using Docker to host Pi-hole while Tailscale and system DNS are in play:

---

# Troubleshooting Pi-hole in Docker with Tailscale and Port Conflicts

_Posted on May 4, 2025_

## Background

I attempted to run Pi-hole in a Docker container on my Ubuntu 22.04 server (`nas04`). The host is also running Tailscale and various other services. My goal: deploy Pi-hole as a local DNS sinkhole, running in a container, while the host remains reachable over Tailscale. Simple enough?

Not quite.

What followed was a deep dive into port bindings, container network isolation, system-level DNS listeners, and the nuanced (sometimes conflicting) realities of Docker, Tailscale, and DNS.

---

## The Problem: Port 53 Conflicts

Pi-hole requires port 53 (TCP and UDP) for DNS service. On first run, I quickly discovered that **something else was already using port 53 on the host**.

I used `lsof` to identify the culprits:

```sh
sudo lsof -i :53
```

This revealed that **Tailscale and Syncthing** were communicating over DNS ports, with Tailscale using `localhost:domain`. Example output:

```
tailscale 626632 root  33u  IPv4 ... TCP localhost:55188->localhost:domain (SYN_SENT)
```

So, even if Docker mapped container port 53 to the host (on a non-default port like 1053), **Tailscale’s activity on port 53 conflicted with Pi-hole**—because the Linux kernel doesn’t allow multiple listeners on the same UDP port/interface combination.

## Resolved.conf and the Stub Listener

Some advice online pointed toward `/etc/systemd/resolved.conf` with this setting:

```ini
DNSStubListener=no
```

This setting disables systemd-resolved’s built-in DNS server on `127.0.0.53:53`. In our case, this was **not the main issue**, since Tailscale's MagicDNS and the tailscaled daemon itself were using DNS via localhost. Nonetheless, this setting is **important when debugging port 53 issues** in general.

## Docker Port Mapping

Pi-hole's container was configured to **expose port 53 inside the container** and map it to **1053 on the host**:

```sh
docker port pihole
```

Returned:

```
53/tcp -> 0.0.0.0:1053
53/udp -> 0.0.0.0:1053
```

So I tried:

```sh
dig @192.168.178.52 -p 1053 bbc.co.uk
```

But it failed with:

```
dig: couldn't get address for '192.168.178.52:1053': not found
```

(The original `dig` syntax was wrong. It should use `-p 1053` rather than appending `:1053` to the IP.)

## Network Debugging

I inspected the container's internal IP:

```sh
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pihole
# 172.20.0.3
```

Then tested from the host:

```sh
dig @172.20.0.3 bbc.co.uk
```

Result:

```
;; communications error to 172.20.0.3#53: timed out
```

And:

```sh
curl http://172.20.0.3
# Just hung—no response.
```

Even though Docker reported Pi-hole as “healthy”, nothing reachable on the network suggested that Pi-hole was actually serving DNS or web content.

## Firewall Rules

I double-checked `iptables`:

```sh
sudo iptables -L -n -v | grep 1053
# No results
```

So I added explicit rules:

```sh
sudo iptables -A INPUT -p tcp --dport 1053 -j ACCEPT
sudo iptables -A INPUT -p udp --dport 1053 -j ACCEPT
```

Still no luck. Even with the ports open, the container seemed unreachable.

## Summary of Tools Used

- `lsof -i :53` – to find DNS port conflicts
    
- `docker inspect` – to view container networks and IPs
    
- `docker port` – to verify port mappings
    
- `dig` – to test DNS queries against custom ports and addresses
    
- `curl` – to test Pi-hole’s web interface
    
- `iptables` – to check and modify firewall rules
    
- `ss -tuln` – to view listening ports on the host
    

---

## Reflection: Docker, Isolation, and Complexity

Docker promises containerized isolation, and in many cases it delivers. But **when you're dealing with low-level system services like DNS**, the abstraction begins to blur.

Here’s the rub:

- Docker containers can't fully escape the host's network stack, especially for privileged ports (like 53).
    
- Tailscale, which adds its own DNS layer (MagicDNS), can block or interfere with those ports.
    
- The container’s `healthy` status means little if it can’t serve real traffic due to firewall, routing, or port issues.
    

You end up debugging not just Docker—but also the host OS, network namespaces, firewall rules, and any other running services.

Docker **reduces environment configuration complexity**, but introduces **integration complexity**. That’s the trade-off.

---

## Virtual Machines: An Alternative?

With a VM:

- **You can bind port 53 inside the VM** without fighting the host's DNS services.
    
- The VM has its own virtual NICs and IP stack, fully isolated from the host unless bridged.
    
- You sacrifice some performance and provisioning speed, but gain clarity and control.
    

In fact, if I were to do this again, I'd consider:

- Running Pi-hole in a **lightweight VM (e.g., with KVM or Proxmox)**.
    
- Avoiding Docker entirely for core infrastructure services like DNS or DHCP.
    
- Letting containers handle apps, not infrastructure.
    

---

## Conclusion

Despite getting close, I didn't get Pi-hole working in Docker with Tailscale active and port 53 constraints on the host. It’s a good reminder that **containerized infrastructure services are not always the best fit**, especially when other agents (like Tailscale) touch the same layers.

Next steps?

Maybe try again with:

- Pi-hole in a VM
    
- Tailscale off or running in a sandbox
    
- Or use a dedicated lightweight host (like a Raspberry Pi) for DNS.
    

For now, this attempt gets parked. Lessons learned. Frustration acknowledged. Curiosity preserved.

---

Would you like me to format this for a particular static site generator like Zola, Hugo, or Pelican?