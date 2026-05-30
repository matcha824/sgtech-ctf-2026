# Overview
This challenge combines two basic concepts found in many OSINT challenges during CTFs.

The first one is reverse image searches. You should be able to find the location of the Whole Foods in the image through reverse image searching. The second is what3words.com. This site is found a lot in OSINT challenges since it's a way people concisely talk about locations online while keeping things easy to remember (compared to traditional coordinates) and somewhat discreet.

## Reverse Image Search
When using google reverse image search to reverse search whole-foods.jpg, Google AI actually told me which Whole Foods it was, the **Union Square Whole Foods**. Even barring this, the reverse search should bring up a couple news articles with photo credits citing the image as the Union Square location.

## Connecting the Dots
The challenge description explicitly mentions what you're searching for, a Capital One Cafe, presumably nearby this whole foods. If you look at Union Square Whole Foods on Google Maps, you can see a Capital One Cafe exists just next door.

## What 3 Words
Navigating to **what3words.com** now, it allows you to input a address directly into it's search box. Doing this will give you the three words (aka the text-based coordinates) of the exact address of this C1 cafe. These three words are your flag: **drag.plot.useful**.
