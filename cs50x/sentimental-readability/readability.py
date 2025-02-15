from cs50 import get_string

plain_text = get_string("Text: ")

letters = 0
words = 0
sentences = 0

for i in plain_text:
    if i.isalpha():
        letters += 1
    if i.isspace():
        words += 1
    if i in ['.', '?', '!']:
        sentences += 1

words += 1

L = (letters * 100.0) / words
S = (sentences * 100.0) / words
index = int((0.0588 * L - 0.296 * S - 15.8) + 0.5)

if index >= 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {index}")