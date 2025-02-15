import sys
import csv

if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit(1)

file = open(sys.argv[1], "r") #ppl


dna_types =[]
people = {}
for num, row in enumerate(file):
    #print(num)
    #print(row)
    if num == 0:
        dna_types = [dna for dna in row.strip().split(',')][1:]
        #print(dna_types)
    else:
        cur = row.strip().split(',')
        people[ cur[0] ] = [int(x) for x in cur[1:]]
        #print(people)


dna_file = open(sys.argv[2], 'r').read()

result = []

for dna in dna_types:
    i = 0
    dna_match = 0
    record_dna_match = -1

    while i < len(dna_file):

        box = dna_file[i:i+len(dna)]

        if dna == box:
            dna_match += 1
            record_dna_match = max(record_dna_match, dna_match)
            i += len(dna)
        else:
            dna_match = 0
            i += 1
    result.append(record_dna_match)
    #print(f"result {result}")

for name, dna in people.items():
    #print(dna)
    #print(name)
    if dna == result:
        print(name)
        exit(0)

print("no match")

