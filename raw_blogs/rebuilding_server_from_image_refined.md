# When Backups Bite Back: The Tale of Config Salvage vs. Image Import in FreeBSD

There are two kinds of sysadmin war stories: the ones where you do something clever, and the ones where you try to do something clever and end up learning why the boring way is usually best. This is one of the latter.

## What We Were Trying to Achieve

The goal was straightforward: restore a server environment quickly without rebuilding everything from scratch. I had a FreeBSD system with years of customizations—jails, WireGuard tunnels, pf firewall rules, and bhyve VMs—and I wanted to preserve that configuration on a new, smaller NVMe drive.

## The Architecture

The stage was set with a modest homelab setup:

- **tb02**: A FreeBSD host with an NVMe drive (nda0) and ZFS root pool `zroot`
- **Backup drive**: A spinning rust drive (ada1) holding a compressed `.img.gz` of the older system
- **Rescue tools**: A USB stick with FreeBSD installer for emergency access

The challenge? The old system image was ~240GB, but the new NVMe was smaller. I needed to either extract just the configurations or shrink the entire image to fit.

## The Discovery Process: Strategy One - Config Extraction

### Mounting the Past

First, we needed to peek inside the old SSD image. The process started with importing the old ZFS pool:

```bash
zpool import -f -o readonly=on -R /mnt/oldroot 9888157219862902893 oldroot
zfs mount oldroot/ROOT/default
```

**Initial symptoms**: At first, `/mnt/oldroot/etc` didn't exist, which was puzzling. The clue came when I realized the dataset `ROOT/default` wasn't mounted.

**The fix**: Explicitly mounting the default root dataset revealed the filesystem structure.

**Lesson learned**: In ZFS, your "root" may not be the pool itself—you need to look for the `ROOT/default` dataset.

### Cherry-Picking Configurations

We wanted to extract configs, not whole jails or VM images. The tool of choice was `cp -av` to a staging area:

```bash
mkdir -p /zroot/staging/oldroot-configs/{etc,usr_local_etc,usr_local_vm,usr_jails}

cp -av /mnt/oldroot/etc/rc.conf /zroot/staging/oldroot-configs/etc/
cp -av /mnt/oldroot/etc/pf.conf /zroot/staging/oldroot-configs/etc/
cp -av /mnt/oldroot/usr/local/etc/wireguard /zroot/staging/oldroot-configs/usr_local_etc/
cp -av /mnt/oldroot/usr/local/vm/*.conf /zroot/staging/oldroot-configs/usr_local_vm/
```

**Unexpected discovery**: We saw hundreds of files fly by from `/usr/jails/nginx/bin`—wait, did we just copy a whole base system?!

**The realization**: Jails look like mini-systems. Copying them brings in `/bin` and `/lib`, not just configs. "Config-only" for jails requires more careful pruning.

### Comparing Old vs. New

How different was the old system from the new? `diff -u` to the rescue:

```bash
diff -u /etc/rc.conf /zroot/staging/oldroot-configs/etc/rc.conf
```

**Example output**:

```
-ntpd_enable="YES"
-ntpd_sync_on_start="YES"
+pf_enable="YES"
+wireguard_enable="YES"
+vm_enable="YES"
```

**What this told us**: The new install had NTP enabled; the old system had PF firewall, WireGuard, and bhyve VMs enabled. Each `-` meant "new had it, old didn't"; each `+` meant "old had it, new didn't."

**Tools mastered**:

- `diff -u file1 file2` → see precise line-by-line differences
- `cp -av` → copy with attributes, see exactly what moves
- `zpool import -R /mnt/foo` → mount old pools read-only for safety

## The Discovery Process: Strategy Two - Image Import

But my tinkerer's brain wasn't satisfied. I wanted to resurrect the whole system image.

### Attaching the Image

The `.img` was written to the spinner (ada1p1). To examine it, I used `mdconfig` to attach it as a memory device:

```bash
mdconfig -a -t vnode -f /spinner/seeed-ssd-expanded.img -u 0
gpart show md0
```

**Output confirmed the expected partitions**:

- efi
- freebsd-boot
- freebsd-swap
- freebsd-zfs (md0p4)

So far, so good. Next step: import the ZFS pool.

```bash
zpool import -d /dev
```

This showed the pool metadata with the name `oldroot`. But attempts to mount it went sideways:

```bash
zpool import -o readonly=on -R /mnt oldroot zroot
# -> "pool was previously in use…"

# Or worse:
zpool import -o readonly=on -R /mnt md0p4 oldroot
# -> "no such pool available"
```

### Debugging with zdb

To confirm I wasn't hallucinating, I used:

```bash
zdb -l /dev/md0p4
```

**That spit out metadata**:

```
name: 'oldroot'
hostname: 'tb02'
pool_guid: 9888157219862902893
```

So the data was there, but ZFS just didn't want to cooperate.

### Symptoms and Theories

**Symptom**: `zpool import` said "no such pool" even when `zdb` saw it.
**Theory**: Maybe it was already imported under a different name.

**Symptom**: Mountpoints were empty (`ls /mnt/zroot/etc` → "no such file or directory").
**Theory**: Default datasets had `mountpoint=none` or weren't auto-mounted.

**Symptom**: Setting a new mountpoint failed with "read-only."
**Theory**: Importing with `-o readonly=on` prevented changes.

## The Professional Pivot

In the end, I had to decide: Was I trying to be clever, or was I trying to get the service running?

**What we learned**:

- ZFS loves replication streams, not `.img` acrobatics. The professional way to migrate pools is `zfs send | zfs recv`, not juggling images inside images.
- ZFS can see pools in `.img` files… but only if you get the import flags exactly right. It's possible, but fussy, especially in single-user mode.
- Config salvage is underrated. Copying `/etc`, `pf.conf`, jail configs, and VM definitions gave me 90% of the rebuild for 10% of the effort.

## The Moral of the Story

Copying configs and rebuilding services turned out to be the professional move. Importing from the `.img` was fascinating, educational, and blog-worthy—but not the fastest route to a working system.

**Professional takeaway**: Professionalism isn't about never failing—it's about knowing when to pivot.

This process felt like unpacking boxes after moving house. I just wanted the Wi-Fi password and router config, but somehow ended up with a toaster and three kettles from the old kitchen.

## Commands Cheat Sheet

**Attach image as device**:

```bash
mdconfig -a -t vnode -f image.img -u 0
```

**Inspect partitions**:

```bash
gpart show md0
```

**List ZFS pools**:

```bash
zpool import -d /dev
```

**Check metadata**:

```bash
zdb -l /dev/md0p4
```

**Copy configs**:

```bash
cp -av /mnt/oldroot/etc/rc.conf /zroot/staging/etc/
```

**Diff configs**:

```bash
diff -u /etc/rc.conf /zroot/staging/etc/rc.conf
```

**Result**: Configs salvaged, system rebuilt, lesson learned. Next time: maybe a cleaner pipeline with `zfs send` instead of `.img` gymnastics.
