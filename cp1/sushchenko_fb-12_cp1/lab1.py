import math
import re

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "


def filter_file():
    with open("text_1.txt", "r", encoding="utf-8") as f:
        text = "".join(re.sub("[^а-яё]", " ", f.read().lower()))
        text = "".join(re.sub(r"\s+", " ", text))

    with open("text_1.txt", "r", encoding="utf-8") as f:
        text2 = "".join(c for c in f.read().lower() if c.isalpha() and c in alphabet)

    return text, text2


def frequency_h(text):
    freqs = {}
    lenght = len(text)

    for c in text:
        if c in freqs:
            freqs[c] += 1
        else:
            freqs.update({c: 1})

    for i in alphabet:
        if i in freqs:
            freqs[i] = freqs[i]/lenght

    freqs = dict(sorted(freqs.items(), key=lambda x: x[1], reverse=True))

    for key, value in freqs.items():
        print(key, value)

    h1 = 0
    for i in freqs:
        h1 += -1 * freqs[i] * math.log2(freqs[i])

    return h1


def bigrams_cross(text):
    bigrams = {}
    freqs = {}
    bigram_count = 0

    for i in range(len(text) - 1):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            bigram_count += 1
            if bigram in bigrams:
                bigrams[bigram] += 1
            else:
                bigrams[bigram] = 1

    bigrams = dict(sorted(bigrams.items(), key=lambda x: x[1], reverse=True))

    for i in bigrams:
        freqs[i] = bigrams[i] / bigram_count

    return bigrams, bigram_count, freqs


def bigrams_no_cross(text):
    bigrams = {}
    freqs = {}
    bigram_count = 0

    for i in range(0, len(text) - 1, 2):
        bigram = text[i] + text[i + 1]
        if len(bigram) == 2:
            bigram_count += 1
            if bigram in bigrams:
                bigrams[bigram] += 1
            else:
                bigrams[bigram] = 1

    bigrams = dict(sorted(bigrams.items(), key=lambda x: x[1], reverse=True))

    for i in bigrams:
        freqs[i] = bigrams[i] / bigram_count

    return bigrams, bigram_count, freqs


def entropy(biagrams, amount):
    entropy = 0

    for i in biagrams:
        biagrams[i] = biagrams[i] / amount
        entropy -= (biagrams[i] * math.log2(biagrams[i])) / 2

    return entropy


def calc_r(entropy, alph_amount):
    return 1-(entropy/math.log2(alph_amount))


if __name__ == '__main__':
    text_spaces, text_no_spaces = filter_file()

    print("Частота символів без пробілів:")
    h1 = frequency_h(text_no_spaces)
    print("\nЧастота символів з пробілами:")
    h_1 = frequency_h(text_spaces)
    h2, count1, freq1 = bigrams_no_cross(text_no_spaces)
    print("Частоти біграм без пробілу без перетину:\n", h2, "\n", freq1)
    h2_cross, count2, freq2 = bigrams_cross(text_no_spaces)
    print("Частоти біграм без пробілу з перетином:\n", h2_cross, "\n", freq2)
    h_2, count3, freq3 = bigrams_no_cross(text_spaces)
    print("Частоти біграм з пробілами без перетину:\n", h_2, "\n", freq3)
    h_2_cross, count4, freq4 = bigrams_cross(text_spaces)
    print("Частоти біграм з пробілами з перетином:\n", h_2_cross, "\n", freq4)

    en1 = entropy(h2, count1)
    en2 = entropy(h2_cross, count2)
    en3 = entropy(h_2, count3)
    en4 = entropy(h_2_cross, count4)

    print("\nЕнтропія H1 без пробілів: ", h1)
    print("Ентропія H1 з пробілами: ", h_1)
    print("Ентропія H2 без пробілів без перетину: ", en1)
    print("Ентропія H2 без пробілів з перетином: ", en2)
    print("Ентропія H2 з пробілами без перетину: ", en3)
    print("Ентропія H2 з пробілами з перетином: ", en4)

    print("\nНадлишковість H1 без пробілів: ", calc_r(h1, 33))
    print("Надлишковість H1 з пробілами: ", calc_r(h_1, 34))
    print("Надлишковість H2 без пробілів без перетину: ", calc_r(en1, 33))
    print("Надлишковість H2 без пробілів з перетином: ", calc_r(en2, 33))
    print("Надлишковість H2 з пробілами без перетину: ", calc_r(en3, 34))
    print("Надлишковість H2 з пробілами з перетином: ", calc_r(en4, 34))
