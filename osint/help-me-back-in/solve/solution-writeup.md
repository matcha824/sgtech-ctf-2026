# Help me back in

This challenge is a little different in that you're given an executable file, which prompts you with different options to talk to Sarah. Based on the options you choose, you will get different responses. In addition to this, there is also some trial and error you must do in order to guess the flag.

### 1. Find the flag format

We want to go down a conversation path that leads us to the password clue. This requires some trial and error on the player part, but I'm listing a flow you can use to get the answer:

- (4) Alright, let me pull up your account and walk you through our standard reset process
- (1) Understood. First, can you confirm the email address associated with your account?
- (2) Perfect, confirmed. I can see your account. For security, can you also confirm your full name?
- (1) Perfect. Let me check what recovery options you have set up.
- (3) I can see a security question on your account. Want to try answering that to verify your identity?
- (1) Go ahead — what's your answer?
- (1) Of course! Let me pull up your password hint. It says you set a hint when you created your account. Do you remember what you might have written?
- (1) That's helpful! Can you try to remember what format you described? Like what pieces you put together?

After this series of paths, you will get this reponse from Sarah giving you the flag format:
```
Sarah: Oh! I remember now. I wrote something like 'sgctf{petname_year_specialcharacter}' — I know, weird format, but I thought it was clever at the time. Like a little code to myself. And I remember I stuck some random symbol at the end for security, like they always tell you to do. Ok I think I've got it from here — thank you so much for walking me through all that!
```

### 2. Find the password values

Now that you have the flag format, you are looking the petname and a year to use as your guess. 

### Pet name
- (3) I understand. I'll need to verify some information to help you. Can you start by telling me what error you're seeing?
- (2) Right. I'll need to confirm some details. Can you start with your date of birth?
- (2) Thank you, confirmed. Now, what's the name of your pet? That's your security question.
- (1) It's your security question — I need the answer to verify your identity and authorize the reset.

After this series of paths, you will get this response from Sarah giving you the pet name:

```
Sarah: Fine. It's Max. Happy now? Can you just reset my password?
```

### Year
- (1) Oh no, that sounds really stressful! Don't worry, we'll figure this out together. Can you tell me what happened?
- (2) That's totally normal! Hey, at least you're being proactive about security. Did you write the new one down anywhere?
- (1) Ha, my partner says the same thing to me! So what kind of things do you usually try to remember? Family stuff, hobbies?
- (1) Oh wow, 8 already? They grow up so fast! My niece is about that age too. What else keeps you busy?
- (1) That's the eternal password struggle! When did you and your husband get married?

After this series of paths, you will get this response from Sarah with her wedding year:
```
Sarah: 2016! It was a beautiful fall wedding. David wanted spring but I won that argument, ha. We went to Cancun for the honeymoon — I still dream about those beaches.
```

### 4. Assemble the flag!

You now have the pet name and the year. Now you just need to guess the special character symbol. You just need to brute force the special characters like `!, @, #, $, %, etc...` but the correct one is `!`

Flag is in the format `sgctf{petname_year_specialcharacter}`. So answer is `sgctf{Max_2016_1}`

### 5. Erroneous findings

This is designed to make players find the wrong information. Most notably, some paths will have Sarah talk about her other pet `Biscuit` and some other years like her birth year and her daughter's birth year. In total there are 2 pet names to find and 3 years to find, making a total of 6 base combinations. Player then has to guess the special characer at the end for final answer. This creates possibly around 60+ combinations of answers depending on how many a player goes through.