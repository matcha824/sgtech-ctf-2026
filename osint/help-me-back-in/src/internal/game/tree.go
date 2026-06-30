package game

func buildTree() map[string]*Node {
	tree := make(map[string]*Node)

	add := func(id, dialogue string, choices []Choice) {
		tree[id] = &Node{ID: id, Dialogue: dialogue, Choices: choices}
	}

	// ============================================================
	// TURN 1 — Opening (shared)
	// ============================================================
	add("start",
		"Hi, um, I'm really hoping you can help me. I've been locked out of my account and I have a bill payment due tomorrow. I'm kind of freaking out here.",
		[]Choice{
			{Text: "Oh no, that sounds really stressful! Don't worry, we'll figure this out together. Can you tell me what happened?", NextID: "a2_empathy", SuspDelta: -1, ComfDelta: 2},
			{Text: "I'm sorry to hear that. I've been there myself — let's see what we can do. What were you trying to do when it locked you out?", NextID: "a2_casual", SuspDelta: -1, ComfDelta: 1},
			{Text: "I understand. I'll need to verify some information to help you. Can you start by telling me what error you're seeing?", NextID: "c2_direct", SuspDelta: 1, ComfDelta: 0},
			{Text: "Alright, let me pull up your account and walk you through our standard reset process.", NextID: "b2_procedure", SuspDelta: 0, ComfDelta: 0},
		})

	// ============================================================
	// PATH A — Rapport Building (yields: pet name + birth year)
	// ============================================================

	add("a2_empathy",
		"Oh thank you so much. So I changed my password last week because I read you should do that regularly? And now I just... can't remember what I changed it to. I feel so dumb.",
		[]Choice{
			{Text: "You're not dumb at all! That happens to everyone. I changed mine last month and locked myself out too. Do you remember if you set up any recovery options?", NextID: "a3_recovery", SuspDelta: -1, ComfDelta: 2},
			{Text: "That's totally normal! Hey, at least you're being proactive about security. Did you write the new one down anywhere?", NextID: "a3_wrote_down", SuspDelta: 0, ComfDelta: 1},
			{Text: "I see. I'll need your full name and date of birth to proceed with the reset.", NextID: "c3_verify_direct", SuspDelta: 2, ComfDelta: -1},
			{Text: "No worries. Let me check what recovery options are on your account.", NextID: "b3_check_account", SuspDelta: 0, ComfDelta: 0},
		})

	add("a2_casual",
		"I was just trying to log in to pay my electric bill, and it kept saying 'incorrect password.' Then after like five tries it locked me out completely. Now I can't even try again.",
		[]Choice{
			{Text: "Five tries — I'd be frustrated too! Those lockout timers are the worst. So this is a new password you set recently?", NextID: "a3_recovery", SuspDelta: -1, ComfDelta: 1},
			{Text: "That must be really frustrating, especially with the bill due. Did you maybe have it saved in your browser or a password manager?", NextID: "a3_wrote_down", SuspDelta: 0, ComfDelta: 1},
			{Text: "Got it. I'll need to verify your identity before we can unlock the account. Can you give me your date of birth?", NextID: "c3_verify_direct", SuspDelta: 2, ComfDelta: -1},
			{Text: "Understood. Let me look at what we have on file for your account recovery options.", NextID: "b3_check_account", SuspDelta: 0, ComfDelta: 0},
		})

	add("a3_recovery",
		"Yeah, I think I set up a security question? Something about... I think it was about my pet. I definitely remember doing that when I first made the account. I love my animals, ha.",
		[]Choice{
			{Text: "Aw, you're a pet person! What kind of pets do you have?", NextID: "a4_pet_ask", SuspDelta: 0, ComfDelta: 1},
			{Text: "Great! So you have a security question about your pet. Do you remember what the question asked specifically?", NextID: "a4_question_detail", SuspDelta: 1, ComfDelta: 0},
			{Text: "Perfect. And just to verify I'm speaking with the right person — what was the answer to that security question?", NextID: "a4_pet_ask", SuspDelta: 1, ComfDelta: -1},
			{Text: "Ok, let me look at what security questions you have on file.", NextID: "b5_security_q", SuspDelta: 0, ComfDelta: 0},
		})

	add("a3_wrote_down",
		"No, I didn't write it down. My husband David always tells me to use a password manager but I never got around to setting one up. I just try to use something I'll remember, you know?",
		[]Choice{
			{Text: "Ha, my partner says the same thing to me! So what kind of things do you usually try to remember? Family stuff, hobbies?", NextID: "a4_personal", SuspDelta: 0, ComfDelta: 1},
			{Text: "David sounds like a smart guy! Yeah, password managers are a lifesaver. So since you didn't write it down, do you have a security question set up we could use?", NextID: "a3_recovery", SuspDelta: 0, ComfDelta: 1},
			{Text: "Understood. Well let's see what other options we have. Can you tell me the email address associated with the account?", NextID: "d3_email", SuspDelta: 0, ComfDelta: 0},
			{Text: "I see. I'll need to verify your identity. Can you confirm your full name and date of birth?", NextID: "c3_verify_direct", SuspDelta: 2, ComfDelta: -1},
		})

	// Turn 4A — Pet ask (gated node — resolved by game state)
	add("a4_pet_ask", "", nil)

	// Turn 4A — Pet real answer (comfort >= 7, suspicion <= 4)
	add("a4_pet_real",
		"Oh, I have a cat named Biscuit! She's the sweetest thing. She likes to sit on my keyboard which is probably how I messed up the password in the first place, honestly.",
		[]Choice{
			{Text: "Ha! Biscuit on the keyboard — that's adorable. My cat does the same thing. How long have you had her?", NextID: "a5_biscuit_detail", SuspDelta: -1, ComfDelta: 1},
			{Text: "Biscuit, what a great name! Ok so for the security question, would the answer be Biscuit then?", NextID: "a5_confirm_pet", SuspDelta: 0, ComfDelta: 0},
			{Text: "That's so cute! Hey, while I have you — can I just confirm your date of birth for verification?", NextID: "a5_year_ask", SuspDelta: 1, ComfDelta: 0},
		})

	// Turn 4A — Pet fake answer (suspicion >= 7)
	add("a4_pet_fake",
		"Um... why do you need to know about my pet? Look, I just need my password reset. Can we just do that?",
		[]Choice{
			{Text: "Of course, I apologize. I just wanted to verify the security question answer. Let me find another way to help you.", NextID: "a5_recover_trust", SuspDelta: -1, ComfDelta: 0},
			{Text: "It's for verification purposes. The security question on your account is about your pet.", NextID: "c5_push", SuspDelta: 2, ComfDelta: -1},
			{Text: "No problem at all! Let me look at other options we have.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 0},
		})

	// Turn 4A — Pet vague answer (middle ground)
	add("a4_pet_vague",
		"I have a couple of pets, yeah. Look, is the security question going to help me get back in? I just really need to pay this bill.",
		[]Choice{
			{Text: "Absolutely, that's exactly why I'm asking! If you can confirm the answer to your security question, we can start the reset right away.", NextID: "a5_vague_push", SuspDelta: 1, ComfDelta: 0},
			{Text: "I totally understand the urgency. Let me see if there's a faster way to verify your identity.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
			{Text: "Of course! I know this is stressful. Let's try a different approach — can you tell me the email on file?", NextID: "d4_email_alt", SuspDelta: 0, ComfDelta: 0},
		})

	// Turn 4A — Question detail path
	add("a4_question_detail",
		"I think it was like 'What is your pet's name?' or something like that. Pretty standard.",
		[]Choice{
			{Text: "Got it! And do you remember what you put as the answer?", NextID: "a4_pet_ask", SuspDelta: 0, ComfDelta: 0},
			{Text: "Perfect. So if you can tell me your pet's name, I can verify that against what we have and get you back in.", NextID: "a4_pet_ask", SuspDelta: 1, ComfDelta: 0},
			{Text: "Ok, let me check if that matches what's on file. I'll also need to confirm your date of birth.", NextID: "c3_verify_direct", SuspDelta: 2, ComfDelta: -1},
		})

	// Turn 4A — Personal info path (from wrote_down)
	add("a4_personal",
		"Yeah exactly! I usually base it on things in my life. My daughter Emma just turned 8 this year so I've been thinking about her a lot lately. Time really flies, you know? She was born in 2018 and it feels like yesterday.",
		[]Choice{
			{Text: "Oh wow, 8 already? They grow up so fast! My niece is about that age too. What else keeps you busy?", NextID: "d5_emma_tangent", SuspDelta: 0, ComfDelta: 1},
			{Text: "That's so sweet! So you use personal things like names and dates. Do you remember if you set up a security question when you made the account?", NextID: "a3_recovery", SuspDelta: 0, ComfDelta: 0},
			{Text: "I see. And just to confirm your identity, can you verify your date of birth for me?", NextID: "a5_year_ask", SuspDelta: 1, ComfDelta: 0},
		})

	// Turn 5A — Biscuit detail
	add("a5_biscuit_detail",
		"Oh gosh, I got her right after college! So that's... over ten years now. She was my first pet on my own. She's been with me through everything — moving, getting married, having Emma.",
		[]Choice{
			{Text: "That's such a long time! She sounds like a real companion. So for the security question, the answer would be Biscuit?", NextID: "a5_confirm_pet", SuspDelta: 0, ComfDelta: 0},
			{Text: "Ten years, wow! She's basically family. Hey, I just need to confirm your date of birth to finish up the verification.", NextID: "a5_year_ask", SuspDelta: 0, ComfDelta: 0},
			{Text: "Aw that's so sweet. Getting married, having a kid — sounds like a busy decade! When did you get married?", NextID: "d6_married", SuspDelta: 0, ComfDelta: 1},
		})

	// Turn 5A — Confirm pet
	add("a5_confirm_pet",
		"Yep! Biscuit is my girl. That's definitely what I put for the security question.",
		[]Choice{
			{Text: "Great, that matches what we have! I just need to verify your date of birth and we'll be all set.", NextID: "a5_year_ask", SuspDelta: 0, ComfDelta: 0},
			{Text: "Perfect! Let me get that reset processed for you. You should get an email shortly.", NextID: "a7_end_partial", SuspDelta: 0, ComfDelta: 0},
		})

	// Turn 5A — Year ask (gated)
	add("a5_year_ask", "", nil)

	// Turn 5A — Year real answer
	add("a5_year_real",
		"Sure! March 15th, 1992. I'm a Pisces if that matters, ha!",
		[]Choice{
			{Text: "Ha! I won't hold it against you. Alright, that checks out. Let me get this reset going for you.", NextID: "a6_end_full", SuspDelta: 0, ComfDelta: 0},
			{Text: "Perfect, thank you Sarah! Alright I'm going to start the reset process now.", NextID: "a6_end_full", SuspDelta: 0, ComfDelta: 0},
		})

	// Turn 5A — Year deflect
	add("a5_year_deflect",
		"I'd rather not give that out over the phone if I don't have to. Can you verify me some other way?",
		[]Choice{
			{Text: "Absolutely, no problem! Let me check what other verification methods we have available.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
			{Text: "I understand your concern. Unfortunately date of birth is our standard verification. It's required by our security policy.", NextID: "c5_push", SuspDelta: 2, ComfDelta: -1},
			{Text: "Of course! Can you tell me the last four digits of the phone number on file instead?", NextID: "d5_phone", SuspDelta: 0, ComfDelta: 0},
		})

	// Turn 5A — Vague push
	add("a5_vague_push",
		"Ok fine. I think I put my cat's name. Can we just move forward?",
		[]Choice{
			{Text: "Of course! And that cat's name is...?", NextID: "a5_vague_name", SuspDelta: 1, ComfDelta: -1},
			{Text: "Sure! Just confirm the name for me and I'll get this sorted right away.", NextID: "a5_vague_name", SuspDelta: 1, ComfDelta: 0},
			{Text: "Absolutely. Let me see if I can verify you another way instead.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
		})

	add("a5_vague_name",
		"It's... look, you should have this on file already, right? I shouldn't have to tell you the answer if you work there.",
		[]Choice{
			{Text: "You're absolutely right — we do have it on file. I just need you to confirm it matches. It's a security measure to protect you.", NextID: "a5_vague_final", SuspDelta: 1, ComfDelta: 0},
			{Text: "Fair point! You're right to be cautious. Let me try verifying you a different way.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
		})

	add("a5_vague_final",
		"Fine. Biscuit. It's Biscuit. Can we please move on?",
		[]Choice{
			{Text: "Perfect, that matches! Let me get your reset going now. Thanks for your patience, Sarah.", NextID: "a7_end_partial", SuspDelta: 0, ComfDelta: 0},
			{Text: "Great, thanks! One last thing — can I confirm your date of birth?", NextID: "c6_too_much", SuspDelta: 2, ComfDelta: -2},
		})

	// Turn 5A — Recover trust after suspicion
	add("a5_recover_trust",
		"It's fine, I just... you hear about scams all the time, you know? I want to make sure this is legit.",
		[]Choice{
			{Text: "Absolutely, and you should be cautious! That's really smart. I can give you our callback number if you'd rather call us back to feel safer?", NextID: "a6_trust_rebuilt", SuspDelta: -2, ComfDelta: 2},
			{Text: "I totally understand. We take security very seriously here. Let me find another way to verify your account.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
			{Text: "Of course. But I do need some way to verify you — it's for your protection.", NextID: "c5_push", SuspDelta: 1, ComfDelta: 0},
		})

	add("a6_trust_rebuilt",
		"No, no, it's ok. You seem nice. I'm sorry for being paranoid. What do you need from me?",
		[]Choice{
			{Text: "No need to apologize! Your caution is a good thing. So you mentioned a security question about your pet — do you remember the answer?", NextID: "a4_pet_ask", SuspDelta: 0, ComfDelta: 1},
			{Text: "You're totally fine! So just to verify you, can you confirm your date of birth?", NextID: "a5_year_ask", SuspDelta: 0, ComfDelta: 0},
		})

	// Endings for Path A
	add("a6_end_full",
		"Oh thank goodness! Thank you so much, you've been so helpful. I was really panicking there for a minute. I'll set up that password manager my husband keeps nagging me about, I promise!",
		nil)

	add("a7_end_partial",
		"Thank you! You've been really helpful. I'll keep an eye on my email for the reset link. Have a great rest of your day!",
		nil)

	// ============================================================
	// PATH B — Procedural (yields: hint format + punctuation)
	// Players must navigate a proper support flow before Sarah
	// eventually recalls her own hint. We don't just "read it to her."
	// ============================================================

	add("b2_procedure",
		"Oh, ok great. Yes please. I just need to get back in — I have a bill due tomorrow.",
		[]Choice{
			{Text: "Understood. First, can you confirm the email address associated with your account?", NextID: "b3_email", SuspDelta: 0, ComfDelta: 0},
			{Text: "No problem. I'll need to verify your identity first. Can you confirm your full name as it appears on the account?", NextID: "b3_name", SuspDelta: 0, ComfDelta: 0},
			{Text: "Of course. Let me look up your account. Can you give me a moment?", NextID: "b3_check_account", SuspDelta: 0, ComfDelta: 0},
			{Text: "That's stressful! Don't worry, we'll get this sorted quickly. Tell me what happened?", NextID: "a2_empathy", SuspDelta: -1, ComfDelta: 1},
		})

	add("b3_email",
		"Sure, it's sarah.mitchell@email.com.",
		[]Choice{
			{Text: "Great, that matches. I can see a few recovery options on your account. Let me walk you through them.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "Perfect, confirmed. I can see your account. For security, can you also confirm your full name?", NextID: "b4_verify_name", SuspDelta: 0, ComfDelta: 0},
			{Text: "Thanks Sarah. And can you confirm your date of birth for additional verification?", NextID: "b4_dob_check", SuspDelta: 1, ComfDelta: 0},
		})

	add("b3_name",
		"Sarah Mitchell. M-I-T-C-H-E-L-L.",
		[]Choice{
			{Text: "Thank you, confirmed. And the email on the account?", NextID: "b4_verify_email", SuspDelta: 0, ComfDelta: 0},
			{Text: "Perfect. I can see your account now. Let me check what recovery options are available.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "Great, thank you. And your date of birth?", NextID: "b4_dob_check", SuspDelta: 1, ComfDelta: 0},
		})

	add("b3_check_account",
		"Ok, thank you. I appreciate you looking into this.",
		[]Choice{
			{Text: "I can see your account. Just to confirm I'm looking at the right one — what's the email associated with it?", NextID: "b4_verify_email", SuspDelta: 0, ComfDelta: 0},
			{Text: "I've got it pulled up. Let me check what recovery options you have available.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "Found it. Can you confirm the full name on the account so I know I'm looking at the right one?", NextID: "b4_verify_name", SuspDelta: 0, ComfDelta: 0},
		})

	add("b4_verify_email",
		"sarah.mitchell@email.com.",
		[]Choice{
			{Text: "Confirmed. Let me look at your recovery options now.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "Great, that matches. Can you also confirm your full name for me?", NextID: "b4_verify_name", SuspDelta: 0, ComfDelta: 0},
		})

	add("b4_verify_name",
		"Sarah Mitchell.",
		[]Choice{
			{Text: "Perfect. Let me check what recovery options you have set up.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "Confirmed. And your date of birth for final verification?", NextID: "b4_dob_check", SuspDelta: 1, ComfDelta: 0},
		})

	add("b4_dob_check",
		"March 15th, 1992.",
		[]Choice{
			{Text: "Confirmed, thank you. Now let me check what recovery options are on your account.", NextID: "b5_recovery_opts", SuspDelta: 0, ComfDelta: 0},
			{Text: "Great, that checks out. I can see you have a security question set up. Would you like to try that?", NextID: "b5_security_q", SuspDelta: 0, ComfDelta: 0},
		})

	add("b4_options",
		"Ok, what are my options?",
		[]Choice{
			{Text: "You have a security question set up, and I can also see there's a password hint on file. Which would you like to try first?", NextID: "b5_recovery_opts", SuspDelta: 0, ComfDelta: 0},
			{Text: "We can send a reset link to your email, or we can try your security question. What do you prefer?", NextID: "b5_recovery_opts", SuspDelta: 0, ComfDelta: 0},
			{Text: "I can see a security question on your account. Want to try answering that to verify your identity?", NextID: "b5_security_q", SuspDelta: 0, ComfDelta: 0},
		})

	add("b5_recovery_opts",
		"A password hint? I forgot I even set one of those up. Let's try the security question first though — I think I know it.",
		[]Choice{
			{Text: "Sure! Go ahead — what do you think the answer is?", NextID: "b6_sq_attempt", SuspDelta: 0, ComfDelta: 0},
			{Text: "Of course. Take your best guess at the answer.", NextID: "b6_sq_attempt", SuspDelta: 0, ComfDelta: 0},
			{Text: "Ok! If the security question doesn't work we can fall back to the hint. Ready when you are.", NextID: "b6_sq_attempt", SuspDelta: 0, ComfDelta: 0},
		})

	add("b5_security_q",
		"Sure, I'll try the security question. I think I remember what I put... maybe?",
		[]Choice{
			{Text: "Go ahead — what's your answer?", NextID: "b6_sq_attempt", SuspDelta: 0, ComfDelta: 0},
			{Text: "Take your best guess!", NextID: "b6_sq_attempt", SuspDelta: 0, ComfDelta: 0},
		})

	add("b6_sq_attempt",
		"Ok, is it... hmm. Actually I'm not sure now. I set this up years ago and I can't remember what I put. Can we try the hint instead?",
		[]Choice{
			{Text: "Of course! Let me pull up your password hint. It says you set a hint when you created your account. Do you remember what you might have written?", NextID: "b6_hint_prompt", SuspDelta: 0, ComfDelta: 0},
			{Text: "No problem. Let me read you the password hint you set up. Give me one moment...", NextID: "b6_hint_think", SuspDelta: 0, ComfDelta: 0},
			{Text: "No problem. That didn't match what we have, but let's try the hint instead.", NextID: "b6_hint_prompt", SuspDelta: 0, ComfDelta: 0},
		})

	add("b6_hint_prompt",
		"Honestly I barely remember setting it up. I think I wrote something about what my password is made of? Like a reminder to myself about the format?",
		[]Choice{
			{Text: "That's helpful! Can you try to remember what format you described? Like what pieces you put together?", NextID: "b7_hint_recall", SuspDelta: 0, ComfDelta: 0},
			{Text: "Ok, take your time. What do you think you would have written as a reminder to yourself?", NextID: "b7_hint_recall", SuspDelta: 0, ComfDelta: 0},
			{Text: "No rush. Think about it — what kind of things do you usually put in passwords?", NextID: "b7_hint_recall", SuspDelta: 0, ComfDelta: 0},
		})

	add("b6_hint_think",
		"Oh right, the hint! Let me think... I remember writing something about what my password is made of, like a note to future me about the structure. Give me a second...",
		[]Choice{
			{Text: "Take your time! No rush at all.", NextID: "b7_hint_recall", SuspDelta: 0, ComfDelta: 0},
			{Text: "Of course. Does anything come to mind about what you might have written?", NextID: "b7_hint_recall", SuspDelta: 0, ComfDelta: 0},
		})

	// Turn 7B — Hint recall (gated — needs proceduralN >= 3 and suspicion <= 3)
	add("b7_hint_recall", "", nil)

	add("b7_hint_real",
		"Oh! I remember now. I wrote something like 'sgctf{petname_year_specialcharacter}' — I know, weird format, but I thought it was clever at the time. Like a little code to myself. And I remember I stuck some random symbol at the end for security, like they always tell you to do. Ok I think I've got it from here — thank you so much for walking me through all that!",
		nil)

	add("b7_hint_fail",
		"Ugh, I really can't remember what I wrote. Something about... I don't know. I'm sorry, this is so frustrating. Can you just send me a reset link to my email instead?",
		[]Choice{
			{Text: "Of course! I'll send that reset link now. You should receive it within a few minutes.", NextID: "b8_end_reset", SuspDelta: 0, ComfDelta: 0},
			{Text: "No problem at all. I'll get that reset link sent over right now.", NextID: "b8_end_reset", SuspDelta: 0, ComfDelta: 0},
		})

	add("b8_probe",
		"I think I can work it out from here. Thank you so much for your patience — you've been really helpful!",
		nil)

	add("b8_end",
		"Thank you so much! I think I can figure it out from here. You've been really helpful — I appreciate your patience walking me through all that!",
		nil)

	add("b8_end_reset",
		"Thank you! I'll watch for that email. You've been really helpful, have a great day!",
		nil)

	// ============================================================
	// PATH C — Aggressive / Direct (yields: red herrings)
	// ============================================================

	add("c2_direct",
		"Um, it just says 'Account Locked.' Look, I just need someone to reset it for me.",
		[]Choice{
			{Text: "I understand. But for security, I need to verify your identity first. What is your full name, date of birth, and the last four of your social?", NextID: "c3_heavy_verify", SuspDelta: 3, ComfDelta: -2},
			{Text: "Right. I'll need to confirm some details. Can you start with your date of birth?", NextID: "c3_verify_direct", SuspDelta: 1, ComfDelta: -1},
			{Text: "Got it. Well, let me see what I can do. Do you have your account number handy?", NextID: "c3_account_num", SuspDelta: 1, ComfDelta: 0},
			{Text: "No worries! Let me see what recovery options we have for you.", NextID: "b3_check_account", SuspDelta: -1, ComfDelta: 1},
		})

	add("c3_heavy_verify",
		"Excuse me? My social security number? I'm not giving that out over the phone. Who is this?",
		[]Choice{
			{Text: "I apologize, that was our old verification process. We don't need that anymore. I'm sorry for the confusion.", NextID: "c4_backtrack", SuspDelta: -1, ComfDelta: 0},
			{Text: "Ma'am, this is standard procedure for account recovery. I need to verify your identity.", NextID: "hangup", SuspDelta: 3, ComfDelta: -2},
			{Text: "You're right, I'm sorry. We only need your date of birth and email. I apologize for the confusion.", NextID: "c4_backtrack", SuspDelta: -1, ComfDelta: 0},
		})

	add("c3_verify_direct",
		"March 15th, 1992. Can we speed this up?",
		[]Choice{
			{Text: "Of course. Now I need your full address on file.", NextID: "c4_address", SuspDelta: 1, ComfDelta: -1},
			{Text: "Thank you, confirmed. Now, what's the name of your pet? That's your security question.", NextID: "c4_pet_direct", SuspDelta: 2, ComfDelta: -1},
			{Text: "Perfect, confirmed! Good news — I can see your account. Let me check your recovery options.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
		})

	add("c3_account_num",
		"I don't know my account number off the top of my head. That's part of the problem — I can't log in to see it.",
		[]Choice{
			{Text: "No problem. I can look you up by email. What's the email on your account?", NextID: "b3_email", SuspDelta: 0, ComfDelta: 0},
			{Text: "Ok, then I'll need to verify you another way. Date of birth?", NextID: "c3_verify_direct", SuspDelta: 1, ComfDelta: 0},
			{Text: "That's ok! Let me search by your name. And I'll need your street address to confirm.", NextID: "c4_address", SuspDelta: 1, ComfDelta: -1},
		})

	add("c4_backtrack",
		"Ok... I'm just going to give you my date of birth and that's it. March 15th, 1992. Is that enough?",
		[]Choice{
			{Text: "Yes, that's perfect! Thank you. I can see your account now. Let me check your recovery options.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
			{Text: "Thank you. Now I also need to confirm your mother's maiden name.", NextID: "c5_mother", SuspDelta: 2, ComfDelta: -2},
			{Text: "That's all I need. Let me pull up your recovery options.", NextID: "b4_options", SuspDelta: -1, ComfDelta: 0},
		})

	add("c4_address",
		"47 Maple Avenue. Look, is this going to take much longer? I feel like I'm getting the runaround here.",
		[]Choice{
			{Text: "I apologize for all the questions. Good news — I have your account now. Let me check your recovery options.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
			{Text: "Almost done. One more thing — what's the name on the account?", NextID: "c5_push", SuspDelta: 1, ComfDelta: -1},
			{Text: "I understand, I'm sorry. Let me get right to it — I can see a few recovery options for you.", NextID: "b4_options", SuspDelta: -1, ComfDelta: 1},
		})

	add("c4_pet_direct",
		"Why do you need that? I thought you were going to reset my password, not quiz me.",
		[]Choice{
			{Text: "It's your security question — I need the answer to verify your identity and authorize the reset.", NextID: "c5_pet_push", SuspDelta: 1, ComfDelta: -1},
			{Text: "You're right, I'm sorry. Let me try a different approach — let me check your recovery options.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
			{Text: "I apologize. It's just part of our security process, but I can verify you another way.", NextID: "b5_recovery_opts", SuspDelta: -1, ComfDelta: 1},
		})

	add("c5_mother",
		"Rodriguez, but I really don't understand why you need all of this. This is making me uncomfortable.",
		[]Choice{
			{Text: "I understand your concern. That's all the verification I need — let me get your account reset going.", NextID: "c6_end_red_herring", SuspDelta: 0, ComfDelta: 0},
			{Text: "I apologize for the inconvenience. It's just for your security. We're almost done.", NextID: "c6_end_red_herring", SuspDelta: 0, ComfDelta: 0},
		})

	add("c5_push",
		"I already told you my name is Sarah Mitchell! What is going on? This doesn't feel right. I think I'm going to hang up and call back.",
		[]Choice{
			{Text: "I'm sorry for the confusion, Sarah. You're right — I have everything I need. Let me process the reset now.", NextID: "c6_end_red_herring", SuspDelta: 0, ComfDelta: 0},
			{Text: "Ma'am, please don't hang up. I just need one more piece of information.", NextID: "hangup", SuspDelta: 3, ComfDelta: -2},
		})

	add("c5_pet_push",
		"Fine. It's Max. Happy now? Can you just reset my password?",
		[]Choice{
			{Text: "Thank you Sarah. Yes, let me get that reset started for you right now.", NextID: "c6_end_red_herring", SuspDelta: 0, ComfDelta: 0},
			{Text: "Perfect. And just to confirm — is there anything else you remember about your account settings?", NextID: "c6_too_much", SuspDelta: 2, ComfDelta: -2},
		})

	add("c6_too_much",
		"Ok I'm done. You're clearly fishing for information. I'm hanging up and calling back to talk to someone else.",
		nil)

	add("c6_end_red_herring",
		"Thank you. I hope the reset goes through quickly. Goodbye.",
		nil)

	// ============================================================
	// PATH D — Rambler Dead End (yields: lots of noise)
	// ============================================================

	add("d3_email",
		"Sure, it's sarah.mitchell@email.com. I've been meaning to switch to a new email actually but you know how it is — everything is connected to this one now.",
		[]Choice{
			{Text: "Oh I know exactly what you mean! I've been wanting to switch mine for years. So what do you do that has you tied to so many accounts?", NextID: "d4_job", SuspDelta: 0, ComfDelta: 1},
			{Text: "Ha, yeah that's the modern problem isn't it! Well good news — I can see your account with that email. Want me to check your recovery options?", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "I totally get it. Ok so with that email I can pull up your account. Let me see what we've got.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
		})

	add("d4_job",
		"I'm an elementary school teacher! So I've got my school email, personal email, all the educational platform logins... it's honestly a nightmare. My students are better with technology than I am half the time.",
		[]Choice{
			{Text: "Ha! That's so true about kids these days. What grade do you teach?", NextID: "d5_grade", SuspDelta: 0, ComfDelta: 1},
			{Text: "Oh wow, teachers are so underappreciated! That must keep you really busy. Hey, let me get you back into your account so you have one less thing to worry about.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 1},
			{Text: "All those passwords to remember! No wonder you got locked out. Let me check your recovery options.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
		})

	add("d4_email_alt",
		"sarah.mitchell@email.com.",
		[]Choice{
			{Text: "Thanks! I can see your account. You have a few recovery options — want me to walk you through them?", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "Got it. Let me pull up your account and see what we can do.", NextID: "b5_recovery_opts", SuspDelta: 0, ComfDelta: 0},
		})

	add("d5_grade",
		"Third grade! They're at that age where they're so curious about everything. One of my students asked me last week if passwords are 'like codes for spies.' I told her yes, basically!",
		[]Choice{
			{Text: "Ha! That's adorable. Third graders are the best. Does your daughter go to the same school?", NextID: "d6_daughter", SuspDelta: 0, ComfDelta: 1},
			{Text: "That's hilarious and also kind of accurate! Hey, speaking of passwords — let me check on yours.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "Kids say the funniest things! Ok so let me get back to helping you with this account.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
		})

	add("d5_emma_tangent",
		"Ha, maybe! Between Emma and my pets and our anniversaries, I have a lot of dates and names to keep track of. Sometimes I get confused about which one I used for what.",
		[]Choice{
			{Text: "That's the eternal password struggle! When did you and your husband get married?", NextID: "d6_married", SuspDelta: 1, ComfDelta: 0},
			{Text: "I totally get that. Well let me check what recovery options you have on your account.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "So many things to remember! Do you recall if you set up a security question when you made the account?", NextID: "a3_recovery", SuspDelta: 0, ComfDelta: 0},
		})

	add("d5_phone",
		"Um, I think it ends in 4832? Or wait, that might be David's. Sorry, we got on a family plan and I always mix them up.",
		[]Choice{
			{Text: "No worries! Let me try a different approach. Let me check your recovery options.", NextID: "b5_recovery_opts", SuspDelta: 0, ComfDelta: 0},
			{Text: "Family plans can be confusing! That's ok. Let me verify you another way.", NextID: "b5_recovery_opts", SuspDelta: 0, ComfDelta: 0},
		})

	add("d6_daughter",
		"No, she goes to Westbrook Elementary across town. I teach at Lincoln. I like keeping work and family a little separate, you know? Though David picks her up from my school sometimes when schedules get crazy.",
		[]Choice{
			{Text: "Smart move keeping things separate! Ok Sarah, let me get you back into your account. Let me pull up your recovery options.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "That makes total sense! Do you guys live close to both schools?", NextID: "d7_location", SuspDelta: 0, ComfDelta: 1},
			{Text: "I totally understand that. Hey, we've been chatting and I almost forgot — let me actually help you with your account!", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
		})

	add("d6_married",
		"2016! It was a beautiful fall wedding. David wanted spring but I won that argument, ha. We went to Cancun for the honeymoon — I still dream about those beaches.",
		[]Choice{
			{Text: "Cancun sounds amazing! Fall weddings are the best. Ok, let me check your account recovery options.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "A fall wedding in 2016, how lovely! Hey, let me get you back into your account so you can get that bill paid.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
		})

	add("d7_location",
		"Yeah, we're on Maple Avenue — pretty central to everything. It's a great neighborhood for kids. Anyway, I'm so sorry, I've been rambling! You're so easy to talk to. I still need to get into my account, don't I?",
		[]Choice{
			{Text: "Ha, no worries at all! You're lovely. Let me pull up your recovery options now.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
			{Text: "Not rambling at all! Let me pull up your account options now.", NextID: "b4_options", SuspDelta: 0, ComfDelta: 0},
		})

	// ============================================================
	// SPECIAL NODES
	// ============================================================

	add("hangup",
		"You know what? Something doesn't feel right here. I'm going to hang up and call back on the official number. Goodbye.",
		nil)

	return tree
}
