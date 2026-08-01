# Serial Cables and COM Ports: Retro Tech in a Modern Rack

There's something oddly satisfying about plugging a modern laptop into a switch with a cable that feels like it belongs in the 1990s. My shiny TP-Link SG3428 came with an RJ45 console port, which meant one thing: serial time.

## First Hurdles: Server-Side Serial

At first I tried connecting the switch to my Ubuntu server (a Celeron box). It had a real COM port, so why not?

```bash
infra@nas04:~$ sudo screen /dev/ttyS0 38400
[screen is terminating]
```

Every attempt over SSH gave me lag, missing characters, and eventually lockups. The console worked only if I plugged in a keyboard/monitor directly. Trying to use minicom and picocom over SSH was no better. I had discovered the dark side of "two users fighting for the same serial buffer."

## The Serial Console Monogamy Problem

At first, things went well. With a direct monitor and keyboard ("head") attached to my Ubuntu home server, screen worked fine:

```bash
sudo screen /dev/ttyS0 38400
```

The console sprang to life, crisp and responsive.

But the minute I tried to get clever and use the network at the same time? Disaster.

I opened the switch via its management IP and via the serial port, thinking I could keep both views in sync. Instead, the switch sprayed output across both sessions, characters went missing, and inputs lagged like treacle. Even after closing the network session, the console didn't recover — I had to fully exit and re-open serial to get back to normal.

The lesson was clear: serial consoles are monogamous. They want one partner at a time, and if you cheat on them, they sulk.

Still, having a monitor on the server is hardly practical. My real goal was to sit at my MacBook, SSH into the server, and from there use the server's serial port. On paper it worked, but in practice it was unusable. Input lag, dropped characters, chopped output — like trying to watch a movie through a broken fax machine. Something in the chain — maybe Ubuntu, maybe my low-power Celeron, maybe just the timing mismatches of multiplexed software — meant the experience collapsed.

## Ser2net: The Workaround That Wasn't

I tried a more advanced trick: ser2net, exposing the serial port as a TCP service and tunnelling it over SSH. That gave me the warm feeling of technical cleverness, but the cold reality of the same lag and lost characters. Serial lines, I learned, are happiest in their intended state: two machines, one cable, no middlemen.

## Enter the USB Cable

I bought a USB to RS232 cable (FTDI-based), plugged the switch directly into my Framework laptop, and suddenly life was simple.

```bash
clexp@framework ~ % ls /dev/tty.*
/dev/tty.usbserial-1410
```

Success! The device showed up. No faffing with groups, no lag. Straight in with screen:

```bash
screen /dev/tty.usbserial-1410 38400
```

And just like that, the SG3428 CLI came alive on my desk. Quirky, old-school, but reliable.

## The Mac Experience

After my Bluefin battles, I tried the same USB serial cable on my MacBook. It wasn't exactly plug-and-play, but it was a lot smoother.

- First, I had to install the USB serial driver from the vendor's site (not in the App Store, of course)
- Then macOS popped up a permissions dialog: "Allow device to connect?" (click → yes)
- Finally, I just listed the devices:

```bash
ls /dev/tty.*
/dev/tty.usbserial-1410
```

…and connected:

```bash
screen /dev/tty.usbserial-1410 38400
```

No toolbox, no udev rules, no rpm-ostree arguments about groups. Just a little friction, then done.

The contrast was striking. On Bluefin I felt like I was holding the distro wrong, constantly hacking around "opinionated defaults." On macOS, once I got past the gatekeeper prompts, it just worked.

## Lessons Learned

- **Trying to use a server's serial port remotely is a rabbit hole of lag and frustration**
- **Immutable distros (like Bluefin) complicate things even more** — you can't just install screen
- **A simple USB-to-RS232 cable is worth its weight in gold**
- **Serial consoles are monogamous** — they want one partner at a time
- **Serial lines are happiest in their intended state: two machines, one cable, no middlemen**

Old tech, new laptop, smooth results. Sometimes the simplest route really is the best.

## The Verdict

This process felt like unpacking boxes after moving house. I just wanted the Wi-Fi password and router config, but somehow ended up with a toaster and three kettles from the old kitchen.

But in the end, the direct USB connection gave me exactly what I needed: reliable, responsive access to the switch console without fighting the network stack or immutable operating systems. Sometimes the old ways really are the best ways.

