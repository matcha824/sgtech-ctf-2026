# Combination Rock - Solution writeup

## Vulnerability

This is, as stated in the description, a ROP challenge. We need to call a lot of different methods that are found in the code, namely, we need to call pin1, pin2, pin3... all the way to pin15, and then flag. Turns out we have a fun package called pwntools that is very useful for this. However there is still quite a bit of work that goes into solving it. Let's take a look at the source code of pinx.

```
long long PIN = 1;
int cnt = 0;
long long MOD = 1000000007;

__attribute__((naked))
void gadget1() { __asm__("pop %edi; ret"); } // gadget so that rop chain works

bool pin0(int attempt){
	if(PIN!=1&&cnt!=0)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin1(int attempt){
	if(PIN!=486500720&&cnt!=1)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin2(int attempt){
	if(PIN!=652630311&&cnt!=2)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
```

So if the PIN value is not exactly a certain integer, then the program exits immediately. Then if we got it right, it multiplies the current PIN with our attempt, all under modulo 1e9+7. 

Let's try to figure out how we would solve this lock if we could directly interface with the program. For pin1, it's pretty easy- $1 \times 486500720 \equiv 486500720 \pmod{1000000007}$. So how do we get to pin2? 

Turns out, division under mod is very possible. Using the [modular multiplicative inverse](https://en.wikipedia.org/wiki/Modular_multiplicative_inverse) we can figure out what number we need to multiply PIN by to get the next number. Assuming `matches` contains all of the pins, 

`coefficient[i] = matches[i] * pow(matches[i-1], 1000000005, 1000000007) % 1000000007`

Alright, so we can harvest the necessary coefficents, now all that remains is to figure out how to directly interface with the program. [ROP chaining](https://ctf101.org/binary-exploitation/return-oriented-programming/) is the tool for this- we need to figure out a buffer overflow that can call all the necessary functions with the right arguments. So the steps are as such-

1. Get the overflow offset. We can execute the executable with a De Brujin sequence, and determine the offset.
2. Then we craft a rop payload, with pwntools. We call all 15 pin functions, and then the flag function.
3. Combining a dummy offset string with the payload, if we send it in to the program, then it will return the flag. 

You can find the code used to generate the solution in `pwnrop.py`, and `elfanalyzer.py`.