Got it — we’ll split this into two tracks:

1. Draft Blog Post: “Config Rescue Mission – Salvaging a FreeBSD System the Gentle Way”

When you run servers at home, you get to wear a lot of hats: sysadmin, disaster-recovery engineer, forensic analyst, sometimes even archaeologist digging through the strata of old configs.

This is the tale of how I tried to salvage my old FreeBSD system, not by restoring the whole beast, but by delicately extracting its brain — the config files — and grafting them onto a fresh install.

⸻

Background – What Were We Even Trying to Do?

The home setup has a few moving parts:
• tb02: a FreeBSD box with ZFS and a history of experiments.
• Oldroot: an SSD pool that had once been the system’s root.
• New NVMe: a shiny new, but smaller, drive that I want to move forward with.
• Network: a flat LAN with jails, bhyve VMs, and a WireGuard tunnel or two.

The goal? Bring over the essence of the old system (configs, services, customizations) without dragging along years of cruft.

⸻

Step One – Mounting the Past

First, we needed to peek inside the old SSD image:

zpool import -f -o readonly=on -R /mnt/oldroot 9888157219862902893 oldroot
zfs mount oldroot/ROOT/default

Symptoms:
• At first, /mnt/oldroot/etc didn’t exist.
• A clue: the dataset ROOT/default wasn’t mounted.
• Fix: explicitly zfs mount the default root dataset.

Lesson: in ZFS, your “root” may not be the pool itself — look for the ROOT/default dataset.

⸻

Step Two – Staging Configs

We wanted to cherry-pick configs, not whole jails or VM images. The tool of choice: cp -av to a staging area.

mkdir -p /zroot/staging/oldroot-configs/{etc,usr_local_etc,usr_local_vm,usr_jails}

cp -av /mnt/oldroot/etc/rc.conf /zroot/staging/oldroot-configs/etc/
cp -av /mnt/oldroot/etc/pf.conf /zroot/staging/oldroot-configs/etc/
cp -av /mnt/oldroot/usr/local/etc/wireguard /zroot/staging/oldroot-configs/usr_local_etc/
cp -av /mnt/oldroot/usr/local/vm/\*.conf /zroot/staging/oldroot-configs/usr_local_vm/

Symptoms:
• We saw hundreds of files fly by from /usr/jails/nginx/bin — wait, did we just copy a whole base system?!
• Realization: we only wanted configs, but jails look like mini-systems. Copying them brings in /bin and /lib.
• Lesson: “config-only” for jails requires more careful pruning.

⸻

Step Three – Diff the Worlds

How different was old vs new? diff -u to the rescue:

diff -u /etc/rc.conf /zroot/staging/oldroot-configs/etc/rc.conf

Example output:

-ntpd_enable="YES"
-ntpd_sync_on_start="YES"
+pf_enable="YES"
+wireguard_enable="YES"
+vm_enable="YES"

What it tells us:
• The new install had NTP on; the old system had PF firewall, WireGuard, and bhyve VMs enabled.
• Each - means “new had it, old didn’t.”
• Each + means “old had it, new didn’t.”

Tools learned:
• diff -u file1 file2 → see precise line-by-line differences.
• cp -av → copy with attributes, see exactly what moves.
• zpool import -R /mnt/foo → mount old pools read-only for safety.

⸻

What Did We Learn?
• FreeBSD jails blur the line between “just configs” and “whole systems.”
• The most valuable configs live in /etc and /usr/local/etc.
• A staged copy + diff is a safe way to compare old vs new without blindly overwriting.
• “Config-only restore” is basically a rebuild — useful for learning, but sometimes slower than just resizing an old image and dropping it in place.

⸻

Light levity: This process felt like unpacking boxes after moving house. I just wanted the Wi-Fi password and router config, but somehow ended up with a toaster and three kettles from the old kitchen.

⸻

That’s the narrative for Post 1: a journey of discovery through configs, ZFS mounts, and the odd surprise of copying too much.

⸻

2. Resizing the Image (so it fits your smaller NVMe)

Your current raw image (seeed-ssd-expanded.img) is ~240 GB. Your NVMe is smaller, so we must shrink the image.

Step A – Check actual usage

Mount or inspect to see how much space is really used:

zpool list oldroot
zfs list -r oldroot

Say only ~70 GB is used. Great: we can shrink.

⸻

Step B – Shrink the filesystem

On ZFS, we don’t “shrink” datasets; instead, we truncate the image container to a smaller size that still holds all blocks. 1. Export the pool:

zpool export oldroot

    2.	Shrink the image with truncate (pick a size > actual usage, e.g. 100 GB):

truncate -s 100G seeed-ssd-expanded.img

⚠️ Must be larger than zpool list → ALLOC.

⸻

Step C – Write to NVMe

Once the image is the right size:

dd if=seeed-ssd-expanded.img of=/dev/nvme0 bs=1M status=progress conv=fsync

(replace /dev/nvme0 with the actual device).

⸻

Step D – Boot & Verify
• Boot from NVMe.
• zpool import → confirm pool health.
• If boot fails: you may need to reinstall the FreeBSD bootloader:

