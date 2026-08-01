title: framework setup: Virtualization for system administration

content narrative arc summaries:

"Excellent — that’s a very thoughtful approach.
You’re distinguishing learning structures (flashcards) from storytelling arcs (blog posts) — and you’re right: they overlap but don’t coincide.

Let’s identify the narrative arcs that naturally emerged from this conversation.
Each arc has a beginning (problem/question), a middle (exploration/discovery), and an end (insight/outcome).

Here’s a list of candidate arcs with concise summaries.

⸻

🧭 Arc 1 — Choosing the Right Distro for Learning and Daily Work

Initial question:

“What Linux distro(s) should I use on my Framework laptop if I want to both learn system administration and have a stable daily driver?”

Exploration:
• Compared Fedora, NixOS, Arch, Bluefin, Debian, openSUSE, and BSD.
• Discussed immutable vs mutable distros, hardware access vs containerization, and declarative vs imperative approaches.
• Reflected on productivity vs tinkering needs.

Outcome / insight:
• Fedora Workstation chosen as the daily driver for stability and hardware support.
• NixOS and Arch kept as “learning” systems (VMs or side installs).
• Immutable distros like Bluefin recognized as poor fits for sysadmin learning.

⸻

🧩 Arc 2 — Understanding Modern Partitioning and Filesystems

Initial question:

“Why did Fedora create Btrfs subvolumes instead of partitions, and where is my root actually mounted?”

Exploration:
• Investigated /dev/nvme0n1p\* naming and Btrfs subvolumes.
• Confusion over / not appearing in mount, and “where does Fedora actually live?”
• Compared partitions, subvolumes, datasets, and snapshots (Btrfs vs ZFS).
• Discussed how encryption, quotas, and flexibility replace rigid partitioning.

Outcome / insight:
• Understood Btrfs as a “filesystem within a filesystem” — dynamic and snapshot-aware.
• Decided to embrace Fedora’s defaults instead of over-partitioning manually.
• Learned how to check subvolumes, quotas, and mounts safely.

⸻

⚙️ Arc 3 — Setting Up a Modern Workstation for Productivity and Experimentation

Initial question:

“How do I set up Fedora to be a reliable productivity machine with Syncthing, Tailscale, Cursor, and Bitwarden, while still leaving space for experimentation?”

Exploration:
• Installed core apps via dnf, navigated Fedora’s dnf5 syntax changes.
• Configured SSH keys for GitHub and tested secure access.
• Chose RPM over AppImage for Cursor.
• Learned about Podman vs Docker, and toolbox isolation pitfalls from Bluefin.

Outcome / insight:
• Built a reproducible, hardware-friendly Fedora base.
• Gained comfort with system management tools and group memberships (dialout, libvirt).
• Clarified host vs container boundaries for tools that touch hardware.

⸻

🌐 Arc 4 — Diagnosing and Measuring Network Performance

Initial question:

“Why is my download speed so low, and how can I tell whether the bottleneck is my hardware, my LAN, or my ISP?”

Exploration:
• Used ethtool, iperf3, and speedtest-cli.
• Discovered hidden 10/100 switch in the lab network.
• Tested across segments (Framework ↔ FreeBSD router, Framework ↔ Amsterdam VPS).
• Upgraded FreeBSD router, learned FreeBSD vs OpenBSD package management (pkg, syspatch).

Outcome / insight:
• Achieved 941 Mbit/s LAN throughput; verified ISP cap (~100/20).
• Understood multi-layer network diagnostics (LAN / WAN / remote).
• Gained confidence in benchmarking, cabling, and version maintenance on BSD systems.

⸻

💻 Arc 5 — Learning Virtualization the Right Way

Initial question:

“How do I safely explore different operating systems without constantly reinstalling, and what exactly happens under the hood of a VM?”

Exploration:
• Installed libvirt and virt-manager.
• Learned what qcow2 files are, how sparse storage works, and why defaults are safest.
• Created Arch and FreeBSD VMs side-by-side.
• Realized the ISO is the “installer USB” and the qcow2 file is the “drive.”
• Connected conceptual dots between hardware, hypervisor, and guest.

Outcome / insight:
• Understood virtualization architecture deeply (“software running software on hardware”).
• Built first learning sandbox VMs with proper isolation.
• Established a foundation for multi-OS learning (Arch, FreeBSD, NixOS, LFS, etc.).

⸻

🧠 Arc 6 — Designing a Structured Learning Path with VMs

Initial question:

“How should I organize my learning across different OS families — Linux, BSD, declarative systems, and experimental OSes?”

Exploration:
• Mapped a staged learning progression:
• Stage 1: Arch + FreeBSD (fundamentals)
• Stage 2: NixOS + Linux From Scratch (infrastructure-as-code, internals)
• Stage 3: Redox + Plan 9 (conceptual exploration)
• Linked each to practical projects (DNS server, web server, SSH bastion, etc.).

Outcome / insight:
• Created a structured, goal-oriented roadmap for lifelong Unix learning.
• Recognized each system’s unique teaching value rather than chasing novelty.
• Prepared for narrative blog posts as “learning journeys.”

⸻

🎙️ Arc 7 — Building Local Dictation and AI Tools

Initial question:

“How can I run Whisper locally on my laptop for technical dictation without a GPU?”

Exploration:
• Discussed model sizes, CPU-only feasibility, and expected speeds.
• Compared Blurt (GUI) and whisper.cpp (CLI).
• Covered microphone quality, preprocessing (ffmpeg filters), and tuning (--threads, beam search).
• Planned future integration with Obsidian.

Outcome / insight:
• CPU Whisper viable for small/medium models, good enough for technical speech.
• Understood that sound quality > model size for low WER.
• Developed a clear plan for incremental improvement (hardware → audio → software tuning).

⸻

✅ Summary of the arcs: 1. Choosing the right distro for learning & daily work 2. Understanding modern partitioning and filesystems 3. Setting up a modern Fedora workstation 4. Diagnosing and measuring network performance 5. Learning virtualization the right way 6. Designing a structured multi-OS learning path 7. Building local dictation and AI tools

⸻

Each of these arcs is self-contained but connected — together, they are “Building a Modern Usable Linux Laptop for Learning and Productivity.”

Would you like me next to show how to group or merge these arcs into 3–4 narrative posts (each with a story flow and audience focus), while keeping all seven arcs intact for your private flashcards?"
