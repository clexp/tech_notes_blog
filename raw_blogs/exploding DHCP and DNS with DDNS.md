# 🧠 The Day My DNS Died (and Took My Network With It): A Sysadmin Lab Chronicle

*May 2025 — Somewhere between coffee and chaos.*

So there I was, deep in the bowels of my home lab, configuring `BIND9` for local DNS and `ISC DHCP Server` for dynamic IP leases. Everything was going fine — too fine. My router (`rtr02`) was humming along, clients were getting IPs, DNS lookups worked... even reverse lookups were starting to take shape.

But I wanted *more*. I wanted **Dynamic DNS (DDNS)**, that mythical beast where DHCP clients register themselves in the DNS zone, auto-magically keeping hostnames and IPs in sync.

## 🧨 Enter: The Line That Killed Everything

Somewhere in my `dhcpd.conf`, I dropped in this innocent-looking line:

```dhcpd
option host-name = config-option host-name;
