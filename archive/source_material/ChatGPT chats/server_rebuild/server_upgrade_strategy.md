title: server upgrade strategy

content narrative arc summaries:
"
Excellent — this conversation has developed a clear multi-stage journey through building a home production server, and it naturally divides into distinct narrative arcs, each with a strong learning thread.
Here are the candidate arcs with short summaries:

⸻

Arc 1: From Vision to Blueprint — defining the purpose and scope of the home production server

Initial question:
What do I actually want this system to do — serve media, rip discs, handle photos, back up data, filter the web — and how do those roles fit together?

Exploration:
We refined the plan around a single always-on x86 server with ZFS, plus a series of satellite boxes (router, CCTV, Home Assistant).
We clarified that “ARM” means Automatic Ripping Machine, not ARM architecture.
You mapped out network topology, VLANs, and service goals (Jellyfin, Immich, SearXNG, Paperless-ngx, Pi-hole).

Outcome:
A clear architecture of roles, power constraints, and learning priorities — a hybrid of production reliability and educational sandbox.

⸻

Arc 2: Hardware Architecture — balancing performance, budget, and practicality

Initial question:
What hardware choices make sense for this workload and budget (~£300 now, staged upgrades later)?

Exploration:
We compared disk sizes, mirror/vdev strategies, and the new ZFS vdev-expansion feature.
You prioritised fast metadata access over write-heavy performance.
We explored Intel QuickSync requirements for Jellyfin, the trade-off between a single capable server and multiple specialist boxes, and RAM sizing (eventually 32 GB).

Outcome:
A rational, expandable hardware plan: ZFS mirrored HDDs for storage, SSD/NVMe for ARC/ZIL, Proxmox host with Ubuntu VM for services, and staged purchases to match cashflow.

⸻

Arc 3: Component Decisions — motherboard, RAM, NVMe, and value hunting

Initial question:
Which mainboard and components give enterprise-like reliability without gamer markup?

Exploration:
We filtered gaming-oriented boards down to professional-looking B760M models, compared ASUS vs MSI vs Gigabyte, learned about VRMs, PCIe lanes, and M.2 slots.
You learned how DDR4/DDR5 speeds and CAS latency translate into real-world performance, and how UDIMM/soDIMM types fit.
We balanced voucher constraints and market volatility while evaluating RAM (Lexar, Yongxinsheng) and NVMe drives (Samsung 990 PRO vs Kingston KC3000).

Outcome:
A confident, well-justified purchase set: MSI B760M DDR4 board, i5-12400 CPU, 32 GB DDR4-3200 CL16 RAM, Samsung 990 PRO 1 TB for L2ARC, Samsung 870 EVO 500 GB for VMs, all powered by an existing Seasonic PSU.

⸻

Arc 4: Infrastructure and Casework — racks, airflow, and ergonomics

Initial question:
How do I house everything cheaply, quietly, and accessibly in a small rack?

Exploration:
We reviewed rack depths and U-sizes, discovered that 500 mm-deep 4U cases like the Codegen fit the bill, and confirmed that standard shelves can host non-rack devices (UPS, router).

Outcome:
A practical home rack design (≈12 U, 19-inch wide, 500 mm deep) with scope for future expansion but still living-room-friendly.

⸻

Arc 5: Disk Strategy and Reliability — testing, mirroring, and performance

Initial question:
How can I ensure my HDDs and SSDs are reliable before entrusting data to them?

Exploration:
We designed a full drive-testing protocol using SMART, badblocks, and fio; discussed NVMe mirroring pros and cons; and clarified HBA (LSI 9211/9300 series) selection.

Outcome:
A repeatable disk-burn-in and benchmarking procedure that builds confidence in the storage layer before pool creation — a key foundation for the project’s reliability ethos.

⸻

Arc 6: The Learning-through-Building Philosophy

Initial question:
Given limited funds, how can I structure purchases so I can learn core systems skills without wasting money on over-complex setups?

Exploration:
You weighed realism against experimentation: keeping core services on stable, standard configurations while using spare or older hardware for learning projects (Home Assistant, Frigate, SDR).

Outcome:
A clear guiding principle for the whole project: spend on reliability, but always leave a pathway for experimentation and education.

⸻

Would you like me next to: 1. Map which arcs could naturally merge or split into coherent blog-length stories, 2. Or begin outlining one arc (for example, “From Vision to Blueprint”) as a draft narrative structure with tone and headings for your blog?
"
