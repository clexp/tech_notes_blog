+++
title = "Information Gathering: Comparing Switch Hardware — When 'Why' Matters"
date = "2025-01-19"
description = "Once I had admitted the old Planet 10/100 switches had to go, the obvious question was: what next? A switch is a switch, right? Eight ports, some blinking lights, and away you go. Except no — once you start comparing models, you realise there are whole families of switches out there."
tags = ['networking', 'switches', 'hardware', 'planning', 'vlan', 'enterprise', 'home-lab']
categories = ["technical"]
+++

## Information Gathering: Comparing Switch Hardware — When 'Why' Matters

Once I had admitted the old Planet 10/100 switches had to go, the obvious question was: what next? A switch is a switch, right? Eight ports, some blinking lights, and away you go. Except no — once you start comparing models, you realise there are whole families of switches out there, from the £20 "plug-and-play" box you buy at the supermarket to the £2,000 enterprise beast with dual power supplies and a fan that sounds like a small jet.

I began with the obvious cheapies. The TP-Link TL-SG108S, for instance. Eight gigabit ports, dead simple, and at under £25, it's cheaper than some patch cables. The problem? It's unmanaged. Plug in a trunk carrying multiple VLANs and it just floods every tagged packet everywhere. Perfect for a kids' study with a few laptops, but useless if you want to isolate the smart TV or prune VLANs in the loft.

Then there are the "smart managed" switches. Netgear's GS308E, ZyXEL's GS1200-8, or D-Link's DGS-1100. These give you just enough VLAN awareness to shape traffic, usually via a web GUI. The Netgear feels a little clunky in its interface, the ZyXEL is bargain-basement, but the D-Link surprised me. Thirty-five pounds and yet it offers a proper CLI, telnet access, user accounts, even the ability to disable the web GUI for security. That's edging into small-business territory, not just hobbyist kit.

At the top of my shortlist sat the TP-Link SG3428. Twenty-four gigabit ports, four SFP cages for fibre, and a Cisco-like CLI you can actually practice CCNA syntax on. It's overkill for most homes, but this is the core of my rebuild — the box in the rack that ties everything together. At ~£140 it's a fraction of Cisco pricing, but it feels "enterprise enough" to matter.

And then, off to the side, lurked MikroTik. Their CRS112 and CRS326 aren't just switches, they run RouterOS — a full-blown network OS you can script, firewall, and even run routing protocols on. That's both exciting and terrifying. They're the lab gear: more Unixy, more configurable, but more likely to eat an evening when a mis-typed command turns the lights off.

The question I kept coming back to wasn't just what can this switch do? but why do I care? VLANs mattered because I wanted to isolate the TV and learn CCNA basics. SFP cages mattered because I wanted fibre up the chimney, not because my laptops need 10G. A full-blown MikroTik firewall-on-a-switch? Interesting, but not necessary for the kitchen Raspberry Pi.

That's when the "why" trumped the "what." Instead of blanketing the house in enterprise gear, I picked my battles. One strong core switch with a CLI to learn on, a couple of capable edges (DGS-1100s) where VLANs matter, and a few dumb SG108S boxes where they don't. Enough enterprise to stretch my skills, but not enough to bankrupt the project.

Sometimes the most important spec sheet is the one you write yourself: what the switch is for, why it matters, and when "good enough" really is good enough.
