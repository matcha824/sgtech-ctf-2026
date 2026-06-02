# Name
Key in C Minor

# Description
A transmission was sent from one of our agents using AES-128-CBC with a constant key. However, our data corrupted, and we only have the last 100 bits of the key! Can you recover the full key and decrypt the flag?

Here's what we know:
The encrypted flag is `cc818157d555903066386d07b7db51d842a05de9e8e432facc31822319d7813d`
The IV is `abababababababab0101010101010101`
The last 100 bits of the key are `-------b3c4d5e6f7890abcdef123456` (where the dashes are unknown values)

(Hint: If the program is taking too long, consider writing in a more efficient language like C or Java)