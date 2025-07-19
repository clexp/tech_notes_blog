+++
title = "LXC Samba container disappearance"
date = "2025-07-09"
description = "In our home lab, one trusty multifunction printer dutifully scans documents to a Samba share. That share feeds directly into Paperless-ngx, which processes and organizes them for easy, searchable arch..."
tags = ['architecture', 'debugging', 'dhcp', 'file-sharing', 'networking', 'samba', 'troubleshooting', 'tutorial']
categories = ["technical"]
+++

## Samba NT1 Container Debugging: A Journey Through Networking Mysteries

## The Mission: Scan to Paperless, Samba Style

In our home lab, one trusty multifunction printer dutifully scans documents to a Samba share. That share feeds directly into Paperless-ngx, which processes and organizes them for easy, searchable archiving. The architecture is minimal yet functional — a scanner on the LAN, a Samba container providing a network share, and Paperless-ngx picking up scans from a bind-mounted inbox.

Our Samba server lives in a systemd-nspawn container named `samba-nt1` on the host `nas04`, bridged to the home LAN using `br0`. The container runs Debian 12 and is deliberately using the NT1 protocol — an older dialect that remains compatible with legacy scanning hardware.

## A Mysterious Disappearance

Everything was working — until it wasn’t. One day, we found no scans in Paperless. The Samba share wasn’t reachable. First theory: the container wasn't running. But `machinectl` showed it was up.

So the next suspect: networking. Did the container lose its IP?

```bash
$ machinectl status samba-nt1
```

No IP address listed. Aha.

## A Theory Emerges: Was It Ever Really Assigned?

We remembered that `systemd-nspawn` can attach containers to the network using either a veth pair or a bridge, and may hand off the container’s interface to DHCP — if everything aligns.

But what was actually configured?

```bash
$ cat /etc/systemd/nspawn/samba-nt1.nspawn
```

We found only this:

```ini
[Exec]
Boot=yes

[Files]
Bind=/pprls_ibx:/srv/scanner_inbox
```

No `[Network]` section. So it wasn’t explicitly bridged. This suggested it may have previously received a lease via implicit veth bridging and DHCP — a fragile, ephemeral setup.

## Bridging the Gap (Literally)

We decided to explicitly bridge the container to the host’s main bridge, `br0`, where all the action happens:

```ini
[Network]
Bridge=br0
```

Added to `/etc/systemd/nspawn/samba-nt1.nspawn`.

To apply the change:

```bash
$ sudo machinectl poweroff samba-nt1
$ sudo machinectl start samba-nt1
```

Now we check again:

```bash
$ machinectl status samba-nt1
```

Victory! An IP address: `192.168.178.84`.

We confirmed reachability:

```bash
$ ping 192.168.178.84
```

Success. No packet loss. The container was back online.

## The Curious Case of the Missing Network Config

Inside the container, we checked the network config:

```bash
$ sudo ls /var/lib/machines/samba-nt1/etc/systemd/network/
```

Empty. So `systemd-networkd` wasn't managing the interfaces. But digging into `machinectl status` showed:

```bash
networking.service
├─ dhclient -4 -v -i -pf /run/dhclient.host0.pid ...
```

The container was running `dhclient` via Debian’s classic `networking.service`, and that was assigning an IP dynamically.

This was a useful clue: no `*.network` file was necessary in this case because DHCP was being handled the old-fashioned way.

## Confirming Samba’s Return

The final test: did the scanner find the Samba share?

We watched the bind-mounted inbox:

```bash
$ ls /pprls_ibx
```

New files! Paperless picked them up. Our inbox was alive again.

## Lessons from the Edge

This wasn’t just a fix — it was a learning experience in how `systemd-nspawn`, bridging, DHCP, and classic networking scripts interact.

**Takeaways:**

- `systemd-nspawn` will provide basic networking by default, but it’s best to be explicit.
- Bridging to `br0` gives the container a proper place on your LAN.
- Use `machinectl status <name>` to quickly view IPs and confirm running state.
- `dhclient` inside the container can work fine, even without systemd-networkd.

And maybe, just maybe, older protocols like NT1 still have a place — at least until every scanner catches up to 2025.

Boom. We did it.
