# Chasing Packets Through Copper: 24-Hour iperf3 Cable Test

There’s a simple question at the heart of this project: “Is my Cat6 cable really good enough?”

Sure, specs say it should handle gigabit traffic without fuss. But our installation wasn’t a textbook setup. The cable ran up into the loft, across the beams, past the chimney stack, and back down again. At night it shared a conduit with a heating element. During the day, PV solar production meant the electrical environment was anything but stable.

That mix of copper, heat, and power noise made it the perfect candidate for a 24-hour stress test.

⸻

## The Test Setup

We built a point-to-point gigabit test link using two devices:
• Seeed Odyssey (FreeBSD): acting as the iperf3 server.
• Framework Laptop (Fedora Bluefin): acting as the iperf3 client.

The link under test was plugged into the second NIC on the Seeed (igb1) and the Framework’s main RJ45 port. For control, the Seeed stayed reachable via its first NIC (igb0) through the home router.

(📸 Photo idea: The cable run in the loft, looping over the chimney stack)

(📸 Photo idea: Framework laptop on the kitchen shelf, next to the audio Raspberry Pi)

⸻

## First Steps: Giving Each End an Address

We carved out a tiny /30 subnet — just four addresses, of which two are usable.

On the Seeed (FreeBSD):

ifconfig igb1 192.168.59.1 netmask 255.255.255.252
ifconfig igb1

Expected output:

igb1: flags=1008843<UP,BROADCAST,RUNNING> mtu 1500
inet 192.168.59.1 netmask 0xfffffffc broadcast 192.168.59.3
media: Ethernet autoselect (1000baseT <full-duplex>)
status: active

On the Framework (Linux):

sudo ip addr add 192.168.59.2/30 dev eth0
ip a show eth0

Output:

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>
inet 192.168.59.2/30 brd 192.168.59.3 scope global eth0

A quick ping confirmed connectivity:

ping -c 3 192.168.59.1

⸻

## Launching iperf3

On the Seeed, we wanted the server to stay alive after logout:

nohup iperf3 -s -B 192.168.59.1 > /var/log/iperf3-server.log 2>&1 &

Checking the log showed it listening:

---

## Server listening on 5201

On the Framework, we scripted the client to run for 24 hours, reporting once a minute, and tagging each line with a timestamp:

nohup stdbuf -oL iperf3 -c 192.168.59.1 -t 86400 -i 60 | \
while read line; do
echo "$(date '+%H:%M:%S') $line"
done > iperf3-client.log 2>&1 &

Sample log line:

08:16:00 [ 5] 0.00-60.00 sec 6.60 GBytes 942 Mbits/sec sender

So far, so good. Both ends agreed: ~942 Mbit/s, the maximum practical throughput for gigabit Ethernet.

⸻

## The Mysterious 35-Minute Wall

And then the weirdness began. The Framework happily logged data… for about 35 minutes. Then it would stop.

We checked the server — still running. The cable LEDs — still lit. The client log — frozen.

Time to check the logs:

journalctl -b | grep suspend

Output revealed the culprit:

ModemManager: system is about to suspend
systemd: Reached target Sleep.
kernel: PM: suspend entry (deep)

The laptop was putting itself to sleep, script or no script.

⸻

## Disabling Sleep

To keep the Framework awake, we masked the relevant systemd units:

sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

Verification:

systemctl status sleep.target

Output:

sleep.target
Loaded: masked (Reason: Unit is masked.)
Active: inactive (dead)

This stopped systemd from suspending, even when the lid closed.

⸻

## NetworkManager Meddling

Another hiccup: sometimes after resume, the Framework’s NIC had no IP address. NetworkManager had torn it down “for security.”

The fix was to stop managing the test interface:

nmcli device set eth0 managed no

After that, manual IP assignment stuck.

⸻

## The Overnight Run

With suspend disabled and NetworkManager tamed, the script ran without interruption. The logs showed 942 Mbit/s every single minute for 24 hours straight.

(📊 Graph of overnight throughput here — perfectly flat line)

Not a single blip, despite heating cycles at night and PV noise during the day.

⸻

## Lessons Learned

    •	Don’t fight the hardware’s defaults without checking logs. The journalctl output pointing to suspend was the real “a-ha!” moment.
    •	Systemd controls sleep. Masking targets worked where GUI sliders didn’t.
    •	NetworkManager isn’t your friend during static tests. Disabling management of the interface kept IPs stable.
    •	iperf3 plus nohup is rock solid. Once the environment was stable, the test was flawless.

⸻

Epilogue: The Serial Cable

As we wrapped up, one lingering thought remained: what if the Seeed locks up again, HDMI dead, but still on the network? The board exposes UART pins (GND, TX, RX, RESET). With a cheap USB-to-UART cable, we can connect those to the Framework or Mac and get a root console no matter what the graphics or SSH daemons are doing.

That’s the next frontier: a direct wire into the board’s brain.

⸻

👉 So in the end, Cat6 passed with flying colors. Fibre would be fun, but copper’s holding its own — even when hanging down the inside of a chimney.
