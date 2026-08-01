+++
title = "When Discord Meets Pi-hole: A Debugging Adventure"
date = "2025-01-19"
draft = true
description = "Sometimes the most interesting technical journeys begin with something small and annoying: in this case, a simple attempt to join the Kaggle Discord. What follows is a tale of sleuthing, diagnostics, and a few 'aha!' moments."
tags = ['dns', 'debugging', 'docker', 'networking', 'pihole', 'tailscale', 'troubleshooting']
categories = ["technical"]
+++

## When Discord Meets Pi-hole: A Debugging Adventure

Sometimes the most interesting technical journeys begin with something small and annoying: in this case, a simple attempt to join the Kaggle Discord. On the surface, nothing could be easier—click a link, accept an invite, and join the conversation. But behind the scenes, DNS, VPNs, and self-hosted services had other ideas. What follows is a tale of sleuthing, diagnostics, and a few "aha!" moments.

---

## The Setup

Our protagonist is a MacBook Pro sitting on a home network. The network isn't your average ISP-default setup: it's running a custom DNS stack. Here's the key architecture:

- **Router (ISP-provided)**: Handles DHCP, but forwards all DNS queries to a local DNS server.
- **Local DNS Server**: A NAS running Pi-hole in Docker, with Unbound as its recursive resolver.
- **Tailscale**: Adds a secure overlay network, and with it, another DNS layer (MagicDNS).
- **Client (MacBook Pro)**: Resolves DNS queries through a mix of Tailscale, Pi-hole, and sometimes Quad9.

The goal? To click a Kaggle Discord invite and successfully land in Discord. Simple enough.

---

## The First Symptom

Clicking the link didn't open Discord. Instead, the browser (Arc and Safari both) greeted us with:

```
This site can't be reached.
ERR_CONNECTION_REFUSED
```

So we began with the obvious: **is DNS working?**

---

## Testing DNS

### The Tools: `nslookup` and `dig`

From the MacBook, we ran:

```bash
nslookup discord.gg
dig discord.gg
```

And the results came back perfectly normal:

```text
discord.gg  IN A 162.159.133.234 ... (and other Cloudflare IPs)
```

So `discord.gg` was resolving fine. No DNS black hole here. That suggested the issue wasn't Discord in general, but maybe something specific to the **email verification link**.

---

## Narrowing Down

Discord's login emails don't link directly to `discord.gg`. Instead, they go through:

```
https://click.discord.com/ls/click?... (long redirect string)
```

This hinted at a possible culprit: some blocklist might be suspicious of a `click.*` domain.

So we tested:

```bash
dig click.discord.com
```

And boom — there it was:

```text
click.discord.com. IN A 0.0.0.0
```

That's not a routing problem. That's a DNS blackhole. Something was intentionally rewriting the domain to a dead-end address.

---

## Double-Checking Theories

- **Connection test:**

  ```bash
  curl -I https://click.discord.com
  ```

  Output: `Couldn't connect to server` → expected, since 0.0.0.0 isn't a real endpoint.

- **Mobile test:** Disable Wi-Fi and try on mobile data. Same hang. This suggested that on Wi-Fi at least, our DNS setup was the one responsible.

---

## Enter Pi-hole

We suspected Pi-hole was the culprit. And sure enough, the Pi-hole container logs showed it was alive and filtering queries:

```text
Blocking status is enabled
-> Blocked DNS queries: 8339
```

So Pi-hole was indeed doing its job—just a bit too enthusiastically. `click.discord.com` had been flagged as an ad/analytics domain by one of the subscribed blocklists.

---

## Recovering the Pi-hole Web UI

We tried to reach Pi-hole's admin dashboard but found the old bookmark no longer worked. A peek at the Docker Compose config revealed why:

```yaml
ports:
  - "8081:80"
```

The web interface wasn't at the default port anymore, but at `http://192.168.178.52:8081/admin/`.

Once there, we logged in with the configured password, navigated to the allowlist, and added:

```
click.discord.com
```

---

## Applying the Fix

To make sure the change took effect, we restarted Pi-hole's DNS service:

```bash
docker exec -it pihole pihole restartdns
```

Then tested again:

```bash
dig click.discord.com
```

And this time, the output looked healthy:

```text
click.discord.com. IN A 162.159.136.234 ... (Cloudflare IPs)
```

Victory! Clicking the verification link now properly redirected to Discord.

---

## Reflections & Learnings

- **Symptom:** Browser refused connection on a verification link.
- **First guess:** DNS issue.
- **Test:** `nslookup` and `dig` confirmed Discord core domain worked fine.
- **Narrowed scope:** The redirect domain `click.discord.com` was failing.
- **Diagnosis:** Pi-hole had blocked it, rewriting to 0.0.0.0.
- **Tools used:**

  - `dig` / `nslookup` to test resolution.
  - `curl` to confirm connections.
  - Pi-hole logs + web UI to identify the block.

- **Fix:** Whitelisted `click.discord.com`, restarted DNS, re-tested.

The broader takeaway? Self-hosted DNS gives you a lot of power, but sometimes that power catches innocent domains in its net. When troubleshooting, the combination of **symptoms → hypotheses → tools → fix** is invaluable. Each step told us whether to keep looking higher (browser, TLS, routing) or lower (DNS, blocklists).

And sometimes, the fix really is as simple as telling Pi-hole: _"This particular click is fine, thanks."_
