from pprint import pprint
from math import log

def calculate_entropy(FROM_FILE, overlap, no_spaces):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'

    with open(FROM_FILE, 'r', encoding='utf-8') as f:
        text = f.read().lower()

    if no_spaces:
        text = text.replace(" ", "")

    text_length = len(text)
    length = text_length // 2 if not overlap else text_length - 1
    bigrams = dict()

    for i in alphabet:
        for j in alphabet:
            bigrams[i + j] = 0

    i = 0
    while i < text_length:
        bigram = text[i:i+2]
        if bigram in bigrams:
            bigrams[bigram] += 1
        i += 2 if not overlap else 1

    pprint(sorted(bigrams.items(), key=lambda item: item[1], reverse=True), sort_dicts=False)

    h2 = 0
    for i in bigrams.keys():
        if bigrams[i] == 0:
            continue
        h2 -= (bigrams[i] / length) * log(bigrams[i] / length, 2)

    return h2 / 2


print("no spaces no overlap")
print(f"H2: {calculate_entropy('NOspaces_text.txt', overlap=False, no_spaces=True)}")


