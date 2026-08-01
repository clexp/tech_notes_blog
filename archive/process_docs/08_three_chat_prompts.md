# Three Chat Prompts — getting blog.clexp.net live

Folders moved to home root on 2026-08-01. Open **new** Cursor chats on these paths
(old Sync-path chats are stale).

One objective, three workspaces, three separate chats. Paste each prompt as the
first message of its chat.

## The three workspaces

| Chat | Folder | Owns | State |
|---|---|---|---|
| **A — Edge** | `~/OpenBSD_web` | DNS + TLS + VPS↔rtr04 WireGuard | 128 KB of notes, no git repo |
| **B — Origin** | `~/MilkV` | MilkV host + MilkV↔rtr04 LAN path | 21 MB, git `main`, no remote |
| **C — Content** | `~/Tech_Blog` | Posts + Zola build | 298 MB, git remote on GitHub |

## Network boundary (revised)

```
Internet
   │
   ▼
 OpenBSD VPS (vps01 / vps)
   │  TLS terminate (relayd/httpd + LE certs)     ← Chat A
   │  WireGuard tunnel                           ← Chat A  (VPS ↔ rtr04 only)
   ▼
 rtr04
   │  WG endpoint + route to 10.100.0.5          ← Chat A owns the WG side
   │  DNAT 10.100.0.5:80 → 10.0.40.13:80         ← Chat B owns DNAT / VLAN 40
   │  VLAN 40 isolation + pf                     ← Chat B
   ▼
 MilkV 10.0.40.13  nginx :80                     ← Chat B
   NO WireGuard on MilkV (board cannot run it)
```

**Shared host: rtr04.** Split cleanly:
- Chat A may edit: WireGuard config on VPS and rtr04, routes that carry the tunnel.
- Chat B may edit: VLAN 40, MilkV static IP, pf rules for VLAN 40, DNAT to MilkV.
- Neither installs WireGuard on MilkV. If you believe you must, stop.

**Shared-resource rule on the VPS.**
- Chat A may edit: `/etc/acme-client.conf`, `httpd.conf` challenge blocks, Cloudflare DNS,
  WireGuard, and only the TLS/SNI side of `relayd.conf`.
- Chat B may edit: `relayd` **backend/table** that points at `10.100.0.5:80`, and nothing
  else in relayd. Prefer leaving a note in `~/OpenBSD_web/HANDOFF.md` if the SNI front
  and the backend must change together.

## Dependency order

A and B can run **in parallel** on different layers; they only meet at rtr04 DNAT↔WG.
C is cleanup. `blog.clexp.net` goes live when A and B are both complete.

## The discrepancy Chat C fixes

- `Tech_Blog/deploy.sh` → `FREEBSD_HOST="10.0.0.50"` nginx jail — **stale**, old host.
- `MilkV/lab/deploy-blog.sh` → current path to `~/Tech_Blog` → MilkV `/var/www/blog`.

---

# PROMPT A — Edge (DNS + certificates + VPS↔rtr04 WireGuard)

```
Workspace: ~/OpenBSD_web

OBJECTIVE (the only one)
Get a valid Let's Encrypt certificate for blog.clexp.net on the OpenBSD VPS,
with automatic renewal, DNS that matches where relayd listens, and a working
WireGuard path from this VPS to rtr04. Stop at the rtr04 WG endpoint.

READ FIRST
- current_LE_status.md   (the diagnosis is already written; trust it)
- DNS_AND_LE_INFRASTRUCTURE.md
- zone_v8_recommended.txt
- Working_Files/acme-client.conf and Working_Files/get-certs-httpd.conf
- Sibling network intent lives in ~/MilkV/docs/site-network.md
  (path: VPS relayd → 10.100.0.5:80 → rtr04 DNAT → MilkV). Read it; do not edit MilkV.

KNOWN STATE
VPS: 46.23.95.221 / 2a03:6000:95f4:618::221. DNS on Cloudflare.
blog.clexp.net is NOT in acme-client.conf, so it has no certificate.
blog has an A record to .221 only, no AAAA, but relayd listens for blog on ::224:443.
That mismatch plus the missing cert is the TLS half of the problem.
WireGuard is VPS ↔ rtr04 only. MilkV has no WireGuard and must not get any.

IN SCOPE
Cloudflare DNS records. /etc/acme-client.conf. httpd.conf ACME challenge blocks.
Certificate issuance and the renewal cron job.
WireGuard on the VPS and the matching WG endpoint / routes on rtr04.
relayd TLS/SNI front for blog.clexp.net (listener + cert binding).

OUT OF SCOPE — another chat owns these
VLAN 40, MilkV static IP, DNAT 10.100.0.5→MilkV, MilkV nginx, blog content,
the apex clexp.net 526 problem, mail on box.clexp.net, ntfy.
Do not put WireGuard on MilkV.

rtr04 OVERLAP RULE
You own the WG tunnel. Chat B owns DNAT and VLAN 40.
If both must change for one test, write the handoff in HANDOFF.md and stop
rather than editing Chat B's pf/DNAT yourself.

THREE OPEN DECISIONS — ask me, do not assume
1. Apex: redirect clexp.net to www at Cloudflare, or serve content on the apex?
2. Model A (one IPv4 SNI relay for all names) or Model B (split listeners)?
3. Which names stay Cloudflare-proxied vs DNS-only?

DONE WHEN
  doas acme-client -v blog.clexp.net   succeeds
  ls -l /etc/ssl/blog.clexp.net.crt    exists
  curl -I https://blog.clexp.net       returns TLS without a name mismatch
  renewal cron is installed and tested
  VPS can reach 10.100.0.5 over WireGuard (even if DNAT to MilkV is still Chat B's job)
Then append a short summary to current_LE_status.md and stop.

WORKING RULES
Do not expand scope. If you find another broken thing, write it in HANDOFF.md and
carry on. I have a documented history of turning one fix into three projects.
Show me commands before running anything against live DNS or the VPS.
```

