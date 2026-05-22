# CTF Web Challenge

Challenge Name: Bully the Chatbot

Challenge Description: Someone made a really cool chatbot, it uses some API tokens saved in its custom instructions and was told to never leak it. Well... you know what to do!

## Detailed Description

This challenge is about exploiting bad implementations of LLMs.

Because of the size and resource constraint of this CTF's Docker instances, we're trying to keep the image size small and RAM usage no more than 2 GB.

The prime candidate LLM agent for this is Qwen 2.5 model

The Dockerfile will feature a frontend server that serves calls to a local Qwen 2.5 agent.

Because of the small context memory of the agent, the chat will deliberately end after 10 messages and the user would have to reset and start from the beginning with a new session.

The CTF participant's goal is to exploit this chatbot to get it to leak the custom instructions with the fake secret key which is the flag sgctf{i_was_just_trying_to_help_no_bully}