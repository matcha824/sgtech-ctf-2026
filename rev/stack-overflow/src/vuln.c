#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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
    printf("🎉 Flag: %s\n", flag);
    fclose(f);
}

void greet()
{
    char name[64];

    printf("Enter your name: ");
    gets(name);

    printf("Hello, %s!\n", name);
}

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Welcome to my app!\n");
    greet();

    printf("Goodbye!\n");
    return 0;
}