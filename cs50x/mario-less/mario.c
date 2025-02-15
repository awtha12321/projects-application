#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = 0;

    do
    {
        height = get_int("Height: ");
    }
    while(! (height >= 1 && height <= 8));

    printf("\n");

    for (int i = 1; i <= height; i++)
    {
        for (int z = 1; z <= height - i; z++)
        {
            printf(" ");
        }
        for (int y = 1; y <= i; y++)
        {
            printf("#");
        }
        printf("\n");
    }
}