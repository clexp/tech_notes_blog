📄 Draft Post 5

Fighting “sensible defaults” on an immutable distro

Immutable distros sound brilliant on paper: no “config drift,” guaranteed reproducibility, easier updates. I thought Bluefin (Fedora-based) might make a neat daily driver for learning sysadmin work. Instead, I discovered just how much “sensible defaults” can fight you.

Installing the tiniest package

I wanted to install telnet to poke at the SG3428. Easy, right? Nope.

$ yum install telnet
bootc is configured to be read only

That’s right — the filesystem is immutable. To install a single tiny package, I had to spin up a toolbox container. That’s a 230MB image, just so I could run a 200KB binary.

(📸 Screenshot: toolbox init + telnet working)

Networking tug-of-war

Next problem: every time I set an IP on my interface, NetworkManager reset it. I’d write a script to reapply my config, run it, and… gone again. Eventually I had to mark the device as “unmanaged”:

sudo nmcli dev set enp0s13f0u2 managed no

That finally stopped NM from tearing my settings down.

(📸 Screenshot: ip addr flush + re-add script output)

Groups that don’t stick

Then came the serial cable. On most distros, you just add yourself to the dialout group:

sudo usermod -aG dialout clexp

Reboot, and you’re good. But on Bluefin, group edits didn’t survive reboots — because, of course, the group files are part of the immutable layer. Even rpm-ostree overrides produced odd errors like:

error: While applying overrides for pkg screen:
Could not find group 'screen' in group file

At this point, the distro was clearly fighting me.

The verdict

Immutable distros are brilliant for:
• Cloud servers.
• Kubernetes hosts.
• Developers who want reproducible build environments.

They are not brilliant for:
• Tinkering with serial ports.
• Learning old-school networking gear.
• Installing tiny tools quickly.

For my SG3428 adventures, Bluefin was friction at every step. The ProBook with plain Ubuntu? Worked first try.

(📸 Photo: Bluefin laptop next to SG3428 with a “not today” post-it)

⸻

please work this in:
📄 Post 5: Fighting ‘sensible defaults’ on an immutable distro

My Bluefin experiment started with optimism. Immutable OS, stable updates, rollback safety nets — what’s not to love?

Then I tried to actually do something with it.

Testing cables with iperf3. Installing screen for the switch console. Running picocom for a bit of low-level debugging. These are tiny tools, the kind of utilities you install without a second thought on Ubuntu or NixOS. But on Bluefin, immutability had opinions.
• Direct installs: blocked. Immutable root filesystem.
• rpm-ostree overrides: cryptic errors, failed group entries.
• User groups: couldn’t add myself to dialout for serial access, changes silently failed on reboot.
• Toolbox: yes, I could install software there, but it was a 230 MB “mini-VM” for a 200 KB tool. And it couldn’t pass hardware through by default.

The Bluefin forum pointed me towards a fix: write a udev rule to hand ownership of /dev/ttyUSB0 to my user. That was a smart workaround, and it worked. But by then the shine was off: I had spent hours fighting the OS for the right to run screen.

Meanwhile, the MacBook experience was almost boring in comparison. Install the driver, allow the permissions, find the tty device, done. Not zero-friction, but pragmatic and predictable.

Immutable systems have their place — cloud servers, big fleets where rollback beats flexibility. But for my use case — learning, experimenting, tinkering with odd bits of network gear — immutability just added friction. I wasn’t working with the system, I was working around it.

(📸 Screenshot: Bluefin toolbox vs tiny screen binary size)
(📸 Photo: Bluefin laptop with “Immutable opinions” sticky note)

---

please work this in:
Post five could include a lot more about how I have had difficulty trying to make the network tools work. I’ve been attempting to test cables and access the server using non-standard, non-default tools on Bluefin, such as iperf3. The problem seem to be it is difficult to install new software without using special installing tools or it's easy to install in a mini virtual machine but you can't pass any hardware through this layer of complexity slowed down all of my efforts and I'm not sure what it gave me in return of course it also affected using my serial cable.

---

please work this in:
📄 Post 5 — Polished verdict

Bluefin showed me the downsides of immutability when you’re tinkering with hardware:
• Couldn’t install screen or picocom directly.
• rpm-ostree overrides threw cryptic errors.
• User group edits didn’t persist (immutable /etc/group).
• Toolbox worked, but was a heavyweight fix for a lightweight need.
• Even with a udev rule, I was forced into the container for simple serial access.

It wasn’t that immutability is bad. It’s just that its opinions didn’t align with what I needed. For learning old-school sysadmin and networking gear, I want the OS to get out of the way, not argue with me.

By contrast, macOS wasn’t flawless, but it was pragmatic: a driver, a permissions prompt, a tty device, and done.

(📸 Photo idea: Bluefin laptop with a “Why are you fighting me?” sticky note vs MacBook happily connected to switch)
