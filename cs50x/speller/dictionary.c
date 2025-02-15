// Implements a dictionary's functionality

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = (LENGTH + 1) * 'z';

// Hash table
int total = 0;
node *table[N];

node *put_word(char *word);

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int hashcode = hash(word);

    node *cursor = table[hashcode];

    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;

    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }

    return (sum % N);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //file open
    FILE *file = fopen(dictionary, "r");

    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    //read string from the file
    while (fscanf(file, "%s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));

        if (new_node == NULL)
        {
            return false;
        }

        //copy string in to node
        strcpy(new_node->word, word);
        new_node->next = NULL;

        //get the hashcode
        int hashcode = hash(word);

        //inserting
        if (table[hashcode] == NULL)
        {
            table[hashcode] = new_node;
        }
        else
        {
            new_node->next = table[hashcode];
            table[hashcode] = new_node;
        }
        total++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return total;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *head = table[i];
        node *cursor = head;
        node *tmp = head;

        while (cursor != NULL)
        {
            cursor = cursor->next;
            free(tmp);
            tmp = cursor;
        }
    }
    return true;
}
