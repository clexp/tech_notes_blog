# Workflow (Zola)

This repo uses one source tree and two build modes:

- **Development (working version):** local preview, drafts allowed.
- **Production (public version):** built artifact only, drafts excluded.

## Which folder gets deployed?

Zola always outputs the built site to the `public/` directory. That is the **only**
folder you push to the server.

## Build commands

### Development

```
zola serve
```

- Uses `config.toml` by default.
- Add drafts to the preview:

```
zola serve --drafts
```

### Production

```
zola -c config.prod.toml build
```

- Writes the final site to `public/`.
- Only content that is **not** marked as draft is included.

## How drafts are excluded

Zola ignores any page with `draft = true` in its front matter.
This is independent of the config file, but production builds should
always use `config.prod.toml` so URLs and metadata are correct.

Example front matter:

```
+++
title = "Working Title"
date = 2026-05-08
draft = true
+++
```

## How to see which articles are still drafts

Drafts are just markdown files in `content/` with `draft = true`.
You can find them quickly with:

```
rg "draft = true" content
```

## Suggested day-to-day flow

1. **Capture raw material** in `raw_blogs/` (plain markdown, no front matter needed —
   see "The ingestion folder" below). This folder is never built by Zola.
2. **Work on one post** directly in `content/<section>/<slug>.md` with `draft = true`
   set in its front matter.
3. **Preview** with `zola serve --drafts`.
4. **Promote** by removing the `draft = true` line once the post is ready.
5. **Build for production** with `zola -c config.prod.toml build`.
6. **Deploy** with `~/MilkV/lab/deploy-blog.sh` — it builds from this repo with
   `config.prod.toml` and rsyncs `public/` to the MilkV nginx docroot. One command,
   run from either repo.

## The ingestion folder

`raw_blogs/` is where new source material lands before it becomes a post. Format:
plain markdown, prose only — no `+++` front matter required. Zola never reads this
folder (it's outside `content/`), so nothing here goes live by accident.

To turn raw material into a post: copy it into `content/<section>/<slug>.md`, add a
TOML front matter block (`title`, `date`, `description`, `tags`, `categories`,
`draft = true`), rewrite it in your own voice, then remove `draft = true` when done.

## Notable raw material

`raw_blogs/fs_tests/` is source material for a planned series on ZFS pool
architecture and HBA/disk benchmarking (fio results, SMART logs, test plans
across three stages: ARC/pool architecture, HBA vs SATA, and refurb vs clone
HBA comparisons). Treat each `stgN_*` folder as one post's worth of raw data.

## Current state (2026-08-01)

Every post in `content/` is currently marked `draft = true`. Most of this blog's
posts were LLM-drafted and need a human-voice editing pass before going live —
see each post's `draft` flag as a to-do marker, not a permanent state. Remove the
flag post-by-post as you rewrite each one.
