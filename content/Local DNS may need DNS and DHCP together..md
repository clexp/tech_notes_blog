+++
title = "Local Dns May Need Dns And Dhcp Together."
date = "2025-07-09"
description = "There are days when your network hums along quietly like a well-trained dog. Then there are days when it turns into a misbehaving circus. This was one of the latter."
tags = ['containers', 'devops', 'dhcp', 'dns', 'docker', 'firewall', 'iptables', 'linux', 'nat', 'networking', 'nixos', 'security']
categories = ["technical"]
+++

## Replacing the FritzBox DHCP with Pi-hole: A Network Detective Story

There are days when your network hums along quietly like a well-trained dog. Then there are days when it turns into a misbehaving circus. This was one of the latter.

### Act I: The Dream

We had a goal: unify DNS and DHCP control under one roof — specifically, Pi-hole. The motivation was clear: Pi-hole was already filtering DNS queries on our home network, and it seemed natural to let it also handle DHCP, providing clean integration between hostname-to-IP mapping and ad-blocking resolution. It would also let us escape some of the FritzBox’s limitations.

Our Pi-hole lives in a Docker container on a server called `nas04` (192.168.178.52), part of the wider home network (`192.168.178.0/24`). The FritzBox router normally handled DHCP, handing out IPs and providing itself as the default DNS server — but we wanted to change that, making Pi-hole the authoritative source.

### Act II: The Cutover

The first move was to turn off DHCP on the FritzBox (this is a simple UI checkbox), and enable it on Pi-hole (via the web UI under _Settings → DHCP_). We also ensured that the Pi-hole container had the right Docker config:

```yaml
ports:
  - '192.168.178.52:53:53/udp'
  - '192.168.178.52:53:53/tcp'
  - '192.168.178.52:67:67/udp'  # crucial for DHCP!
cap_add:
  - NET_ADMIN
```

But then things went sideways.

### Act III: The Symptoms

Some devices (Android, iPhone, NixOS box) continued to work fine. Others — a MacBook, an iPad, a Windows laptop — either couldn’t resolve DNS or didn’t seem to be getting DHCP leases at all. The TV grew sluggish. The household grew restless.

The `scutil --dns` command on macOS showed that DNS servers were still pointing to the old addresses:

```bash
scutil --dns | grep 'nameserver'
nameserver[0] : 100.100.100.100
nameserver[0] : 192.168.1.1
```

This was a clue — clearly, the Mac hadn’t been told about the Pi-hole’s DNS, and hadn’t picked up a new lease from the Pi-hole DHCP server.

### Act IV: Diagnosis

We suspected the DHCP broadcast wasn’t being seen by Pi-hole. We used:

```bash
sudo lsof -iUDP -P -n | grep ':67'
```

To confirm that the Pi-hole container was actually listening on port 67 (the DHCP port). Output like this meant we were good:

```bash
docker-pr 94214 root 4u IPv4 338503 0t0 UDP 192.168.178.52:67
```

If not, the fix was to expose the port in the Docker Compose file and restart:

```yaml
- '192.168.178.52:67:67/udp'
```

and then:

```bash
docker compose down && docker compose up -d
```

Next, we realized some devices never asked for a new lease — and macOS in particular can hold onto old DHCP leases for dear life. So we tried releasing and renewing leases manually:

```bash
sudo ipconfig set en0 DHCP
```

We also cleared the DNS cache on the Mac:

```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

### Act V: The Firewall

Even with port 67 exposed, DHCP still wasn’t working for all devices. We checked the firewall. If you’re using `ufw`, you need to allow UDP/67:

```bash
sudo ufw allow proto udp from any to any port 67 comment 'Allow DHCP requests'
```

If you’re using raw `iptables`:

```bash
sudo iptables -A INPUT -p udp --dport 67 -j ACCEPT
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

### Act VI: Retreat and Regroup

At this point, users were getting loud. So we reverted — DHCP back on in the FritzBox, Pi-hole’s DHCP disabled. Peace returned.

But the lesson was invaluable. We now understood that Docker’s network isolation means that exposing ports like 67/UDP is essential and that some clients (looking at you, macOS) don’t easily let go of their leases or DNS settings. Also, port binding and capabilities (`NET_ADMIN`) are critical for DHCP functionality in containers.

### Final Thoughts

This episode reminded us that network transitions are best done with a quiet house and a clear head. Still, we’re closer than ever to cutting the FritzBox cord. Next time, we’ll:

- Preconfigure the firewall for port 67
    
- Ensure all Docker `cap_add` and port bindings are in place
    
- Use short leases temporarily for fast turnaround
    
- Test with one device before switching the entire LAN
    

As any good sysadmin knows: move slow, test often, document everything, and keep the coffee hot.

---

_Filed under: Home Lab, Pi-hole, Docker, Networking Adventures_
