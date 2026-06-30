#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define GUARD_VALUE 0xDEADBEEFDEADC0DEULL

void win() 
{
    FILE *f = fopen("flag.txt", "r");
    if (!f) 
    {
        printf("Flag file not found.\n");
        exit(0);
    }
    
    char flag[128];
    fgets(flag, sizeof(flag), f);
    printf("Flag: %s\n", flag);
    fclose(f);
}

void greet() 
{
    volatile unsigned long guard = GUARD_VALUE;
    char name[64];

    printf("Enter your name: ");
    gets(name);

    printf("Hello, %s!\n", name);

    if (guard != GUARD_VALUE) 
    {
        printf("*** stack smashing detected *** \n");
        exit(1);
    }
}

int main() 
{
    setvbuf(stdout, NULL, _IONBF, 0);
    
    printf("=== Stack Overflow ===\n");
    greet();

    printf("Goodbye!\n");
    return 0;
}
