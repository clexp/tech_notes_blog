+++
title = "Iptables, Ssh And Dns Debugging"
date = "2025-07-09"
description = "It’s been a productive and occasionally nerve-wracking stretch in the lab. This latest chapter of the journey took us deep into the thickets of iptables, VLAN networking, and DNS server configuration ..."
tags = ['dns', 'firewall', 'iptables', 'nat', 'networking', 'security', 'ssh', 'vlan']
categories = ["technical"]
+++

### Adventures in Firewall Rules, VLANs, and DNS: Lessons from the Lab

It’s been a productive and occasionally nerve-wracking stretch in the lab. This latest chapter of the journey took us deep into the thickets of `iptables`, VLAN networking, and DNS server configuration on `rtr02`. Here’s a rundown of what went down, what went wrong, and what we learned.

---

#### 🔒 The SSH Lockout Incident (a.k.a. "Oops")

It started with a perfectly reasonable idea: clean up some `iptables` rules that were cluttering the configuration. The `INPUT` chain had an early rule:

```
1    ACCEPT     tcp  --  0.0.0.0/0  0.0.0.0/0  tcp dpt:22
```

It seemed broad. Maybe too broad? So we deleted it, thinking we had better control via more precise rules elsewhere. Then: _bam!_ SSH from the inside stopped working, and worse, we were locked out of `rtr02`.

**Lesson:** If you’re going to touch `iptables` with a `DROP` default policy, **never delete SSH rules before confirming your new rules work.**

**Fix:** Fortunately, we were still logged in via an existing session, which survived because of the RELATED,ESTABLISHED rule. A quick `iptables -I INPUT 1 -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT` restored access.

---

#### 🧱 Understanding Systemd Quirks: The bind9 Enablement Oddity

Another confusing moment came when trying to enable `bind9` using systemd:

```
sudo systemctl enable bind9
```

This failed with:

```
Failed to enable unit: Refusing to operate on alias name or linked unit file: bind9.service
```

Turns out that `bind9` is an **alias** for the real systemd service name, `named.service`. To avoid confusion:

```
sudo systemctl enable named
```

**Lesson:** When systemctl complains about aliases, it’s usually hinting that you should use the canonical unit name.

---

#### 🌐 DNS is Up, but IPv6 is Loud

With `named` running, we noticed recurring log entries:

```
network unreachable resolving 'ns-1554.awsdns-02.co.uk/AAAA/IN': 2600:9000:...#53
```

These are IPv6 DNS resolution attempts failing. Since this lab is IPv4-only, the IPv6 requests were just noise. No harm done, but worth knowing why they're showing up.

**Lesson:** If you're IPv4-only, you can suppress IPv6 noise by either disabling IPv6 entirely or adjusting `named.conf.options` to prefer IPv4.

---

#### 🔁 Forwarding Rules: Are They Always Necessary?

We spotted this rule in the `FORWARD` chain:

```
5    ACCEPT     tcp  --  0.0.0.0/0  10.0.0.50  tcp dpt:22 state NEW,RELATED,ESTABLISHED
```

This looked overly specific. Do we really need to forward SSH traffic to a test machine? Not unless we’re exposing that host via port forwarding or DMZ-style access. Since routing alone can do the job inside the lab, the rule was removed.

**Lesson:** If all traffic is internal and routes are configured, you may not need explicit FORWARD rules unless you’re restricting by default or want precise control.

---

#### ✅ Takeaways and Habits to Adopt

- **Use `iptables -I` to insert temporary rules** while testing. Save only after confirming stability.
    
- **Always whitelist SSH early** in your rule chain if your default policy is `DROP`.
    
- **Check your current SSH session before deleting rules.** Related sessions stay up thanks to the `ESTABLISHED` rule.
    
- **Use `named` instead of `bind9` with systemctl.**
    
- **Know when you're in a NAT vs routing scenario.** Routing doesn't need DNAT rules unless you're exposing services across boundaries.
    

---

What’s next? We’re turning our attention back to DNS — now that our local resolver is working, dynamic DNS is on the horizon. And maybe a splash of VLAN segregation magic. Until then, keep your SSH ports open and your chains clean.
