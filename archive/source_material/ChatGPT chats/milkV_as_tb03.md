title: milkV as tb03, fwupt probook, rebuild tb02

content narrative arc summaries:
"Perfect — this is the right move if you’re shaping this into narrative-style writing.
You’ve had a very organic technical journey, full of discovery, problem-solving, and pivots — ideal for human-readable storytelling arcs.

Here are the candidate narrative arcs extracted from your recent sessions, each framed as a short storyline (not just a topic):

⸻

Arc 1 — The Quest to Save and Restore the FreeBSD Webserver

Initial problem:
You wanted to back up and restore your FreeBSD webserver environment cleanly — ideally as a portable .img file — so you could replicate or migrate it.

Exploration:
You tried multiple approaches:
• Using dd and image files vs. ZFS snapshots.
• Attempting to mount .img files directly under ZFS and running into limitations.
• Wrestling with FreeBSD’s expectations for device-backed pools vs file-backed ones.
• Several detours into partitioning schemes (GPT vs MBR) and how bootloaders interact.

Outcome / insight:
• Realized that ZFS pools can’t easily import file-based disk images as volumes.
• Learned the deeper mechanics of how ZFS treats block devices vs filesystems.
• Decided to rebuild fresh, taking the knowledge forward rather than restoring old systems.
→ Narrative tone: the classic “I tried to clone my system, but it cloned me instead.”

⸻

Arc 2 — The Case of the Sluggish Network

Initial problem:
Network transfers were unexpectedly slow; you suspected drive or SATA issues, but it turned out to be the network itself.

Exploration:
• Used lsblk, lspci, and link checks to trace possible I/O bottlenecks.
• Discovered one link was negotiating at 100 Mb/s instead of gigabit.
• Verified via ifconfig and switch diagnostics.
• Began exploring switch replacement and physical wiring.

Outcome / insight:
• Identified the root cause: link negotiation / cabling issue.
• Sparked a much larger conversation about lab network design — VLANs, routers, switches, and redundancy.
→ Narrative tone: “The day I learned my cables were lying to me.”

⸻

Arc 3 — Building a FreeBSD Router from Scratch (rtr03)

Initial problem:
Needed a flexible, secure FreeBSD-based router to replace your existing setup — and wanted to understand every part of it.

Exploration:
• Configured interfaces (igb0, igb1), static IPs, and gateways.
• Set up pf firewall, NAT, and DHCP services.
• Debugged SSH failures (missing host keys, pf blocking, incorrect default routes).
• Routed around typos (10.0.0.5 instead of .50) and confirmed NAT via tcpdump.
• Tested end-to-end connectivity: LAN → router → ISP → Internet.
• Added Unbound as a local DNS proxy, forwarding queries to Pi-hole on the external network.

Outcome / insight:
• Achieved fully functional routing, DHCP, NAT, and DNS.
• Learned firewall and packet flow at packet-capture level.
• Gained an intuitive sense for “what’s actually happening” in home routing.
→ Narrative tone: “I built a router and accidentally became a packet detective.”

⸻

Arc 4 — Wrestling the Ghosts of an Old HP ProBook

Initial problem:
Wanted to repurpose an old ProBook, possibly as a server or rescue device, but firmware and OS updates were painful.

Exploration:
• Discovered BIOS only handled MBR, not GPT.
• Struggled to flash firmware via FreeDOS and Windows 7 tools.
• Tried Hiren’s Boot CD and rescue images with mixed success.

Outcome / insight:
• Learned where BIOS-era hardware hits the wall for modern OS use.
• Reclassified the machine as a safe tinkering or programming platform rather than a production one.
→ Narrative tone: “I tried to save an old ProBook — and learned how the past refuses to boot.”

⸻

Arc 5 — The DNS and NAT Detective Story

Initial problem:
Your new router (rtr03) wasn’t forwarding DNS or ICMP traffic correctly; devices on the LAN could ping internally but not resolve domains.

Exploration:
• Deep dive with tcpdump on both interfaces.
• Verified NAT rules missing from pfctl -sr.
• Fixed Unbound configuration to forward DNS queries across subnets (to Pi-hole).
• Debugged multiple SERVFAILs until forwarders, ports, and ACLs were correctly aligned.
• Verified proper DNS resolution with drill and dig.

Outcome / insight:
• Fully working DNS proxy with local Unbound forwarding outward.
• Gained hands-on understanding of recursive vs forwarding DNS behavior, pf states, and NAT translation.
→ Narrative tone: “How a missing forward-zone line taught me everything about DNS recursion.”

⸻

Arc 6 — The Jump to RISC-V

Initial problem:
You needed a low-power, 24/7 home webserver — and wanted something intellectually interesting (not another Pi).

Exploration:
• Researched RISC-V boards: Milk-V Mars, StarFive, Banana Pi, BeagleV.
• Compared features, price, performance, OS support.
• Discovered the Mars’ M.2 E-key slot lacks PCIe lanes (no NVMe).
• Explored eMMC vs microSD vs USB SSD for system storage.
• Discussed Debian vs Fedora on RISC-V and container support (Podman vs Docker).

Outcome / insight:
• Ordered a Milk-V Mars (4 GB, eMMC model).
• Planned Debian setup, lightweight webserver stack, and later Podman deployment.
• Established a forward-looking vision for open hardware hosting.
→ Narrative tone: “Leaving x86 behind — one RISC-V at a time.”

⸻

Arc 7 — The Philosophy of the Home Lab

(This one runs quietly through all arcs.)
Initial question:
How can you build a network and compute environment that’s educational, secure, modular, and sustainable?

Exploration:
• Every practical task led to broader insights — redundancy, security zones, long-term maintainability.
• You began moving from tinkering to architecting.

Outcome / insight:
• You now have a coherent multi-layered home infrastructure plan:
• FreeBSD routers,
• managed switches,
• segmented LANs,
• Pi-hole/Unbound DNS,
• future RISC-V servers.
→ Narrative tone: “From blinking lights to systems thinking: building the lab I wish I’d started with.”

⸻

Would you like me to now group or merge these into potential blog series arcs (e.g. 3–5 longform posts that flow as a story),
or would you prefer I expand each of these arcs first into 2–3 paragraph summaries so you can feel their narrative weight before combining them?"
