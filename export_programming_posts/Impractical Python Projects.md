+++
title = "Impractical Python Projects"
date = "2025-01-01"
description = "Review of the book"
tags = ['Python']
categories = ["technical"]
+++


On the reviews this look like a great book. It covered a range of popular topics to some level and it's clearly a follow one book from earlier Python learning books. I was particularly excited about the use of base theorem, genetic algorithms and encryption. But there was much more in here much more that I learned about probability science and unknown areas.

### Chapter 01: Sensible Name Generator
This was a nice simple randomising name generator. The goal was to generate silly names but I modified it to generate real names. I modified it to scoop data from various websites including the office of national statistics about Colin first names in the UK. I added a couple of extra libraries to format the text better.

What I haven't really covered before with style guides. Particularly pate and pep 257 for formatting Dock streams. I covered pilot and covering a config file. I learnt about the 79 character limit, which I always thought was a bit ridiculous. I previously thought we have giant wide screens why are we worried about 79 character limits, surely this is for when you use Terminal to SSH into another host. Interestingly, it was the chatbot and not the book that explained that if you have a wide screen and you're comparing to text files keeping the width to just 79 is helpful. However, different organisations have different standards.

What I mean by this is pep eight doesn't recommend 79 characters. It recommends 79 characters for code and 72 characters for dark strings and comments. I thought this was about consistency? Many modern teams recommend 88 characters which is the default for black format or 100 characters since modern screens are wider. The limit of 79 characters is probably a soft recommendation.

There was an interesting challenge projects at the end, which I've actually think I've done previously through the exorcism project. See my Exercism repo.

### Chapter 02: Palingrams
Now I have done this before on the exorcism pathway, however I'm undoubtedly going to learn lots of surrounding extras.

The initial palindrome was very easy, and the palingram was easier than I thought it would be.  I did have a GIANT dictionary made from 6-7 sources, so it went on for a long time and made a HUGE list of mainly meaningless palingrams.  Some of the dictionaries have many 2 and 3 letter words that are debatably words but have a high likelyhood of being palindromes.  

The request getting and formatting the source files was made so much easier by AI, that I went over and above here and learnt about pickle files and unpacking zip files.  You can say what you like about AI, but I am learning faster, a different way.  

What was interesting were the speed tests, I knew this was slow, but I did not realise how slow.  I had to do 174159 word check on 174159 words. That is 174159 * 174159, that's 21.7 billion word reversals.  

First I found a whole function for checking if something was a palindrome.  This could have been just one line, not a whole frame on the stack and mem allocation.  

This made it from 200+168 seconds down to 175 seconds.  Python likes one-liners.

Then we looked at repeated word reversals.  We just reversed all the words once and stored them in the table.  Then we used this as a quick lookup.  This took us down to 89 seconds.  

That is a real learning point, I have not used cProfile before.  

I moved over to time() directly.  We next removed any word pairs not of the same length.  This however would rule out palingrams from different lengthes looking back we stayed with this change.  using time the time increased, but I am not sure why this is.  Time measured the whole file but cProfile just measured the functions.  

The challenge was to do a dictionary cleanup. I put this filter on loading the dictionary file.  

I have previously done the anagram speed test, see my Exercism repo for anagram/ pangram.

The harder challenge was to use a recursive algorithm.  Recursion is where a function calls itself for a smaller version of the same problem.  It this case you really are comparing every word to every word, so there is not a 'smaller' problem you can call.  

There are some 'quit early' options.  For example 'nurses' should only be paired with words ending n and nu and nur.. this would be selective comparison.  I did implement two versions of a palidrome checker, a quitting early algorithm (that could be made recursive), and one using python's reverse list notation.  You can see this in my Exercism repo anagram exercise.  I did this on discussion with a C programmer I hold in high regard.  He advised the quickest route so I thought I would time it.  The python reverse list notation came out quicker.  This is likely because python is doing something clever behind the scenes.  I did not replicate that here.  

I created an example and you can see it in my python teaching repository.  

### Chapter 03: Anagrams
This was very interesting.  From what I previously learnt I could structure the problem in a way that would work.  First you needed to find a word that was an anagram of itself, then find a word that

This is not a great project, I am not sure what I learnt here that I did not learn in Chapter 2.  I learnt that small lists make anagram building tricky, but giant dictionaries are full of dubious words and too big to put on a screen.  

Then it started revealing some simple cryptoanalysis, and I was hooked.  

I want to talk about consonant vowel mapping, trigram frequency and diagram frequency. Cryptographers have long study languages and compile statistics on recurring patterns of words and letters we can use many cryptological tools to identify letter combinations that are more likely to be words.

In trying to generate an anagram from someone's name, it is possible to use a tool like permutations. This will give every possible combination of a given set of things. This could end up with a very large number of possible combinations however most of these will be rubbish. We can filter them using these krypton analytical tools.

### Chapter 04: 