---

# PROMPT B — Origin (MilkV ↔ rtr04; no WireGuard on MilkV)

```
Workspace: ~/MilkV

OBJECTIVE (the only one)
Finish Phase 1: make MilkV Mars reachable from rtr04 so the VPS can forward
blog.clexp.net to it. Harden the board. No WireGuard on MilkV.

READ FIRST
- docs/STATUS.md   (resume file)
- Plan.md
- docs/rtr04-vlan40-milkv.md, docs/milkv-static-ip-vlan40.md, docs/vps-relayd-blog-fix.md
- lab/rtr04-vlan40-pf.conf
- docs/site-network.md

KNOWN STATE
Board done. VLAN 40 live. nginx serving /var/www/blog; curl http://127.0.0.1/ returns 200
with 71 files already deployed. SSH keys-only, server_tokens off, mosquitto purged.
Remaining: hardening, VLAN/pf, and DNAT on rtr04.
Target path: VPS (Chat A) → WG → rtr04 → DNAT 10.100.0.5:80 → MilkV 10.0.40.13:80.
MilkV is not capable enough for WireGuard. Do not install it. Do not configure it.

IN SCOPE
The MilkV board itself. VLAN 40 / switch / rtr04 LAN side. pf rules for VLAN 40.
DNAT on rtr04 from 10.100.0.5:80 to MilkV. lab/deploy-blog.sh.
relayd BACKEND / table on the VPS that points at 10.100.0.5:80 — only that table,
not the TLS listener (Chat A).

OUT OF SCOPE — another chat owns these
acme-client.conf, TLS certificate issuance, Cloudflare DNS, httpd.conf,
WireGuard on VPS or rtr04, blog content or Zola configuration.

EXPLICITLY NOT THIS PROJECT (already moved out, keep it that way)
Phase 2 MIPI CSI camera. Phase 3 cabinet GPIO/fans/temp. The home alarm. uptime-tick.
MQTT, LoRa, greenhouse, Grafana. If any of these look tempting, they are not in Phase 1.

rtr04 OVERLAP RULE
You own VLAN 40 + DNAT + MilkV-facing pf.
Chat A owns WireGuard VPS↔rtr04.
If the WG address 10.100.0.5 is missing or wrong, write HANDOFF.md under
~/OpenBSD_web and stop — do not "fix" it by putting WG on MilkV.

DONE WHEN
  from rtr04, curl -sI http://10.0.40.13/ returns MilkV nginx
  DNAT 10.100.0.5:80 → 10.0.40.13:80 works when Chat A's tunnel is up
  hardening checklist in docs/STATUS.md is complete
  lab/deploy-blog.sh runs clean end to end (content source is ~/Tech_Blog)
Then update docs/STATUS.md and stop.

WORKING RULES
Phase 1 only. Do not start Phase 2 or 3.
This repo has no git remote. Before we finish, set one up and push.
Show me commands before running anything against the router, pf, or the VPS.
```

---

# PROMPT C — Content (Zola build + deploy hygiene)

```
Workspace: ~/Tech_Blog

OBJECTIVE (the only one)
Get this repo into a clean, publishable state. The content is already written —
this is tidying and deploy hygiene, not writing.

KNOWN STATE
Zola site. 46 posts in content/, 43 drafts in raw_blogs/, 5 in work_in_progress/.
public/ builds. git remote: git@github.com:clexp/tech_notes_blog.git (branch main, dirty).
config.prod.toml sets base_url = https://blog.clexp.net
This folder was moved from ~/Sync/Work_Pieces/Tech_Blog to ~/Tech_Blog.

TASK 1 — retire the stale deploy path
deploy.sh targets FREEBSD_HOST=10.0.0.50 with an nginx jail. That host is obsolete.
The live path is ~/MilkV/lab/deploy-blog.sh, which already builds from ~/Tech_Blog
with config.prod.toml and rsyncs to MilkV /var/www/blog.
Move deploy.sh to archive/ and put one line in README.md saying where deploy now lives.

TASK 2 — prune the process documents
There are 25 markdown strategy documents and 7 workflow scripts at the top level,
including four separate documents about image strategy. Consolidate to at most two:
WORK_FLOW.md and one image guide. Move the rest to archive/.
Do not delete anything - move it.

TASK 3 — verify and commit
  zola -c config.prod.toml build   must succeed
  commit and push to origin

OUT OF SCOPE — do not touch, another chat owns these
TLS certificates, DNS, relayd, pf, WireGuard, the MilkV board, VPS configuration.
Do NOT write new blog posts. Do NOT restructure content/.

DONE WHEN
prod build is clean, deploy.sh is archived with a pointer, top-level process docs
are down to two, and everything is committed and pushed.

WORKING RULES
No new posts, no new tooling, no new strategy documents. If you catch yourself
writing a document about how to write documents, stop.
```
