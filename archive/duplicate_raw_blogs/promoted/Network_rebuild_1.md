+++
title = "Old Networks and Technical Debt"
date = "2025-01-19"
description = "The day it really hit me was when I tried to pull a disk image off my server. Eleven megabytes per second. Not bits — bytes. That's USB-2 territory. I sat there watching the progress bar crawl along and realised I was effectively running a 21st-century home server farm on a late-1990s backbone."
tags = ['networking', 'technical-debt', 'home-lab', 'infrastructure', 'planning']
categories = ["technical"]
+++

## Old Networks and Technical Debt

The day it really hit me was when I tried to pull a disk image off my server. Eleven megabytes per second. Not bits — bytes. That's USB-2 territory. I sat there watching the progress bar crawl along and realised I was effectively running a 21st-century home server farm on a late-1990s backbone.

Like most people, I'd been quietly living with the compromises. A FritzBox router in the wrong corner of the living room, a handful of ageing 10/100 switches picked up years ago, a chimney doing double duty as a cable riser, and a loft strung with Cat5 like Christmas lights. It worked, sort of. The NAS spoke to the printer, the laptops found the internet, and the kitchen Raspberry Pi kept streaming music. The fact that every byte in the house was squeezing itself through fast-ethernet bottlenecks… well, I didn't look too closely.

This is technical debt, but at home scale. The problem isn't just that things get slow — it's that we get used to them being slow. We design around the pain instead of fixing the root. I had spent hours carefully scheduling backups and limiting transfers, when the real fix was to stop pretending the Planet SW-804 was still fit for duty.

So this is where the project begins. Not with fancy new servers or cloud integrations, but with asking: why is my network slow? And the answer turned out to be as simple as it was embarrassing: because I built it that way, and then ignored it for a decade.

The plan now is to start from first principles. Map out what I have, what I need, and what I might want in the future. Understand which parts of the sprawl are genuine bottlenecks and which are just messy but harmless. And, above all, rebuild with some thought to the next ten years — not just what gets me through this week's file transfer.

Technical debt doesn't just live in enterprise IT. It grows quietly in lofts, sheds, and behind televisions. My house had plenty, and I finally decided to pay some of it down. This series is the story of how.
