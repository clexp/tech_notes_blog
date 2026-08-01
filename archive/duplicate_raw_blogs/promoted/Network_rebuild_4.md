+++
title = "Radio Interference is a Thing, But How Much of a Thing?"
date = "2025-01-19"
description = "When I first thought about rebuilding the network, I worried a lot about interference. My main cable run goes up a disused chimney, through the loft, and down again to the garage and kitchen. Surely that was a recipe for disaster?"
tags = ['networking', 'interference', 'ethernet', 'fibre', 'cabling', 'electromagnetic']
categories = ["technical"]
+++

## Radio Interference is a Thing, But How Much of a Thing?

When I first thought about rebuilding the network, I worried a lot about interference. My main cable run goes up a disused chimney, through the loft, and down again to the garage and kitchen. It sits near a power cable feeding a 2 kW immersion heater, crosses a loft that hits 30°C on a good summer's day, and runs close to the DC wiring from a solar array. Surely that was a recipe for disaster?

And yet… the Raspberry Pi in the kitchen has been happily streaming music across that very cable for years, never missing a beat. Was interference really the monster under the bed, or just a shadow on the wall?

A little digging made things clearer. Ethernet uses twisted pairs and differential signalling, which cancels out a surprising amount of noise. AC mains can couple interference if you run in parallel for long distances, but cross at 90° and the risk mostly disappears. Loft heat is less about EMI and more about whether your Cat5 sheath softens at 50°C. And solar DC wiring? It doesn't "hum" the way AC does, so the interference is minimal. My neighbour the ham radio enthusiast might lose sleep over powerline networking, but he's not going to care about my Ethernet runs.

So why was I drawn to fibre? Not because I needed ten gigabits to watch Netflix — my AP tops out at one gig anyway. Fibre is immune to electromagnetic noise. It doesn't care about the chimney, the loft, or the solar array. It gives me peace of mind that one bad crimp or one hot day won't suddenly flood my logs with CRC errors. It's less about speed, more about removing one variable from the list of things that could go wrong.

That said, Cat6a is still the workhorse of most networks. Shielded or not, it's good enough for ten gigabits over the kind of distances you find in a house. Crimped properly and routed sensibly, it will shrug off the loft just fine. But fibre in the riser is my insurance policy. If nothing else, it keeps the learning interesting — I get to run SFP modules, play with media converters, and write the kind of blog post you're reading right now.

And because I'm not content with theory alone, I'm running iperf3 across the existing Cat5 loft cable for 24 hours at a time. Every minute it logs throughput, and soon I'll be able to graph day versus night, solar on versus solar off. Maybe it'll prove me right about interference. Maybe it'll prove the cable is better than I gave it credit for. Either way, it will be data, and data makes for a much better story than hunches and paranoia.

So yes, radio interference is a thing. But how much of a thing? Enough to think about, not enough to panic over. The trick is knowing when to spend money on fibre, when to trust twisted copper, and when to stop blaming the loft and admit the real bottleneck is still that old 100-megabit switch behind the TV.
