+++
title = "Debugging a Broken WireGuard Tunnel: A Journey Through Routers, Relays, and Routing Tables"
date = "2025-07-09"
description = "In a home lab far from the convenience of consumer plug-and-play, we had a plan: expose services running deep in a private lab network via a secure WireGuard tunnel to a public OpenBSD VPS. The goals ..."
tags = ['architecture', 'bsd', 'cloud', 'debugging', 'dns', 'firewall', 'freebsd', 'hosting', 'linux', 'nat', 'networking', 'nginx', 'openbsd', 'security', 'troubleshooting', 'tunnel', 'tutorial', 'ubuntu', 'unix', 'vpn', 'vps', 'web-server', 'wireguard']
categories = ["technical"]
+++


## Introduction

In a home lab far from the convenience of consumer plug-and-play, we had a plan: expose services running deep in a private lab network via a secure WireGuard tunnel to a public OpenBSD VPS. The goals were:

- Serve a static site (`100dop.clexp.net`) from the OpenBSD VPS
- Reverse proxy `blog.clexp.net` to an Nginx jail on a FreeBSD box behind double NAT
- Reverse proxy `books.clexp.net` to a Django app in a bhyve VM also behind that NAT

And it was all supposed to "just work."

Spoiler: it did not. But with persistence and some packet-fueled deduction, we found the culprit. Here's the journey.

---

## Architecture Recap

### Key Hosts:

- **vps-server**: Public OpenBSD VPS at `203.0.113.10`, WireGuard IP `10.100.0.1`
- **test-server**: Private FreeBSD server behind double NAT, WireGuard IP `10.100.0.2`
- **router**: Inner Ubuntu router doing NAT between the home LAN and the lab subnet

### Tunnel Goals:

- OpenBSD reverse proxies `blog` and `books` subdomains to the FreeBSD server via WireGuard.
- Jail for Nginx lives at `10.100.0.5`, VM for Django app at `10.100.0.6`
- Only HTTP flows through the tunnel; TLS terminates on the VPS.

---

## The Mystery: The Tunnel Handshakes, but Nothing Else Works

We had this WireGuard config:

```ini
[Interface]
PrivateKey = ...
ListenPort = 51820

[Peer]
PublicKey = ...
AllowedIPs = 10.100.0.0/24
```

We could run:

```sh
doas wg show
```

And see `latest handshake` entries. So the tunnel was up. But:

- `ping 10.100.0.2` → nothing.
- `nc -vz 10.100.0.5 80` → crickets.
- `relayctl show` → relayd not connecting.

Everything looked dead _except_ for that tantalizing handshake.

---

## Diagnosis Phase

We suspected:

- PF firewall rules
- A missing route
- A broken relayd or httpd configuration
- NAT/firewall on `router`

### 1. Checking Routing Tables

```sh
route -n show -inet
```

This showed no route for `10.100.0.0/24`. We had:

```
10.100.0.1         wg0
```

...but no subnet route. That meant OpenBSD didn't know how to reach other 10.100.0.x addresses!

### 2. Attempts to Fix It

We tried:

```sh
doas route add -net 10.100.0.0/24 -ifp wg0
```

And got:

```
Invalid argument
```

Then tried:

```sh
doas route add 10.100.0.0/24 wg0
```

```
wg0: bad address
```

After several syntactic misfires, the command that worked was:

```sh
doas route add 10.100.0.0/24 10.100.0.1
```

It felt wrong (adding a route to the subnet _via its own address?_), but it told OpenBSD: "Yes, 10.100.0.0/24 is reachable via this interface."

### 3. Immediate Breakthrough

```sh
ping 10.100.0.2
```

Success. Sweet, sweet ICMP.

---

## Understanding the Mechanics

In OpenBSD, `AllowedIPs` in WireGuard doesn't automatically insert a full subnet route the way Linux might. Only the peer's IP may be inserted (e.g. `10.100.0.2`).

So despite having `AllowedIPs = 10.100.0.0/24`, the OS did not know the route.

The fix:

```sh
doas route add 10.100.0.0/24 10.100.0.1
```

means:

> All traffic for 10.100.0.x — go to me (`10.100.0.1`) and I'll use `wg0` to send it.

---

## Firewall and Relayd Debugging

Next we confirmed:

- PF on `vps-server` had rules like:

```pf
pass in on vio0 proto tcp from any to port 443
pass out on wg0 proto tcp to 10.100.0.5 port 80
```

- `relayd.conf`:

```
table <blog> { 10.100.0.5 }
relay "blog" {
  listen on 127.0.0.1 port 8080
  forward to <blog> port 80
  protocol "http"
}
```

- `httpd.conf`:

```conf
server "blog.clexp.net" {
  listen on * tls port 443
  tls {
    certificate "/etc/ssl/clexp.net.fullchain.pem"
    key "/etc/ssl/private/clexp.net.key"
  }
  location "/" {
    root "/htdocs/empty"
  }
}
```

- `doas httpd -n` and `doas relayd -n -f /etc/relayd.conf` both returned `configuration OK`

All set.

---

## DNS Confusion and Victory

Then:

```sh
curl blog.clexp.net
```

```
could not resolve host
```

Ah — the Namecheap DNS needed a refresh.

After updating A records for `blog.clexp.net`, `100dop.clexp.net`, and `books.clexp.net`, everything clicked into place:

```sh
curl https://blog.clexp.net
<h1>Hello from nginx in a FreeBSD jail</h1>
```

**Success.**

---

## Lessons Learned

### 🧠 Routing:

- OpenBSD does **not** auto-add subnet routes from `AllowedIPs`
- You may need to add explicit routes for the full subnet

### 🧠 Debugging Tools:

- `wg show` → checks tunnel handshake
- `ping`, `nc -vz`, `sockstat` → tests connectivity
- `pfctl -sr` → confirm firewall rules
- `route -n show -inet` → inspect routing tables
- `httpd -n`, `relayd -n -f` → validate config syntax

### 🧠 Configuration:

- `httpd` on OpenBSD is simple and must offload anything fancy to `relayd`
- `relayd` can forward requests to remote IPs over tunnels
- PF must allow not just inbound 443, but also loopback 80 (relayd uses this)

---

## What I Learned

This project taught me the importance of **platform-specific knowledge**. I initially thought WireGuard would behave the same across Linux and BSD, but the reality was that OpenBSD's routing behavior differs significantly. The key insight was understanding that `AllowedIPs` in WireGuard doesn't automatically create subnet routes on OpenBSD like it does on Linux.

I also learned that **RFC 4193** (Unique Local IPv6 Unicast Addresses) becomes relevant when planning tunnel networks. While we used IPv4 for this setup, understanding how tunnel addressing works helped me troubleshoot the routing issues.

**Next time I would**: Document the routing requirements upfront. While I can troubleshoot routing issues, having a clear understanding of platform differences would have saved significant debugging time.

---

## Security Considerations

While WireGuard provides excellent encryption, I'm aware that exposing services through tunnels creates new attack vectors. I've configured basic firewall rules to restrict tunnel access, but proper production deployments would need more comprehensive security monitoring and access controls.

---

## Closing Thoughts

What started as a basic reverse proxy setup turned into a hands-on lesson in routing, tunnel behavior, and OpenBSD peculiarities.

There were a few moments of confusion and a lot of `Invalid argument`, but in the end, it was just a missing route.

---

> **Note**: This post documents a lab environment setup. Real production networks should use different IP ranges and follow your organization's security policies.
