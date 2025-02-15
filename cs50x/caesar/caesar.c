#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

bool checking_digit_or_not(string s);
void encrypt(string ciphertext, string plaintext, int k);

int main(int argc, string argv[])
{

    if(argc != 2 || !checking_digit_or_not(argv[1]))
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }

    int k = atoi(argv[1]);
    string plaintext = get_string("plaintext: ");
    int n = strlen(plaintext);
    char ciphertext[n + 1];
    encrypt(ciphertext, plaintext, k);

    printf("ciphertext: %s\n", ciphertext);

    return 0;
}

void encrypt(string ciphertext, string plaintext, int k)
{

    int i = 0;

    for(i = 0; i < strlen(plaintext); i++)
    {
        char ch = plaintext[i];
        char tem = ch;
        int pi = 0;
        char ci;

        if(isalpha(ch))
        {
            if(ch >= 'A' && ch <= 'Z')
            {
                pi = tem - 'A';
                ci = ((pi + k) % 26) + 'A';

            }

            if(ch >= 'a' && ch <= 'z')
            {
                pi = tem - 'a';
                ci = ((pi + k) % 26) + 'a';
            }

            ciphertext[i] = ci;
        }
        else
        {
            ciphertext[i] = ch;
        }
    }

    ciphertext[i] = '\0';
}

bool checking_digit_or_not(string s)
{
    for(int i = 0; i < strlen(s); i++)
    {
        char c = s[i];

        if(!isdigit(c))
        {
            return false;
        }
    }
    return true;
}