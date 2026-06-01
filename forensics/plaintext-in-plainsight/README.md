Plaintext in Plainsight

## Flag
Contained in `solve/flag.txt`

## Message
The IT team has been puzzled by a recurring security incident. An administrator account appears to be repeatedly compromised despite password resets, policy reviews, and assurances that the application is configured according to best practices.

As part of the investigation, a network capture was taken while users interacted with the system. Your task is to review the evidence and determine whether the source of the problem can be identified.

## Files Included
- `challenge.pcap` - Network capture file, open with Wireshark
- `README.md` - This file
- `solve-writeup.md` - Shows the steps and thinking one should take when solving this challenge

## Hints
* Not all traffic is created equal, learn to filter the noise.
* How is the admin account repeatedly compromised despite password resets?
* Wireshark can inspect more than just headers it can read the full request body too.