gpart bootcode -b /boot/pmbr -p /boot/gptzfsboot -i 1 nvme0

⸻

heere is the latest version of the post:
Got it 👍 — let’s turn your whole “config salvage vs. image import” adventure into a proper narrative blog post. Here’s a first draft that balances professional depth with a bit of levity:

⸻

When Backups Bite Back: Config Copy vs. Image Import in FreeBSD + ZFS

There are two kinds of sysadmin war stories:
• the ones where you do something clever,
• and the ones where you try to do something clever, and end up learning why the boring way is usually best.

This is one of the latter.

⸻

Background: the architecture

The stage was a little homelab setup:
• tb02, a FreeBSD host with an NVMe drive (nda0) and ZFS root pool zroot.
• A spinning rust backup drive (ada1), holding a big compressed .img.gz of an older system (“seeed-ssd”).
• A USB stick with a FreeBSD installer for rescue mode.

The goal?
Restore a server environment quickly.
I wanted to take the old system image and put it on the smaller NVMe drive — preserving services like jails, WireGuard, and pf rules — so I wouldn’t have to rebuild from scratch.

⸻

Strategy 1: Copy configs

The first attempt was pragmatic: just pull the config files out of the old root pool and drop them into staging.

Tools used
• zpool import — to make the old pool visible.
• zfs list — to explore what datasets existed.
• cp -av — to collect configs into a safe place.

Example

zpool import -f -o readonly=on -R /mnt/oldroot 9888157219862902893 oldroot
zfs mount oldroot/ROOT/default
cp -av /mnt/oldroot/etc/rc.conf /zroot/staging/oldroot-configs/etc/

Findings

This worked beautifully for /etc/rc.conf, pf.conf, WireGuard configs, and bhyve VM definitions.
diff -u made it easy to spot changes:

diff -u /etc/rc.conf /zroot/staging/oldroot-configs/etc/rc.conf

Output showed extra lines in the old system (jails, pf, wireguard, vm_dir).
That confirmed we’d salvaged what mattered.

Lesson: copying configs is fast, reliable, and the kind of thing production teams actually do.

But my tinkerer’s brain wasn’t satisfied — I wanted to resurrect the whole system image.

⸻

Strategy 2: Importing the image

This was where the hair-pulling began.

The .img was written to the spinner (ada1p1). To poke at it, I used mdconfig to attach it as a memory device:

mdconfig -a -t vnode -f /spinner/seeed-ssd-expanded.img -u 0
gpart show md0

Output confirmed the expected partitions:
• efi
• freebsd-boot
• freebsd-swap
• freebsd-zfs (md0p4)

So far so good.
Next step: import the ZFS pool.

zpool import -d /dev

This showed the pool metadata with the name oldroot.
But attempts to mount it went sideways:

zpool import -o readonly=on -R /mnt oldroot zroot

# -> “pool was previously in use…”

Or worse:

zpool import -o readonly=on -R /mnt md0p4 oldroot

# -> “no such pool available”

Debugging with zdb

To confirm I wasn’t hallucinating, I used:

zdb -l /dev/md0p4

That spit out metadata:

name: 'oldroot'
hostname: 'tb02'
pool_guid: 9888157219862902893

So the data was there, ZFS just didn’t want to cooperate.

⸻

Symptoms and theories
• Symptom: zpool import said “no such pool” even when zdb saw it.
Theory: maybe it was already imported, under a different name.
• Symptom: mountpoints were empty (ls /mnt/zroot/etc → “no such file or directory”).
Theory: default datasets had mountpoint=none or weren’t auto-mounted.
• Symptom: setting a new mountpoint failed with “read-only.”
Theory: importing with -o readonly=on prevented changes.

⸻

What we learned
• ZFS loves replication streams, not .img acrobatics.
The pro way to migrate pools is zfs send | zfs recv, not juggling images inside images.
• ZFS can see pools in .img files… but only if you get the import flags exactly right.
It’s possible, but fussy, especially in single-user mode.
• Config salvage is underrated.
Copying /etc, pf.conf, jail configs, and VM definitions gave me 90% of the rebuild for 10% of the effort.

⸻

Professional takeaway

In the end, I had to decide:
Was I trying to be clever, or was I trying to get the service running?

Copying configs and rebuilding services turned out to be the professional move. Importing from the .img was fascinating, educational, and blog-worthy — but not the fastest route to a working system.

And that’s the moral: professionalism isn’t about never failing — it’s about knowing when to pivot.

⸻

Commands cheat sheet
• Attach image as device
mdconfig -a -t vnode -f image.img -u 0
• Inspect partitions
gpart show md0
• List ZFS pools
zpool import -d /dev
• Check metadata
zdb -l /dev/md0p4
• Copy configs
cp -av /mnt/oldroot/etc/rc.conf /zroot/staging/etc/
• Diff configs
diff -u /etc/rc.conf /zroot/staging/etc/rc.conf

⸻

✅ Result: configs salvaged, system rebuilt, lesson learned.
Next time: maybe a cleaner pipeline with zfs send instead of .img gymnastics.

⸻

can you work these together
