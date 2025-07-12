+++
title = "Zero To OpenBSD VPS Hero"
date = "2025-07-09"
description = "In this post, we walk through the first stages of setting up a secure OpenBSD VPS — from purchase to shell prompt, from confusion to clarity. It's not just about typing commands; it’s about learning h..."
tags = ['apache', 'architecture', 'bsd', 'cloud', 'dns', 'firewall', 'freebsd', 'hosting', 'nat', 'networking', 'nginx', 'openbsd', 'security', 'ssh', 'tunnel', 'unix', 'vpn', 'vps', 'web-server', 'wireguard']
categories = ["technical"]
+++

# From Zero to VPS Hero: A Journey into OpenBSD, SSH, and Console Zen

In this post, we walk through the first stages of setting up a secure OpenBSD VPS — from purchase to shell prompt, from confusion to clarity. It's not just about typing commands; it’s about learning how the pieces fit together. If you're looking to deepen your understanding of Unix-y systems and networking, come along for the ride.

## 🚀 The Goal

Set up a publicly-accessible VPS running OpenBSD. This server will act as an access point and potential reverse proxy for a machine living behind double NAT — hosting a static Zola blog and a Django site. The longer-term aim is to build a tunnel (WireGuard), expose websites via HTTPS, and learn how TLS, DNS, and web servers integrate across a distributed architecture.

## 🧱 The Architecture

The basic layout we’re working toward:

```
Internet
   |
OpenBSD VPS (46.23.95.221)  <- Exposes domains, TLS termination
   |
   | (tunnel or proxy)
   |
FreeBSD box behind double NAT
  |- nginx serves Zola static site
  |- apache serves Django site
```

## 🛒 Step 1: Ordering the VPS

We went with [openbsd.amsterdam](https://openbsd.amsterdam/) — a community-focused VPS host running OpenBSD VMs on OpenBSD hypervisors.

Details we needed:

- **Hostname**: cl_vps_01 (cattle, not pets)
- **Username**: `clexp`
- **SSH key**: Generated a fresh Ed25519 key pair using `ssh-keygen`, stored private key in Bitwarden

### SSH Key Generation:

```sh
ssh-keygen -t ed25519 -f ~/.ssh/cl_vps_01 -C "clexp@cl_vps_01"
```

### Uploading to ssh-agent:

```sh
ssh-add ~/.ssh/cl_vps_01
```

Check:

```sh
ssh-add -l
```

## 🔐 Logging In

After the welcome email arrived (including public IP, user, and port for host console), we connected:

```sh
ssh -i ~/.ssh/cl_vps_01 clexp@46.23.95.221
```

That’s to the VM itself. But there’s a bonus: you can also SSH to the physical host machine (with a port like `-p 3022`) and attach to your VM’s console:

```sh
ssh -p 3022 clexp@server26.openbsd.amsterdam
vmctl console vm18
```

### Console Exit:

Use `~.` to exit the console. It took us a bit to discover this — the login prompt was confusing, and exiting a hung shell required terminating the terminal tab.

## 🔐 Securing the Server (Part 1)

We locked down the system in a few key ways:

### ✅ Add to `doas`

```sh
echo "permit persist clexp as root" | sudo tee -a /etc/doas.conf
```

### ✅ Disable Password Auth

Even though our key had a passphrase, we chose to disable password login:

```sh
# In /etc/ssh/sshd_config:
PasswordAuthentication no
```

Then reload:

```sh
rcctl restart sshd
```

> 🔒 Note: Always test in a second SSH session before restarting `sshd`! A typo here can lock you out.

### ✅ Apply Patches

```sh
syspatch
```

This brings the system up to date with the latest errata.

## 🛠️ Console Power

Once in the host via:

```sh
ssh -p XXXX clexp@server26.openbsd.amsterdam
```

You can run:

```sh
vmctl console vm18
```

This drops you into the live terminal of the VM. If networking or firewall rules go sideways, this console is your parachute. Detach with `~.`.

## 🧯 Coming Next: PF Firewall

Before we dive into exposing services or tunneling back to the FreeBSD box, we’ll set up `pf` (the OpenBSD packet filter) to:

- Allow SSH in
- Allow DNS, HTTP/HTTPS out
- Drop all else

We’ll build that config incrementally, test it in a dry run, and always keep console access as a failsafe.

## 🌍 Domain Planning

We’re looking at Gandi or Namecheap for a domain registrar. We’ll:

- Purchase a domain
- Point `A` (IPv4) and `AAAA` (IPv6) records to the VPS
- Eventually, serve HTTPS using Let’s Encrypt

But before that, we’ll explore the magic of TLS, certificates, reverse proxies, and maybe even Caddy or Traefik.

## 🎉 Conclusion

In a single session, we’ve:

- Acquired and accessed a public VPS
- Verified SSH key auth with ssh-agent
- Entered the VM and its host
- Learned how to use `vmctl` console and exit safely
- Locked down the system and applied patches

We now have a solid, secure base to build from. Next up: firewalls, tunnels, proxies, and TLS.

Stay tuned.
