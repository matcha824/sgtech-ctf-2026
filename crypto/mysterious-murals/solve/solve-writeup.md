# Mysterious Murals Solution

### 1. Identify the encryption type

The image features a clue about Joan & Vincent, who are the creators of AES encryption. Google search like Joan & Vincent crypto will give you results about AES.

### 2. Find the AES values

The IV value for this is actually on the picture as "mysteriousmurals". The secret key is harder, but this is embedded in the actual image metadata `Source` field. Upon doing a textdump of the image metadata, the value for `Source` should look a little strange, which will hint you that you should do something with this value. 

My recommendation would be to just cyberchef this value using Magic to find the key value. Alternatively, you can try different decoding options, but in this case the secret key was encoded with base85.

### 3. Decrypt!

I would once again recommend using CyberChef for this for ease. You can choose [AES Decrypt to solve](https://gchq.github.io/CyberChef/#recipe=AES_Decrypt(%7B'option':'UTF8','string':'capturetheflag26'%7D,%7B'option':'UTF8','string':'mysteriousmurals'%7D,'CBC','Hex','Raw',%7B'option':'Hex','string':''%7D,%7B'option':'Hex','string':''%7D)&input=NjZjZDdjZjUwZjAyOGNiZWE0YzRjYjQ2Njc2ZWMxMGRjODA0NmMwYjQzYTk0MWY3ODgxZjNhMjAxMTIzYzVkOA). It's important to note that you need to switch to UTF8 instead of using Hex for both key and IV to properly get the value.

### 4. Assemble the flag!

Flag is in the format `sgctf{decryptedmessage}`. So answer is `sgctf{hiding.in.plain.sight}`