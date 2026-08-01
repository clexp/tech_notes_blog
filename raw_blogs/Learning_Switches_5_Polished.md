# Fighting "Sensible Defaults" on an Immutable Distro

Immutable distros sound brilliant on paper: no "config drift," guaranteed reproducibility, easier updates. I thought Bluefin (Fedora-based) might make a neat daily driver for learning sysadmin work. Instead, I discovered just how much "sensible defaults" can fight you.

## Installing the Tiniest Package

I wanted to install telnet to poke at the SG3428. Easy, right? Nope.

```bash
$ yum install telnet
bootc is configured to be read only
```

That's right — the filesystem is immutable. To install a single tiny package, I had to spin up a toolbox container. That's a 230MB image, just so I could run a 200KB binary.

## The Immutability Problem

My Bluefin experiment started with optimism. Immutable OS, stable updates, rollback safety nets — what's not to love?

Then I tried to actually do something with it.

Testing cables with iperf3. Installing screen for the switch console. Running picocom for a bit of low-level debugging. These are tiny tools, the kind of utilities you install without a second thought on Ubuntu or NixOS. But on Bluefin, immutability had opinions.

- **Direct installs:** blocked. Immutable root filesystem
- **rpm-ostree overrides:** cryptic errors, failed group entries
- **User groups:** couldn't add myself to dialout for serial access, changes silently failed on reboot
- **Toolbox:** yes, I could install software there, but it was a 230 MB "mini-VM" for a 200 KB tool. And it couldn't pass hardware through by default

## Networking Tug-of-War

Next problem: every time I set an IP on my interface, NetworkManager reset it. I'd write a script to reapply my config, run it, and… gone again. Eventually I had to mark the device as "unmanaged":

```bash
sudo nmcli dev set enp0s13f0u2 managed no
```

That finally stopped NM from tearing my settings down.

## Groups That Don't Stick

Then came the serial cable. On most distros, you just add yourself to the dialout group:

```bash
sudo usermod -aG dialout clexp
```

Reboot, and you're good. But on Bluefin, group edits didn't survive reboots — because, of course, the group files are part of the immutable layer. Even rpm-ostree overrides produced odd errors like:

```
error: While applying overrides for pkg screen:
Could not find group 'screen' in group file
```

At this point, the distro was clearly fighting me.

## The Workaround That Worked (Sort Of)

The Bluefin forum pointed me towards a fix: write a udev rule to hand ownership of `/dev/ttyUSB0` to my user. That was a smart workaround, and it worked. But by then the shine was off: I had spent hours fighting the OS for the right to run screen.

```bash
# Create udev rule for USB serial devices
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666", OWNER="clexp"' | sudo tee /etc/udev/rules.d/99-usb-serial.rules
sudo udevadm control --reload-rules
```

## The Contrast: macOS Simplicity

Meanwhile, the MacBook experience was almost boring in comparison. Install the driver, allow the permissions, find the tty device, done. Not zero-friction, but pragmatic and predictable.

```bash
# On macOS - just works
ls /dev/tty.*
/dev/tty.usbserial-1410
screen /dev/tty.usbserial-1410 38400
```

## The Verdict

**Bluefin showed me the downsides of immutability when you're tinkering with hardware:**

- Couldn't install screen or picocom directly
- rpm-ostree overrides threw cryptic errors
- User group edits didn't persist (immutable /etc/group)
- Toolbox worked, but was a heavyweight fix for a lightweight need
- Even with a udev rule, I was forced into the container for simple serial access

**Immutable systems have their place:**

- Cloud servers
- Kubernetes hosts
- Developers who want reproducible build environments
- Big fleets where rollback beats flexibility

**They are not brilliant for:**

- Tinkering with serial ports
- Learning old-school networking gear
- Installing tiny tools quickly
- Hardware experimentation

It wasn't that immutability is bad. It's just that its opinions didn't align with what I needed. For learning old-school sysadmin and networking gear, I want the OS to get out of the way, not argue with me.

By contrast, macOS wasn't flawless, but it was pragmatic: a driver, a permissions prompt, a tty device, and done.

## The Professional Takeaway

For my SG3428 adventures, Bluefin was friction at every step. The ProBook with plain Ubuntu? Worked first try.

Immutable systems are brilliant for production environments where you want consistency and rollback capabilities. But for learning, experimenting, and tinkering with odd bits of network gear, immutability just added friction. I wasn't working with the system, I was working around it.

Sometimes the best tool for the job is the one that gets out of your way and lets you focus on what you're actually trying to learn.


