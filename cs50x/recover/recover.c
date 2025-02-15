#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#define block_size 512

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");

    if (file ==  NULL)
    {
        printf("opening file error");
        return 1;
    }

    typedef uint8_t byte;
    byte buffer[block_size];
    size_t byte_read;
    bool first_jpeg = false;
    FILE *current_file;
    char current_filename[100];
    int file_number = 0;
    bool found = false;

    while(true)
    {
        byte_read = fread(buffer, sizeof(byte), block_size, file);

        if(byte_read == 0)
        {
            break;
        }
        //0xff 0xd8 0xff

        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            found = true;

            if(!first_jpeg)
            {
                first_jpeg = true;
            }
            else
            {
               fclose(current_file);
            }
            sprintf(current_filename, "%03i.jpg", file_number);
            current_file = fopen(current_filename, "w");
            fwrite(buffer, sizeof(byte), byte_read, current_file);
            file_number++;
        }
        else
        {
            if(found)
            {
                fwrite(buffer, sizeof(byte), byte_read, current_file);
            }
        }
    }
}
