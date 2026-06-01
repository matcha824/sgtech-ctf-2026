For this challenge, we are given a binary file that takes in an input and compares it to a hardcoded value. However, the hardcoded value is decrypted at runtime and compared to our user input. As such, we can run dynamic analysis tools to determine the value of the flag.

In this case, running `ltrace` shows us the library calls made by the program, including the `strcmp` function. We can see that the program is comparing our input to the decrypted flag, and we can submit it again as input to verify that it is correct.
