+++
title = "Exploring Options: Needs and Wants in a Home Network"
date = "2025-01-19"
draft = true
description = "Once I admitted my network was held together with 100-megabit string, the temptation was immediate: rebuild it all, but better, faster, shinier. This is where the fun begins, and also where the danger lies."
tags = ['networking', 'planning', 'home-lab', 'vlan', 'infrastructure', 'design']
categories = ["technical"]
+++

## Exploring Options: Needs and Wants in a Home Network

Once I admitted my network was held together with 100-megabit string, the temptation was immediate: rebuild it all, but better, faster, shinier. If I was going to crawl through the loft again, I might as well pull fibre everywhere, right? Maybe put in a rack the size of a fridge, give the solar panels their own VLAN, and run a LORA gateway for good measure.

This is where the fun begins, and also where the danger lies. Planning a network is a lot like kitchen design — you can either add just enough counter space to chop the vegetables, or you can dream yourself into a marble-topped fantasy with six ovens and a dumbwaiter. I wanted everything: VLANs for guests, VLANs for kids, an "untrusted" net for the TV, a proper backup box in the garage, and a utility network for the solar inverter, battery, and car charger. I also wanted a loft stuffed with toys: a software-defined radio, a weather station, maybe even a LORA backhaul to something mysterious and futuristic.

But needs are not wants. Most days the "need" was simple: my wife and I should be able to open a laptop and get on the internet without watching a spinning wheel. The NAS should talk to the printer without sulking. The kitchen Raspberry Pi should stream music without lagging out. Everything beyond that was ambition.

So I started a list. At the top: "every machine gets gigabit." Below that: "backhaul might need to be 10-gig in places, but maybe fibre is overkill." Then: "do I want one big switch with miles of cable, or a set of smaller managed switches closer to where they're needed?" And, in brackets: "can I get away without my partner noticing the rack growing legs?"

It's easy to drift off into the clouds of "what if." What if I turn off the FritzBox Wi-Fi and install proper access points? What if I put the garage on its own utility network? What if I swap the ISP router for my home-built box? Each of these questions sounds sensible until you add them all together and realise you've designed something closer to a data centre than a home LAN.

So the job at this stage wasn't just making a shopping list. It was interrogating myself: why do I want this feature? What am I really trying to solve? Fibre in the loft wasn't about speed — no laptop in the house needs more than a gigabit — it was about interference and peace of mind. VLANs weren't about performance, they were about learning, and maybe keeping the smart TV from talking to the NAS in the dead of night. A better access point wasn't urgent, but moving the one I already owned into a sensible position probably was.

This is the stage where "blue sky thinking" turns into grounded planning. Not everything belongs in the first rebuild. Some features can wait for version two, or three. But writing down the dreams is still worthwhile, because a network is never truly finished. It grows with the house, the people, and, if you're not careful, the number of Raspberry Pis hiding in the loft.
