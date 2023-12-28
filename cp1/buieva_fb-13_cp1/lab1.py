import math
from collections import Counter

file = open('text_without_spaces.txt', 'r', encoding="windows-1251")
text = file.read()
normalized_text = text.lower()

probabilities_of_symbol={}
def letter_frequencies(text):
    text = normalized_text
    number_of_each_letter = Counter(text)
    total_number = len(text)
    for letter, k in number_of_each_letter.items():
        probabilities_of_symbol[letter] = k / total_number
    return probabilities_of_symbol

letter_frequencies(text)
sorted_probabilities_of_symbol = sorted(probabilities_of_symbol.items(), key=lambda item: item[1])
for symbol, probability in sorted_probabilities_of_symbol:
    print(f"{symbol}: {probability}")
probabilities_of_bigram={}
def bigram_1_frequencies(text):
    text = normalized_text
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    number_of_each_bigram = Counter(bigrams)
    total_number_of_bigrams = len(bigrams)
    for bigram, k in number_of_each_bigram.items():
        probabilities_of_bigram[bigram] = k / total_number_of_bigrams
    return probabilities_of_bigram
bigram_1_frequencies(text)
sorted_probabilities_of_bigram = sorted(probabilities_of_bigram.items(), key=lambda item: item[1])
for bigram, probability in sorted_probabilities_of_bigram:
    print(f"{bigram}: {probability}")

def bigram_2_frequencies(text):
    text = normalized_text
    bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    number_of_each_bigram = Counter(bigrams)
    total_number_of_bigrams = len(bigrams)
    for bigram, k in number_of_each_bigram.items():
        probabilities_of_bigram[bigram] = k / total_number_of_bigrams
    return probabilities_of_bigram
bigram_2_frequencies(text)
sorted_probabilities_of_bigram = sorted(probabilities_of_bigram.items(), key=lambda item: item[1])
for bigram, probability in sorted_probabilities_of_bigram:
    print(f"{bigram}: {probability}")


def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities.values())

print("Н1 для тексту з пробілами: ", entropy(letter_frequencies(text)))
print("Н2 для тексту з пробілам: ", entropy(bigram_1_frequencies(text)))
print("Н2 (пари букв не перетинаються) для тексту без пробілів: ", entropy(bigram_2_frequencies(text)))

