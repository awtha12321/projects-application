#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <ctype.h>


int main(void)
{
    string plaintext = get_string("Text: ");

    string s = plaintext;

    int letters = 0;
    int words = 0;
    int sentences = 0;

    for (int i = 0; i < strlen(s); i++)
    {
        char ch = s[i];

        if (isalpha(ch))
        {
            letters++;
        }

        if (isspace(ch))
        {
            words++;
        }

        if (ch == '.' || ch == '?' || ch == '!')
        {
            sentences++;
        }
    }
    words++;

    float L = (letters * 100.0f) / words;
    float S = (sentences * 100.0f) / words;
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
       printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

    return 0;
}
