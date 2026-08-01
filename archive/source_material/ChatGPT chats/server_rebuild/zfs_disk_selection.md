title: zfs disk selection

content narrative arc summaries:
"
Excellent — this chat has evolved through several intertwined threads, but we can now see clear narrative arcs emerging. Each one follows a distinct problem–exploration–resolution path and could stand alone or interconnect into a larger “building a resilient home server” series.

Here are the candidate arcs with short summaries:

⸻

Arc 1 — What drives are suitable for ZFS?

Summary:
Starts with uncertainty about which disks are appropriate for ZFS and whether cheaper drives can safely replace Seagate IronWolf models. The exploration covers CMR vs SMR recording, NAS vs desktop drives, the importance of mixing vendors, and performance vs reliability trade-offs.
Outcome:
A clear rule set for choosing ZFS-safe drives emerges — prioritizing CMR NAS-class drives and redundancy over speed.

⸻

Arc 2 — How much storage do I really need?

Summary:
Begins with rough estimates of data sizes and a suspicion that the current 12 TB mirrored setup is excessive. Using zfs list and du, the user examines real dataset sizes, discovers actual usage under 1 TB, and recalibrates expectations.
Outcome:
Realization that 3–5 TB will comfortably cover medium-term growth, leading to simpler, cheaper storage planning and more confidence in mirror-based pools.

⸻

Arc 3 — Planning the migration and liberation of drives

Summary:
Focuses on how to free the IronWolf drives from existing mirrors to reuse in a new pool without losing uptime. Explores live data migration via ZFS resilvering, and later evolves into a simpler “use temporary backup drives instead” plan.
Outcome:
A step-by-step migration plan forms: use temporary backups to liberate drives, then rebuild the main pool cleanly. The process is demystified and becomes repeatable.

⸻

Arc 4 — Rethinking backup purpose and scope

Summary:
A pivotal realization: not all data is equally valuable. The user separates irreplaceable datasets (personal files, photos, documents) from easily re-rippable media (music, DVDs).
Outcome:
The backup plan shifts from “mirror the entire server” to “protect what matters.” This simplification reshapes both storage needs and architecture — a classic “less but better” moment.

⸻

Arc 5 — Salvaging old hardware for meaningful roles

Summary:
The aging Athlon system with mixed SATA cards and drives transforms from e-waste into a practical backup host. The user balances risk, power draw, and redundancy, designing a pair of RAIDZ2 vdevs from legacy disks.
Outcome:
Old hardware is given a new life as an offsite or secondary backup, turning salvage into sustainability — and illustrating the virtue of designing within constraints.

⸻

Arc 6 — Designing a layered backup hierarchy

Summary:
Brings together all the decisions: 1. New server (production) 2. Old server (onsite backup) 3. Athlon salvage box (offsite backup).
The user develops a tiered, rotating backup strategy and confronts questions of automation vs manual sync.
Outcome:
A professional-grade, multi-tiered backup design emerges organically from home resources. It blends reliability, pragmatism, and long-term sustainability.

⸻

Arc 7 — Automation, trust, and control: the offsite replication dilemma

Summary:
A reflective close: whether to automate replication over WireGuard or do manual syncs. This opens a philosophical thread about trust, maintenance burden, and the human factor in backup design.
Outcome:
Acknowledges that “professional” isn’t always “best” — manual syncs may be safer and simpler for a home setup. Ends with a nuanced understanding of how technology serves human limits.

⸻

Would you like me to now expand each arc into a structured outline (problem → exploration → insight) so we can see which ones naturally flow together as potential blog posts or a serial story (e.g., “Building a Resilient Home Server: from Chaos to Confidence”)?
"
