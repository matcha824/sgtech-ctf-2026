#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <openssl/aes.h>

// AES block size is 16 bytes (128 bits)
#define AES_BLOCK_SIZE 16

// Challenge data from challenge.json
const char *encrypted_flag_hex = "cc818157d555903066386d07b7db51d842a05de9e8e432facc31822319d7813d";
const char *iv_hex = "abababababababab0101010101010101";

// Known flag prefix for validation
const char *flag_prefix = "sgctf{";

// Convert hex string to bytes
void hex_to_bytes(const char *hex, uint8_t *bytes, size_t len) {
    for (size_t i = 0; i < len; i++) {
        sscanf(hex + 2 * i, "%2hhx", &bytes[i]);
    }
}

// Remove PKCS7 padding
// Returns the actual length of the unpadded data
size_t pkcs7_unpad(uint8_t *data, size_t len) {
    if (len == 0) return 0;
    
    uint8_t pad_len = data[len - 1];
    
    // Validate padding
    if (pad_len == 0 || pad_len > 16) {
        return len;  // Invalid padding, return as-is
    }
    
    // Check that all padding bytes are correct
    for (size_t i = len - pad_len; i < len; i++) {
        if (data[i] != pad_len) {
            return len;  // Invalid padding, return as-is
        }
    }
    
    return len - pad_len;
}


int main() {
    uint8_t iv[16];
    uint8_t ciphertext[32];  // 64 hex chars = 32 bytes
    
    // Parse challenge data
    hex_to_bytes(iv_hex, iv, 16);
    hex_to_bytes(encrypted_flag_hex, ciphertext, 32);
    
    // Known last 100 bits as hex (from challenge.json)
    // This is bytes 3-15 of the key (with byte 3 having the bottom 4 bits)
    const uint8_t known_bytes[13] = {
        0x2b, 0x3c, 0x4d, 0x5e, 0x6f, 0x78, 0x90, 0xab, 0xcd, 0xef, 0x12, 0x34, 0x56
    };
    
    printf("Starting brute force of first 28 bits...\n");
    printf("Total combinations: 2^28 = %lu\n", (1UL << 28));
    printf("This may take a while...\n\n");
    
    // Doubly-nested loop to iterate through all 28-bit combinations
    // We iterate byte by byte for the first 3 bytes, then bit by bit for the last 4 bits
    uint64_t count = 0;
    
    for (int b0 = 0; b0 < 256; b0++) {           // Byte 0: bits 0-7
        for (int b1 = 0; b1 < 256; b1++) {       // Byte 1: bits 8-15
            for (int b2 = 0; b2 < 256; b2++) {   // Byte 2: bits 16-23
                for (int b3_top = 0; b3_top < 16; b3_top++) {  // Top 4 bits of byte 3: bits 24-27
                    
                    count++;
                    if (count % 10000000 == 0) {
                        printf("Progress: %lu / 268435456 (%.2f%%)\n", 
                               count, (double)count / (1UL << 28) * 100);
                    }
                    
                    // Construct the full key
                    uint8_t key[16];
                    key[0] = b0;
                    key[1] = b1;
                    key[2] = b2;
                    key[3] = (b3_top << 4) | (known_bytes[0] & 0x0F);  // Top 4 bits from brute force, bottom 4 bits from known
                    
                    // Copy the remaining known bytes
                    for (int i = 0; i < 12; i++) {
                        key[4 + i] = known_bytes[1 + i];
                    }
                    
                    // Decrypt and check
                    AES_KEY aes_key;
                    AES_set_decrypt_key(key, 128, &aes_key);
                    
                    // First, decrypt only the first block and check prefix
                    uint8_t first_block[16];
                    uint8_t decrypted_block[16];
                    AES_decrypt(ciphertext, decrypted_block, &aes_key);
                    
                    // XOR with IV (CBC mode for first block)
                    for (int i = 0; i < 16; i++) {
                        first_block[i] = decrypted_block[i] ^ iv[i];
                    }
                    
                    // Check if first block starts with flag prefix
                    if (memcmp(first_block, flag_prefix, strlen(flag_prefix)) == 0) {
                        // Key is valid, decrypt all blocks
                        uint8_t plaintext[32];
                        memcpy(plaintext, first_block, 16);  // Copy first block
                        
                        uint8_t prev_block[16];
                        memcpy(prev_block, ciphertext, 16);
                        
                        for (int block = 1; block < 2; block++) {
                            AES_decrypt(ciphertext + block * 16, decrypted_block, &aes_key);
                            
                            // XOR with previous block (CBC mode)
                            for (int i = 0; i < 16; i++) {
                                plaintext[block * 16 + i] = decrypted_block[i] ^ prev_block[i];
                            }
                            
                            memcpy(prev_block, ciphertext + block * 16, 16);
                        }
                        
                        // Remove PKCS7 padding
                        size_t unpadded_len = pkcs7_unpad(plaintext, 32);
                        
                        // Null-terminate for printing
                        plaintext[unpadded_len] = '\0';
                        
                        printf("Found key!\n");
                        printf("Key (hex): ");
                        for (int i = 0; i < 16; i++) {
                            printf("%02x", key[i]);
                        }
                        printf("\n");
                        
                        printf("Decrypted flag: %s\n", plaintext);
                        return 0;
                    }
                }
            }
        }
    }
    
    printf("Key not found!\n");
    return 1;
}
