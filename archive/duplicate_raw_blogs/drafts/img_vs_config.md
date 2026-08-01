
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

