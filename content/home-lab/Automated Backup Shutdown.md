+++
title = "Automated Backup Shutdown"
date = "2025-07-09"
description = "In the quiet hum of my home lab, nestled between an Ubuntu main server (nas04) and a FreeBSD backup box (bub03), I decided to embrace full automation: nightly ZFS snapshots using sanoid and incrementa..."
tags = ['architecture', 'backup', 'bsd', 'freebsd', 'linux', 'nat', 'networking', 'security', 'ssh', 'storage', 'tutorial', 'ubuntu', 'unix']
categories = ["technical"]
+++

## Backup, Shutdown, and a Wake-Up Call: A Home Lab Tale

### Prelude: Ambitions in Automation

In the quiet hum of my home lab, nestled between an Ubuntu main server (`nas04`) and a FreeBSD backup box (`bub03`), I decided to embrace full automation: nightly ZFS snapshots using `sanoid` and incremental replication via `syncoid`, followed by an automatic shutdown of the backup box to conserve power. It seemed simple: a cron job, a backup, and a polite power-off.

But, like all good engineering stories, this one quickly detoured into a lesson-packed journey through permissions, cron behavior, filesystem states, and the nuances of safe automation.

---

### The Setup

- **Primary server:** `nas04` (Ubuntu) — hosts the live data on various ZFS datasets like `reflect/Pictures`, `reflect/paperless`, etc.
    
- **Backup target:** `bub03` (FreeBSD) — a ZFS mirror, set to receive replicated snapshots.
    
- **Networking:** `nas04` connects to `bub03` over a private interface (192.168.177.0/24).
    
- **Access:** Passwordless SSH from `nas04` (user `infra`) to `bub03`.
    

The goal: Have `bub03` wake up on LAN, receive ZFS snapshots, and then power down once the job is done.

---

### Phase 1: Getting Syncoid Working

We began by testing the raw `syncoid` command from `bub03`, pulling snapshots from `nas04`. Here's a working example:

```sh
/usr/local/bin/syncoid --recursive --no-privilege-elevation nas04:reflect/paperless backup/paperless
```

Once verified, we wrapped all dataset syncs into a single backup script, which also logged output and executed a `shutdown -p now` at the end.

To test it regularly, we used:

```sh
crontab -e
```

With an entry like:

```cron
*/1 * * * * /home/infra/bin/nightly-backup.sh >> /tmp/nightly-syncoid.log 2>&1
```

---

### Phase 2: Ownership and Permissions

Initially, `root` owned the script. But the cron job runs as `infra`, so we:

```sh
chown infra:infra /home/infra/bin/nightly-backup.sh
chmod +x /home/infra/bin/nightly-backup.sh
```

Once that was set, logs showed the script executing cleanly, backups syncing, and then...

```sh
Shutdown now!
```

And we got booted off! Success? Sort of.

---

### Phase 3: A Shutdown Too Far

The problem was subtle but serious: any time we rebooted or powered up `bub03`, it would shut itself down within a minute, before we could intervene.

**Why?** The cron job was active and firing on boot.

**Fix attempt:** Boot into single-user mode (FreeBSD bootloader > option 2).

But then:

```sh
crontab -e
## Error: filesystem is read-only
```

### Making the Filesystem Writable

To fix this, we needed to remount the root filesystem as read-write:

```sh
mount -u /
mount -a
```

Then we could safely edit `infra`'s crontab:

```sh
crontab -e -u infra
## Comment out the job
## */1 * * * * /home/infra/bin/nightly-backup.sh
```

Alternatively:

```sh
vi /var/cron/tabs/infra
```

---

### Phase 4: Making Automation Safe

To prevent this boot-loop behavior in the future, we added a **shutdown override lock file** check to the script:

```bash
if [ -f /tmp/skip_shutdown ]; then
  echo "Shutdown skipped by override" >> "$LOGFILE"
  exit 0
fi
```

Then, from a terminal, we can easily cancel the shutdown:

```sh
touch /tmp/skip_shutdown
```

We also added a `wall` broadcast before shutdown:

```sh
wall "System shutting down in 5 minutes. Create /tmp/skip_shutdown to abort."
sleep 300
```

### Final Script Snippet

```bash
#!/bin/sh
LOGFILE="/tmp/nightly-syncoid.log"
echo "Backup run started: $(date)" >> "$LOGFILE"

## Sync datasets...
/usr/local/bin/syncoid ...

if [ -f /tmp/skip_shutdown ]; then
  echo "Shutdown skipped by override" >> "$LOGFILE"
  exit 0
fi

wall "System shutting down in 5 minutes. Create /tmp/skip_shutdown to abort."
sleep 300
shutdown -p now
```

---

### Learnings Along the Way

- **`cron` runs in minimal environments.** Make sure scripts have full paths and expected environment.
    
- **Ownership matters.** If a script is owned by another user, `cron` may fail silently.
    
- **Filesystem state in single-user mode defaults to read-only.** Use `mount -u /` to fix.
    
- **Preventing irreversible automation is key.** Build in override controls for safety.
    

---

### Epilogue

Today, `bub03` wakes on LAN, receives its snapshots, then waits a polite 5 minutes before going back to sleep — unless told otherwise. Cron runs like clockwork, logs are clear, and the system respects a simple file as a veto.

Backup isn’t just about copying data. It's about designing resilience — for systems _and_ for sysadmins who might just need one more minute to fix something.
