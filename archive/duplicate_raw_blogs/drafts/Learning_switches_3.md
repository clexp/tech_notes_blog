Perfect — let’s lock in 3 and 5, then you’ll be free to dive into the “real fun” of switch configs.

I’ll give you two clean drafts:

⸻

📄 Draft Post 3

Serial cables and COM ports: retro tech in a modern rack

There’s something oddly satisfying about plugging a modern laptop into a switch with a cable that feels like it belongs in the 1990s. My shiny TP-Link SG3428 came with an RJ45 console port, which meant one thing: serial time.

First hurdles: server-side serial

At first I tried connecting the switch to my Ubuntu server (a Celeron box). It had a real COM port, so why not?

infra@nas04:~$ sudo screen /dev/ttyS0 38400
[screen is terminating]

Every attempt over SSH gave me lag, missing characters, and eventually lockups. The console worked only if I plugged in a keyboard/monitor directly. Trying to use minicom and picocom over SSH was no better. I had discovered the dark side of “two users fighting for the same serial buffer.”

(📸 Screenshot: terminal showing repeated [screen is terminating] errors)

Ser2net: the workaround that wasn’t

I installed ser2net, edited /etc/ser2net.yaml, and forwarded /dev/ttyS0 out over TCP. This half-worked, but still felt flaky — like serial wasn’t meant to be piped through SSH hops. At this point I started to suspect the truth: maybe serial consoles are meant to be accessed directly, not remotely via a server.

Enter the USB cable

I bought a USB to RS232 cable (FTDI-based), plugged the switch directly into my Framework laptop, and suddenly life was simple.

clexp@framework ~ % ls /dev/tty.\*
/dev/tty.usbserial-1410

Success! The device showed up. No faffing with groups, no lag. Straight in with screen:

screen /dev/tty.usbserial-1410 38400

(📸 Screenshot: first login prompt from SG3428 via Mac terminal)

And just like that, the SG3428 CLI came alive on my desk. Quirky, old-school, but reliable.

Lessons learned
• Trying to use a server’s serial port remotely is a rabbit hole of lag and frustration.
• Immutable distros (like Bluefin) complicate things even more — you can’t just install screen.
• A simple USB-to-RS232 cable is worth its weight in gold.

(📸 Photo: cable chain from switch RJ45 → DB9 → USB-C into the laptop)

Old tech, new laptop, smooth results. Sometimes the simplest route really is the best.

⸻

please inclued this in the draft:
mac was easier but still had some friction. You needed the app from the website, which was in the app store. You needed to give it permission. You needed to find the tty in /dev. but it worked.

---

please include
in the draft:
📄 Post 3: Serial cables and COM ports: retro tech in a modern rack

When the TP-Link SG3428 arrived, I knew the serial console would be part of the journey. What I didn’t know was how finicky and downright opinionated it would be about who gets to talk to it, and when.

At first, things went well. With a direct monitor and keyboard (“head”) attached to my Ubuntu home server, screen worked fine:

```
sudo screen /dev/ttyS0 38400
```

The console sprang to life, crisp and responsive.

But the minute I tried to get clever and use the network at the same time? Disaster.
I opened the switch via its management IP and via the serial port, thinking I could keep both views in sync. Instead, the switch sprayed output across both sessions, characters went missing, and inputs lagged like treacle. Even after closing the network session, the console didn’t recover — I had to fully exit and re-open serial to get back to normal.

The lesson was clear: serial consoles are monogamous. They want one partner at a time, and if you cheat on them, they sulk.

Still, having a monitor on the server is hardly practical. My real goal was to sit at my MacBook, SSH into the server, and from there use the server’s serial port. On paper it worked, but in practice it was unusable. Input lag, dropped characters, chopped output — like trying to watch a movie through a broken fax machine. Something in the chain — maybe Ubuntu, maybe my low-power Celeron, maybe just the timing mismatches of multiplexed software — meant the experience collapsed.

I tried a more advanced trick: ser2net, exposing the serial port as a TCP service and tunnelling it over SSH. That gave me the warm feeling of technical cleverness, but the cold reality of the same lag and lost characters. Serial lines, I learned, are happiest in their intended state: two machines, one cable, no middlemen.

(📸 Screenshot: screen working locally vs garbled characters over SSH)
(📸 Photo: the “snake” cable chain DB9→USB into the server)

---

please work this in:
Post three needs a little bit more detail about how difficult it was to use screen on the server remotely by SSH. Directly with a head on the server, a temporary arrangement, screen overs to the switch was good accessing the serial through the network port from another laptop at the same time meant there was lag and only some characters were sent to each screen. Clearly the serial console is made for one point of access at one time. Closing down the second access from the network port did not immediately fix the problem without existing completely and re-accessing from one port only once we were back on one port from the direct head on the server, the experience was very reasonable. However, the server is not built to have a head I tried to SSH into the server and access screen to access the switch. This had a lot of lag and missing characters while it worked. It was unusable. I am not sure what happened here but I think there must have been some sort of buffer or timing mismatch between the sending of the signals we tried using ser2net, firstly opening a port and then secondly over SSH but in neither case was it actually any better. I was not sure whether this was a problem with my celeron Home server or with ubuntu or a problem from combining two different pieces of software that were not designed to be combined in any case serial lines are clearly meant to be between just two machines with no further hops.

---

please add this to the storey:
Post 3 — Addendum (Mac angle)

After my Bluefin battles, I tried the same USB serial cable on my MacBook. It wasn’t exactly plug-and-play, but it was a lot smoother.
• First, I had to install the USB serial driver from the vendor’s site (not in the App Store, of course).
• Then macOS popped up a permissions dialog: “Allow device to connect?” (click → yes).
• Finally, I just listed the devices:

```
`ls /dev/tty.*
/dev/tty.usbserial-1410
```

…and connected:

````
screen /dev/tty.usbserial-1410 38400
```No toolbox, no udev rules, no rpm-ostree arguments about groups. Just a little friction, then done.

(📸 Screenshot: macOS terminal showing tty.usbserial and SG3428 login prompt)

The contrast was striking. On Bluefin I felt like I was holding the distro wrong, constantly hacking around “opinionated defaults.” On macOS, once I got past the gatekeeper prompts, it just worked.
````
