import collections
import math
import re
def edited_text(text):
    text = text.replace("ъ", "ь")
    text = text.replace("ё", "е")
    text = re.sub(r'[^а-яА-Я]', ' ', text)
    text = re.sub(r'[a-zA-Z]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text

def letter_freq(text):
    letter_freq = collections.Counter(text)
    total_letters = len(text)
    letter_prob = {letter: freq / total_letters for letter, freq in letter_freq.items()}
    sorted_letter_prob = dict(sorted(letter_prob.items(), key=lambda item: item[1], reverse=True))
    return sorted_letter_prob

def bigram_freq_intersec(text):
    bigram_freq = collections.defaultdict(int)
    text_length = len(text)

    for i in range(0, text_length - 1):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            bigram_freq[bigram] += 1

    tot_bigrams = sum(bigram_freq.values())
    bigram_prob = {bigram: freq / tot_bigrams for bigram, freq in bigram_freq.items()}
    sorted_bigram_prob = dict(sorted(bigram_prob.items(), key=lambda item: item[1], reverse=True))
    return sorted_bigram_prob

def bigram_freq_nintersec(text):
    bigram_freq = collections.defaultdict(int)
    text_length = len(text)

    for i in range(0, text_length, 2):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            bigram_freq[bigram] += 1

    tot_bigrams = sum(bigram_freq.values())
    bigram_prob = {bigram: freq / tot_bigrams for bigram, freq in bigram_freq.items()}
    sorted_bigram_prob = dict(sorted(bigram_prob.items(), key=lambda item: item[1], reverse=True))
    return sorted_bigram_prob

def entr(text):
    letter_prob = letter_freq(text)
    bigram_prob_intersec = bigram_freq_intersec(text)
    bigram_prob_nintersec = bigram_freq_nintersec(text)

    entr_letter = -sum(prob * math.log2(prob) for prob in letter_prob.values() if prob > 0)
    entr_bigram_intersec = -0.5*sum(prob * math.log2(prob) for prob in bigram_prob_intersec.values() if prob > 0)
    entr_bigram_nintersec = -0.5*sum(prob * math.log2(prob) for prob in bigram_prob_nintersec.values() if prob > 0)

    return entr_letter, entr_bigram_intersec, entr_bigram_nintersec

with open('D:\Навчання\Криптологія\kafka-na-plyazhe.txt', 'r', encoding='utf-8') as file:
    text = file.read()

new_text = edited_text(text)
with open('D:\Навчання\Криптологія\kafka-na-plyazhe_filtered.txt', 'w', encoding='utf-8') as file:
    file.write(new_text)

text_bez_probelov = new_text.replace(" ", "")
with open('D:\Навчання\Криптологія\kafka-na-plyazhe_bez.txt', 'w', encoding='utf-8') as file:
    file.write(text_bez_probelov)

sorted_letter_frequencies = letter_freq(new_text)
print("Відсортована таблиця частот символів:")
for letter, probability in sorted_letter_frequencies.items():
    print(f"{letter}: {probability:.4f}")

sorted_bigram_frequencies_intersection = bigram_freq_intersec(new_text)
print("\nВідсортована таблиця частот біграм, що перетинаються:")
for bigram, probability in sorted_bigram_frequencies_intersection.items():
    print(f"{bigram}: {probability:.4f}")

sorted_bigram_frequencies_non_intersection = bigram_freq_nintersec(new_text)
print("\nВідсортована таблиця частот біграм, що не перетинаються:")
for bigram, probability in sorted_bigram_frequencies_non_intersection.items():
    print(f"{bigram}: {probability:.4f}")

entropies = entr(new_text)
print("Ентропія Н1:", entropies[0])
print("Ентропія Н2, що перетинаються:", entropies[1])
print("Ентропія Н2, що не перетинаються:", entropies[2])

entropies = entr(text_bez_probelov)
print("Ентропія Н1 для тексту без пробілів:", entropies[0])
print("Ентропія Н2, що перетинаються для тексту без пробілів:", entropies[1])
print("Ентропія Н2, що не перетинаються для тексту без пробілів:", entropies[2])
