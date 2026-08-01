# The Four Doors: Web, Serial, Telnet, and SSH Access to Your Switch

There are two kinds of network gear users: those who think "I'll just use the web GUI" and those who immediately reach for a serial cable. I'm learning to be a messy hybrid — I want the convenience of a browser and the precision of a CLI, plus the confidence that I can always reach the hardware even if the network breaks.

A managed switch like the TP-Link SG3428 gives you four ways in: web, serial, telnet, and SSH. Here's how I tried them, what worked, and the gotchas I'd warn you about.

## 1) Web Management (GUI) — The Comfy Door

**What it is:** HTTP/HTTPS web UI served by the switch at its management IP (default on this model: 192.168.0.1).

**How I used it:** Set my laptop to 192.168.0.2/24, opened a browser and logged in with the default admin account.

**Why use it:** Very visual — quick to check port LED status, VLAN lists, firmware, and make basic changes. Good for one-off edits and for users uncomfortable with CLI.

**Commands / Steps:**

- Assign laptop IP on same subnet:

```bash
sudo ip addr add 192.168.0.2/24 dev enp0s13f0u2
```

- Browse to: `https://192.168.0.1` (expect a self-signed cert warning)
- Turn off HTTP; enable HTTPS/TLS1.2 in the Security → Web settings

**Gotchas:**

- Self-signed certificate warnings (normal). Either accept in your browser for lab use, or upload a cert signed by your CA
- Many web UIs let you change everything instantly — but they can also hide defaults that are insecure (e.g., telnet enabled by default)

**Security quick wins (do these ASAP after first login):**

- Change the default password to a long, unique passphrase
- Disable HTTP (leave HTTPS w/ TLS1.2) and install a proper certificate if possible
- Restrict management to a management VLAN or specific source IP subnets if the UI supports it

## 2) Serial (Console) — The Lifeline

**What it is:** A direct hardware console. On the SG3428 you have an RJ45 console port and a USB-B serial console. Serial works even if the switch's networking is broken — it's the lifeline for real recovery.

**Why use it:** Ultimate reliability — you can always access the device from a machine with a serial port (or USB-serial adapter), and it gives you the freshest console output (boot messages, crash logs).

**Hardware & cable notes:**

- The switch came with an RJ45→DB9 console cable. Verify the cable pinout matches the switch vendor cable (if it's the cable included with the box, you're usually OK). TP-Link uses common console wiring but double-check
- If you plug into a motherboard COM port (not USB), use `/dev/ttyS0` (Linux); USB adapters appear as `/dev/ttyUSB0`
- Typical serial settings for SG3428: 38400 8N1 (38400 baud, 8 data bits, no parity, 1 stop bit)

**Linux examples:**

- Direct on the host:

```bash
sudo screen /dev/ttyS0 38400
# or
sudo picocom -b 38400 /dev/ttyS0
```

- If you want remote access to the serial console (recommended for convenience & to avoid SSH->screen lag): run ser2net on the machine that the serial cable is physically attached to (your NAS/server) then tunnel it securely:
  1. On NAS (bind to localhost!): configure ser2net to expose `/dev/ttyS0` on local TCP port 2000
  2. From remote client: `ssh -L 2000:localhost:2000 infra@nas04` then `telnet localhost 2000`

**Common problems & fixes:**

- Screen over SSH is laggy / drops characters: this is exactly what I hit. SSH wraps the terminal and can introduce buffering/line discipline issues. That's why ser2net + SSH tunnel (raw TCP serial) is the nicer approach
- No backspace behavior: some consoles require arrow-left then backspace or need terminal settings fixed. If backspace is weird, type slowly, or use a terminal program that maps delete/backspace correctly

## 3) Telnet — The Beginner's CLI (But Insecure)

**What it is:** Telnet is a TCP protocol (port 23) that offers CLI access — but it sends credentials in the clear.

**How I used it:** `toolbox→telnet→telnet 192.168.0.1` and used the CLI over the LAN. It works, and it's convenient — fast to start and identical to serial CLI in many respects.

**Commands to try:**

