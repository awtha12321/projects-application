#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int y = 0; y < width; y++)
        {
            RGBTRIPLE color = image[i][y];

            int average = round((color.rgbtRed + color.rgbtGreen + color.rgbtBlue) / 3.0 );

            image[i][y].rgbtBlue = image[i][y].rgbtRed = image[i][y].rgbtGreen = average;
        }
    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for(int  i = 0; i < height; i++)
    {
        for(int y = 0; y < width; y++)
        {
            RGBTRIPLE pixel = image[i][y];

            int sepiaRed = round(.393 * pixel.rgbtRed + .769 * pixel.rgbtGreen + .189 * pixel.rgbtBlue);
            int sepiaGreen = round(.349 * pixel.rgbtRed + .686 * pixel.rgbtGreen + .168 * pixel.rgbtBlue);
            int sepiaBlue = round(.272 * pixel.rgbtRed + .534 * pixel.rgbtGreen + .131 * pixel.rgbtBlue);

            if(sepiaRed > 255)
                sepiaRed = 255;

            if(sepiaGreen > 255)
                sepiaGreen = 255;

            if(sepiaBlue > 255)
                sepiaBlue = 255;

            image[i][y].rgbtRed = sepiaRed; //> 255 ? 255 : sepiaRed;
            image[i][y].rgbtBlue = sepiaBlue; //> 255 ? 255 : sepiaBlue;
            image[i][y].rgbtGreen = sepiaGreen; //> 255 ? 255 : sepiaGreen;

        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tem[height][width];

    for(int i = 0; i < height; i++)
    {
        int star_point = 0;

        for(int j = width - 1; j >= 0 ; j--, star_point++)
        {
            tem[i][star_point] = image[i][j];
        }
    }

    for(int z = 0; z < height; z++)
    {
        for(int y = 0; y < width; y++)
        {
            image[z][y] = tem[z][y];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tem[height][width];

    for(int row = 0; row < height; row++)
    {

        for(int col = 0; col < width; col++)
        {
            int count = 0;
            int x_row[] = {row-1, row, row+1};
            int y_colum[] = {col-1, col, col+1};
            float totalR = 0;
            float totalG = 0;
            float totalB = 0;

            for(int c = 0; c < 3; c++)
            {
                for(int z = 0; z < 3; z++)
                {
                    int rows = x_row[c];//height
                    int colums = y_colum[z];//width

                    if(rows >= 0 && rows < height && colums >= 0 && colums < width)
                    {
                        RGBTRIPLE pixel = image[rows][colums];

                        totalR = totalR + pixel.rgbtRed;
                        totalG = totalG + pixel.rgbtGreen;
                        totalB = totalB + pixel.rgbtBlue;
                        count++;
                    }
                }
            }

            tem[row][col].rgbtRed = round(totalR / count);
            tem[row][col].rgbtGreen = round(totalG / count);
            tem[row][col].rgbtBlue = round(totalB / count);
        }
    }


    for(int w = 0; w < height; w++)
    {
        for(int a = 0; a < width; a++)
        {
            image[w][a] = tem[w][a];
        }
    }
    return;
}
