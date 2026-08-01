+++
title = "Exploding Networks 2"
date = "2025-07-09"
description = "_May 2025 — Somewhere between coffee and chaos._"
tags = ['dhcp', 'dns', 'linux', 'networking', 'nixos', 'security', 'ssh']
categories = ["technical"]
+++

## 🧠 The Day My DNS Died (and Took My Network With It): A Sysadmin Lab Chronicle

_May 2025 — Somewhere between coffee and chaos._

So there I was, deep in the bowels of my home lab, configuring `BIND9` for local DNS and `ISC DHCP Server` for dynamic IP leases. Everything was going fine — too fine. My router (`rtr02`) was humming along, clients were getting IPs, DNS lookups worked... even reverse lookups were starting to take shape.

But I wanted _more_. I wanted **Dynamic DNS (DDNS)**, that mythical beast where DHCP clients register themselves in the DNS zone, auto-magically keeping hostnames and IPs in sync.

### 🧨 Enter: The Line That Killed Everything

Somewhere in my `dhcpd.conf`, I dropped in this innocent-looking line:

dhcpd

CopyEdit

`option host-name = config-option host-name;`

I'd seen it floating around in online forums. Surely it would help clients tell the server their hostnames... right?

Wrong.

The next thing I knew, everything started crumbling:

- The DHCP server wouldn't start.
- No clients could get an IP address.
- My laptop was marooned with no DNS.
- SSH into `rtr02` failed. **FAILED.**
- I found myself hunched over a monitor directly plugged into the router like it was 2002.

### 🕵️‍♂️ Diagnosing the Disaster

A few commands told the tale:

bash

CopyEdit

`systemctl status isc-dhcp-server`

→ Failed to start. No helpful logs. Just broken dreams.

The culprit? That `option host-name = config-option host-name;` line. ISC DHCP doesn’t speak that syntax. It belongs to another world (like Kea DHCP or certain managed systems). It turns out **clients send their hostname already**, and BIND can accept those updates _if properly configured_. You don’t need to set it in DHCP.

### 🔧 The Fix

Back to basics:

- Removed the bad line from `dhcpd.conf`.
- Restarted `isc-dhcp-server` like a digital defibrillator:
  bash
  CopyEdit
  `sudo systemctl restart isc-dhcp-server`
- Clients rejoined the network. DNS came back. SSH worked. The lab lived again.

We even verified that our DNS zone (`testlab1.local`) had some auto-updating going on — some `A` records were indeed dynamic. (Victory dance omitted but implied.)

### 💡 Lessons Learned

- Don’t blindly copy config lines from the internet. Read the man pages. (_Really._)
- Keep your DHCP and DNS servers on static IPs.
- Use `nixos-rebuild --rollback` liberally. It’s there to save your skin.
- DDNS is cool — but fragile. Start simple and add complexity carefully.

---

## ✅ What’s Next?

After conquering the dragons of DNS and DHCP, I'm off to slay IPv6. Who knows what horrors (or hilarity) lie in wait? One thing’s for sure — `ping6` will become my best friend.

---

Thanks for joining me on this networking odyssey. Stay tuned for more from the lab, where cables are plenty and syntax errors are lurking in every conf file.

_Happy hacking!_
