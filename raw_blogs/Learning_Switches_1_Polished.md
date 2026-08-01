# The Excitement of a New Switch: Learning Old Commands and New Tricks

Every big adventure begins with a small box. In this case, a box containing a shiny new TP-Link SG3428 switch. You know the type: fingerprint-free, still smelling of factory plastic, and bristling with more gigabit ports than I currently have uses for.

But buying hardware is the easy bit. The real work — and the real fun — begins when you try to talk to it.

## Step 1: Access - Where the Journey Always Begins

Networking gear is like a fortress: lots of doors, but not all of them lead inside. The SG3428 offers four:

- Web management panel (default IP 192.168.0.1)
- SSH
- Telnet
- Serial console

Naturally, I wanted to try them all. Web was easy enough — I gave my laptop a manual IP on 192.168.0.2/24, pinged the switch, and voilà, the panel appeared in my browser.

But I wasn't here for point-and-click. I wanted to learn the CLI.

## Step 2: Telnet - Sounds Easy, Feels Ancient

The docs promised telnet access on port 23. Easy! Or so I thought.

**First attempt (host setup):**
Bluefin (Fedora) doesn't ship with telnet. Immutable distro means no `dnf install`. Solution? Enter toolbox — Fedora's containerised userland — and install telnet there. That worked, but it was a fiddly detour.

```bash
toolbox create --distro fedora --release 42
toolbox enter
sudo dnf install telnet
```

**Error seen if skipped:**

```bash
bash: telnet: command not found
```

**Lesson learned:** Immutable distros require workarounds. Toolbox = "userland sidecar VM."

**Second attempt (actual telnet):**
Inside toolbox:

```bash
telnet 192.168.0.1
```

Prompt appears, I log in with admin, and we're in!

## Step 3: CLI Expectations vs CLI Reality

Coming from a Cisco/Unix background, I expected familiar commands. My fingers reflexively typed:

```bash
show version
```

Only to be rewarded with:

```
                   ^
% Unrecognized command found at '^' position.
```

Hmm. Not Cisco, then.

So I tried:

```bash
configure terminal
```

Nope.

```bash
write memory
```

Nope.

```bash
show interface counters
```

Nope.

**What I learned the hard way:** TP-Link's SMB CLI is similar-ish, but not IOS. Commands are different, and some features (like counters) use their own syntax.

## Step 4: Commands That Did Work

After some reading and trial-and-error, a few gems emerged:

**System info:**

```bash
enable
show system-info
```

→ Hardware, firmware version, uptime.

**Config inspection:**

```bash
show running-config
show startup-config
```

→ What's active vs what loads on boot.

**VLANs:**

```bash
show vlan
```

→ Confirmed VLAN 1 is the only one present (the "system-vlan").

**Interfaces (status):**

```bash
show interface status
```

→ Current state of ports (up/down).

## Step 5: Security Musings Along the Way

One thought stuck with me: telnet passwords are clear text. My password is long (29 characters, mixed case + symbols), but without rate limiting, someone could brute force indefinitely.

So the plan is clear:

- Use telnet only for learning (short-lived)
- Long term: disable telnet
- Management will shift to HTTPS and SSH

## Lessons Learned So Far

1. **Immutable distros bite** — toolbox saved me, but added friction
2. **Not all CLIs are Cisco** — you can't just muscle memory your way through
3. **Backspace is weird** — in telnet, it requires arrow left then delete
4. **VLAN 1 is default** — secure management requires more than defaults

## Conclusion: Just the Beginning

This was only the first chapter. I now have access via web, telnet, and serial (sort of). Each comes with quirks and trade-offs.

Next up: the serial console — where 1990s COM ports still reign, and where I learned why running screen over SSH is a recipe for lag and frustration.

✅ That's the first blog post draft. It tells a chronological story of discovery, with commands, errors, outputs, and lessons.


