from pprint import pprint
from math import log

def calculate_entropy(FROM_FILE):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'

    with open(FROM_FILE, 'r', encoding='utf-8') as f:
        text = f.read().lower()

    text_length = len(text)
    length = text_length // 2 
    bigrams = dict()

    for i in alphabet:
        for j in alphabet:
            bigrams[i + j] = 0

    i = 0
    while i < text_length:
        bigram = text[i:i+2]
        if bigram in bigrams:
            bigrams[bigram] += 1
        i += 2 

    pprint(sorted(bigrams.items(), key=lambda item: item[1], reverse=True), sort_dicts=False)


print("no spaces no overlap")
print(f"H2: {calculate_entropy('08.txt')}")

