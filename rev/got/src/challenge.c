#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

long numbers[16];
long auth_token;
int authenticated = 0;

void setup() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    srand(time(NULL));
    auth_token = ((long)rand() << 32) | rand();
}

void menu() {
    puts("=== GOT ===");
    puts("1. Read number");
    puts("2. Authenticate");
    if (authenticated) {
        puts("3. Write number");
    }
    puts("0. Quit");
    printf("> ");
}

void do_read() {
    char inp[16];
    int idx;

    printf("Which index would you like to read?\n> ");
    fgets(inp, 16, stdin);
    idx = atoi(inp);    
    printf("numbers[%d] = %lu\n", idx, (unsigned long)numbers[idx]);
}

void do_auth() {
    char inp[32];
    long token;

    printf("Enter the authentication token: \n> ");
    fgets(inp, 32, stdin);
    token = strtol(inp, NULL, 10);

    if (token == auth_token) {
        authenticated = 1;
        puts("[+] Authenticated! Write access granted.");
    } else {
        puts("[-] Authentication failed. Invalid token.");
    }
}

void do_write() {
    char inp[32];
    int idx;
    long val;

    printf("Which index would you like to write to?\n> ");
    fgets(inp, 32, stdin);
    idx = atoi(inp);
    
    printf("What value should be written?\n> ");
    fgets(inp, 32, stdin);
    val = strtol(inp, NULL, 10);
    numbers[idx] = val;
    puts("[+] Done.");
}

int main() {
    setup();
    
    char inp[16];
    int choice;

    while (1) {
        menu();
        fgets(inp, 16, stdin);
        choice = atoi(inp);
        
        switch (choice) {
            case 0:
                puts("Goodbye!");
                exit(0);
            case 1:
                do_read();
                break;
            case 2:
                do_auth();
                break;
            case 3:
                if (authenticated) {
                    do_write();
                } else {
                    puts("[-] Access denied. Authenticate first.");
                }
                break;
            default:
                puts("[-] Invalid choice.");
                break;
        }
    }
    return 0;
}