#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/* Buffer size is unknown but it's somewhere between 200 and 300 bytes (4-byte aligned).
 * Find your buffer size with GDB. */
#ifndef BUF_SIZE
#define BUF_SIZE ???
#endif

int bof(char *str)
{
    char buffer[BUF_SIZE];
    /* The following statement has a buffer overflow problem */
    strcpy(buffer, str);
    return 1;
}

int main(int argc, char **argv)
{
    char str[517];
    FILE *badfile;

    badfile = fopen("badfile", "r");
    if (!badfile) {
        perror("fopen");
        return 1;
    }
    fread(str, sizeof(char), 517, badfile);
    fclose(badfile);
    bof(str);
    printf("Returned Properly\n");
    return 1;
}
