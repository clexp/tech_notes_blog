# A Samba Odyssey: Scanning, Containers, and a Printer's Long Journey Home

In the quiet hum of a home lab, a printer stood alone. It could print. It could fax. It could even scan. But could it scan directly to a shared network folder and trigger automated document processing? That was the dream. This is the tale of how we made it happen—using Samba, Linux containers, a fair bit of debugging, and a lot of learning along the way.

## The Goal: Scan to Samba, Feed to Paperless

The mission was clear: scan documents on an HP OfficeJet 8620 network printer and deposit them into a shared Samba folder, where they would be picked up and processed by [Paperless-ngx](https://paperless-ngx.readthedocs.io/en/latest/). The catch? The share needed to support the ancient SMB1 (NT1) protocol, and we didn't want to weaken the entire Samba server just to support one outdated client.

## Architecture Recap

- **Host**: Ubuntu server (`nas04`) running Docker containers including `paperless-ngx`, `pihole`, and others.
    
- **Network**:
    
    - Main LAN: `192.168.178.0/24`
        
    - Test subnet: `192.168.177.0/24`
        
- **Printer**: HP OfficeJet 8620 (networked on `192.168.178.11`)
    
- **Samba Share**: `/pprls_ibx` on host, owned by `infra`, used as an inbox for scanned documents.
    
- **Challenge**: The printer only spoke **SMB1**, which was no longer enabled on the host's Samba instance.
    

## Problem 1: When SMB1 Is the Only Option

We couldn't enable SMB1 on the main Samba server without weakening security for all clients. The solution? Spin up a **dedicated Samba server inside a systemd-nspawn container**, isolated and constrained to just this function.

## Step 1: Bootstrapping the Container

We used `debootstrap` to build a minimal Debian container:

```bash
sudo debootstrap stable /var/lib/machines/samba-nt1 https://deb.debian.org/debian
```

Then we installed `systemd-container` to use `machinectl` and `systemd-nspawn`:

```bash
sudo apt install systemd-container
```

Launching the container:

```bash
sudo systemd-nspawn -D /var/lib/machines/samba-nt1 --machine=samba-nt1 --network-bridge=br0 -b
```

> Pro tip: Don't close your SSH session while running this interactively unless you want the container to die with it.

## Step 2: Networking Woes

At first, our container had no network access. No DHCP, no DNS, no connectivity. The `host0` interface was down. We brought it up manually:

```bash
ip link set host0 up
dhclient host0
```

Symptoms of failure:

- `ping` to any external address failed.
    
- `dig` and `curl` showed DNS resolution issues.
    

Confirmed working once:

```bash
ping -c 2 1.1.1.1
```

## Step 3: Firewall Frustrations

A quick look at iptables showed the likely culprit:

```bash
sudo iptables -L -n
```

We had a **DROP policy** on the FORWARD chain and INPUT chain.

Fix: Explicitly allow bridged traffic from the container's subnet or host0 interface, or relax input restrictions for internal traffic. Also ensure the interface is actually part of a bridge:

```bash
ip link set enp3s0 promisc on
```

## Step 4: UID Mapping and the Samba User

We passed the host directory `/pprls_ibx` into the container and matched the user `infra` inside the container to UID 1004 (same as on the host):

```bash
groupadd -g 1004 infra
useradd -u 1004 -g 1004 -M -s /usr/sbin/nologin infra
smbpasswd -a infra
```

No need to create a separate `scanner_user` as long as the UID matches.

The Samba config inside the container looked like:

```ini
[pprls_ibx]
   path = /srv/pprls_ibx
   browseable = yes
   writable = yes
   guest ok = no
   valid users = infra
   create mask = 0660
   directory mask = 0770
```

## Step 5: Printer Panel Configuration

On the HP web panel:

- Address: `\\192.168.178.84\pprls_ibx`
    
- Username: `infra`
    
- Password: (what we set via `smbpasswd` in container)
    

We went from **"Cannot connect"** to **"Incorrect credentials"**, and finally to **"Connection successful"**.

## Step 6: Success!

With network sorted, UID mapping matched, and credentials working, we had a dedicated Samba server running SMB1, isolated to its own container, with write access to a shared folder consumed by Paperless-ngx.

## Reflections

- `systemd-nspawn` proved ideal for this tight use case: isolation, control, performance.
    
- Bridged networking enabled full LAN access for the container.
    
- SMB1 is a legacy protocol, but when hardware demands it, isolation can balance security and functionality.
    
- UID consistency across host and container is key for shared filesystem use.
    
- Debugging is easier with `ping`, `dig`, `curl`, and watching logs (`journalctl -xe`, `tail -f /var/log/samba/log.smbd`).
    

## Next Steps

- Add container to `systemd` for persistent boot.
    
- Monitor `/pprls_ibx` for anomalies.
    
- Auto-rotate printer credentials, if possible.
    
- Replace SMB1-capable printer eventually.
    

## In Closing

This wasn’t just about scanning documents. It was a deep dive into Samba behavior, UID mapping, container networking, and practical security boundaries. And somewhere in there, a humble OfficeJet 8620 got to shine again—if only for a while.

Until next scan...