#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdbool.h>

long long PIN = 1;
int cnt = 0;
long long MOD = 1000000007;

__attribute__((naked))
void gadget1() { __asm__("pop %edi; ret"); }

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
bool pin3(int attempt){
	if(PIN!=604386456&&cnt!=3)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin4(int attempt){
	if(PIN!=263466265&&cnt!=4)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin5(int attempt){
	if(PIN!=817119764&&cnt!=5)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin6(int attempt){
	if(PIN!=386472936&&cnt!=6)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin7(int attempt){
	if(PIN!=401196988&&cnt!=7)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin8(int attempt){
	if(PIN!=12189063&&cnt!=8)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin9(int attempt){
	if(PIN!=756303192&&cnt!=9)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin10(int attempt){
	if(PIN!=715517256&&cnt!=10)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin11(int attempt){
	if(PIN!=33571847&&cnt!=11)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin12(int attempt){
	if(PIN!=498869914&&cnt!=12)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin13(int attempt){
	if(PIN!=479631744&&cnt!=13)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin14(int attempt){
	if(PIN!=830540662&&cnt!=14)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool pin15(int attempt){
	if(PIN!=238917823&&cnt!=15)
		exit(0);
	PIN*=attempt;
	PIN%=MOD;
	cnt++;
}
bool flag(int attempt) {
  if(PIN!=53644440&&cnt!=16)
    exit(0);
  printf("access granted\n");
  char flag[48];
  FILE *file;
  file = fopen("flag.txt", "r");
  if (file == NULL) {
    printf("flag file missing, if this is on the shell server please let an admin know!\n");
    exit(0);
  }
  fgets(flag, sizeof(flag), file);
  printf(flag);
}

void vuln() {
  char buf[16];
  printf("exploit me... if you dare> ");
  return gets(buf);
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  // Set the gid to the effective gid
  // this prevents /bin/sh from dropping the privileges
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  vuln();
}