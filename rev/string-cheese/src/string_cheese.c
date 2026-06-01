#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define FLAG "sgctf{b1n4Ri3s_doNt_h1d3_d4tA}"
#define MAX_INPUT_LEN 256

int main() {
    char input[MAX_INPUT_LEN];
    
    printf("Enter the flag: ");
    fflush(stdout);
    
    if (fgets(input, MAX_INPUT_LEN, stdin) == NULL) {
        printf("Error reading input.\n");
        return 1;
    }
    
    size_t len = strlen(input);
    if (len > 0 && input[len - 1] == '\n') {
        input[len - 1] = '\0';
    }
    
    if (strcmp(input, FLAG) == 0) {
        printf("Congratulations! You've found the flag!\n");
    } else {
        printf("That doesn't seem quite right...\n");
    }
    
    return 0;
}