```bash
enable                    # most sessions require privileged mode
show running-config      # what's active
show startup-config      # what loads on boot
show vlan               # VLAN configuration
show interface status    # port states
```

**Why not to rely on it:** Telnet is plaintext, so on an untrusted network it leaks credentials. Even on a home LAN: don't expose port 23 unnecessarily.

**Temporary safe use:** Use telnet only when isolated (your lab), then disable telnet once you're done learning:

- From web UI or CLI → turn off telnet, keep SSH and HTTPS enabled

**Security notes:**

- Telnet has no built-in brute-force protections typically. A long password helps but doesn't solve the fundamental lack of encryption
- If you must leave telnet enabled for automation in a totally isolated lab, consider adding ACLs in the switch to only allow your laptop's IP (or management VLAN) to reach it

## 4) SSH — The Modern Secure Door (Recommended)

**What it is:** Secure encrypted CLI access (use SSH v2 only).

**Why use it:** Encrypted, supports keys, safer to expose to a management network. In my setup, SSH was fast and responsive (unlike serial over SSH), so it's my preferred interactive CLI.

**Steps:**

- Enable SSH in the web UI / CLI and configure to accept only protocol v2
- If supported, add SSH keys for passwordless or key-based logins:

```bash
ssh admin@192.168.0.1
```

- Configure enable authentication / line ssh settings if you want privileged auth control (see manual)

**Gotchas:**

- Some switches still accept SSH v1 if you don't explicitly disable it — make sure only v2 is allowed
- If telnet is enabled and SSH is not locked down, attackers could use telnet to attempt privilege escalations (use SSH + disable telnet)

## Management Access: Practical Security Checklist

Use this checklist after exploring:

- Change the default admin password to a secure long passphrase
- Create a lower-privilege observer user for monitoring (useful later for Nagios/Prometheus checks)
- Disable HTTP completely; enable only HTTPS + TLS1.2. Disable SSLv3
- Enable SSH (protocol v2 only). Add SSH keys if possible
- Disable Telnet after you finish practicing. If you must use it temporarily, restrict it by IP via an ACL or a management VLAN
- Limit remote management (remote web access, SNMP, etc.) to a specific management VLAN or specific source addresses
- If available, enable login rate limits or integrate with RADIUS for AAA. If you can, use AAA to centralize auth/authorization
- Back up config after you reach a good state (`copy running-config startup-config`)

## Can an Attacker Guess a Management IP and Get In?

**Short answer:** Yes — if your management runs on VLAN1 and VLAN1 is reachable from devices an attacker can access, guessing/scanning IPs could discover the management address. That's why:

- Put management on a dedicated VLAN that normal hosts and guests can't reach
- Restrict management access by ACLs or by only binding management services to selected interfaces
- Disable management on default VLAN1 where possible

## Quick Troubleshooting Notes (From My Live Lab)

- If `screen /dev/ttyS0 38400` works on the head but is terribly laggy over SSH, don't fight it — use ser2net on the server and tunnel to it. That gives you the responsiveness of direct serial without being physically at the rack
- On immutable Linux hosts (Fedora Silverblue/Bluefin): don't try to install telnet onto the host. Use toolbox, or install host packages with rpm-ostree when you must. Toolbox is great for ephemeral testing but you must configure the host network to let toolbox see the management subnet reliably

## Small Cheat Commands (Copy-Paste While You Explore)

Use these while you're in a telnet / serial / SSH session with the switch (TP-Link syntax):

```bash
enable
show system-info
show running-config
show startup-config
show vlan
show interface status
show mac-address-table
configure
 interface gigabitEthernet 1/0/1
  description Uplink
  switchport access vlan 10
 exit
copy running-config startup-config
```

## Closing: How I'll Write This Up

For the blog I plan three short posts:

1. **Unboxing + first-touch** — web UI, first firmware check, and quick secure hardening
2. **Access: the four doors** — this post (serial, telnet, ssh, web) — what worked, what failed, and how I secured things
3. **Serial deep dive** — how I got ser2net working, why screen over SSH is a no-go, and how to reliably manage from a remote laptop

Each post will be chronological, with command snippets, the errors I hit and why they happened, and clearly labeled screenshots where they help the narrative.


