import math
from collections import Counter

file = open('text.txt', 'r', encoding="windows-1251")
# file = open('text_without_spaces.txt', 'r', encoding="windows-1251")
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
# sorted_probabilities_of_symbol = sorted(probabilities_of_symbol.items(), key=lambda item: item[1])
# for symbol, probability in sorted_probabilities_of_symbol:
#     print(f"{symbol}: {probability}")

probabilities_of_bigram1={}
def bigram_1_frequencies(text):
    text = normalized_text
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    number_of_each_bigram = Counter(bigrams)
    total_number_of_bigrams = len(bigrams)
    for bigram, k in number_of_each_bigram.items():
        probabilities_of_bigram1[bigram] = k / total_number_of_bigrams
    return probabilities_of_bigram1
bigram_1_frequencies(text)
# sorted_probabilities_of_bigram = sorted(probabilities_of_bigram.items(), key=lambda item: item[1])
# for bigram, probability in sorted_probabilities_of_bigram:
#     print(f"{bigram}: {probability}")

probabilities_of_bigram2={}
def bigram_2_frequencies(text):
    text = normalized_text
    bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    number_of_each_bigram = Counter(bigrams)
    total_number_of_bigrams = len(bigrams)
    for bigram, k in number_of_each_bigram.items():
        probabilities_of_bigram2[bigram] = k / total_number_of_bigrams
    return probabilities_of_bigram2
bigram_2_frequencies(text)
# sorted_probabilities_of_bigram = sorted(probabilities_of_bigram.items(), key=lambda item: item[1])
# for bigram, probability in sorted_probabilities_of_bigram:
#     print(f"{bigram}: {probability}")


def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities.values())

def R(entropy):
    H0 = math.log2(len(set(text)))
    R = 100 * (1 - (entropy / H0))
    return R

print("Н1 для тексту з пробілами: ", entropy(letter_frequencies(text)), "    ", "R = ", R(entropy(letter_frequencies(text))), "%")
print("Н2 для тексту з пробілам: ", entropy(bigram_1_frequencies(text))/2, "    ", "R = ", R(entropy(bigram_1_frequencies(text))/2), "%")
print("Н2 (пари букв не перетинаються) для тексту з пробілами: ", entropy(bigram_2_frequencies(text))/2, "    ", "R = ", R(entropy(bigram_2_frequencies(text))/2), "%")

# print("Н1 для тексту без пробілів: ", entropy(letter_frequencies(text)), "    ", "R = ", R(entropy(letter_frequencies(text))), "%")
# print("Н2 для тексту без пробілів: ", entropy(bigram_1_frequencies(text))/2, "    ", "R = ", R(entropy(bigram_1_frequencies(text))/2), "%")
# print("Н2 (пари букв не перетинаються) для тексту без пробілів: ", entropy(bigram_2_frequencies(text))/2, "    ", "R = ", R(entropy(bigram_2_frequencies(text))/2), "%")
