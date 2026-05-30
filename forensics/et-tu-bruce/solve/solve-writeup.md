# Solve Writeup
##Overview
This challenge relies primarily on audio steganography with a bit of cryptography at the end

## Audio Steganography
The message in this audio is very obvious cause I didn't wanna make the text too hard to see, but what may confuse people is how to get the embedded message out.

It has nothing to do with actually listening to the audio. To get the message out of the .wav file, you need to open it in Audacity or some other application that allows you to see the spectograph of a wav file.

Once in audacity, you may need to play with the settings a bit to clearly see the text in "Spectograph Settings", but for me opening the Spectograph view was good enough.

You should see the message **os_ut_loxkcgrr**

## Cryptography 
This obviously isn't plain text, but a Caesar cipher (as hinted to by the challenge title). Putting this into a decoder or doing it yourself will get you **im_on_firewall**, the flag for this challenge.
