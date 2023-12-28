import re
from collections import Counter
import math

def filter_text(input_text):
    filtered_text = re.sub(r'[a-zA-Z]', '', input_text)
    filtered_text = filtered_text.lower()
    filtered_text = filtered_text.replace("ъ", "ь")
    filtered_text = filtered_text.replace("ё", "е")
    filtered_text = re.sub(r'[^a-z]', ' ', filtered_text)
    filtered_text = re.sub(r'\s+', ' ', filtered_text)

    return filtered_text

# Текст на входе
with open("cp1_text.txt", "r", encoding="utf8") as input_file:
    input_text = input_file.read()

filtered_text = filter_text(input_text)

# # Отфильтрованный текст
with open("cp1_edited", "w", encoding="utf-8") as output_file:
    output_file.write(filtered_text)

filtered_text_no_spaces = filtered_text.replace(" ", "")

# # Отфильтрованный текст без пробелов
with open("cp1_without_whitespaces", "w", encoding="utf-8") as output_file_no_spaces:
    output_file_no_spaces.write(filtered_text_no_spaces)


def count_letter_frequency(text):
    total_letters = len(text)
    letter_frequency = Counter(text)
    for letter, frequency in letter_frequency.items():
        relative_frequency = frequency / total_letters
        print(f'"{letter}" {relative_frequency:.6f}')


def count_bigram_frequency(text, n):
    if n == 1 :
        ngrams = [text[i:i + n + 1 ] for i in range(len(text) - n + 1)]
    else:
        ngrams = [text[i:i + n] for i in range(0, len(text) - n + 1, 2)]
    ngram_frequency = Counter(ngrams)
    total_ngrams = len(ngrams)
    sorted_ngram_frequency = sorted(ngram_frequency.items(), key=lambda x: x[1], reverse=True)
    for ngram, frequency in sorted_ngram_frequency:
        relative_frequency = frequency / total_ngrams
        print(f'"{ngram}" {relative_frequency:.6f}')


def count_letter_entropy(text):
    total_letters = len(text)
    letter_frequency = Counter(text)
    entropy = 0
    for letter, frequency in letter_frequency.items():
        probability = frequency / total_letters
        entropy -= probability * math.log2(probability)
    print(f"Энтропия частоты букв: {entropy:.6f}")

    return entropy


def count_bigram_entropy(text, n):
    if n == 1 :
        ngrams = [text[i:i + n + 1 ] for i in range(len(text) - n + 1)]
    else:
        ngrams = [text[i:i + n] for i in range(0, len(text) - n + 1, 2)]
    ngram_frequency = Counter(ngrams)
    total_ngrams = len(ngrams)
    entropy = 0
    for ngram, frequency in ngram_frequency.items():
        probability = frequency / total_ngrams
        entropy -= (probability * math.log2(probability) / 2)
    print(f"Энтропия частоты биграмм: {entropy:.6f}")

    return entropy




# Частота букв в тексте с пробелом
# count_letter_frequency(filtered_text)


# Частота биграмм в тексте с пробелом (1 - пересечение; 2 - без)
# count_bigram_frequency(filtered_text, 1)
# count_bigram_frequency(filtered_text, 2)


# Энтропия букв в тексте с пробелом
# entropy = count_letter_entropy(filtered_text)


# Энтропия биграмм в тексте с пробелом (1 - пересечение; 2 - без)
# entropy = count_bigram_entropy(filtered_text, 1)
# entropy = count_bigram_entropy(filtered_text, 2)


# Энтропия букв в тексте без пробелов
# entropy = count_letter_entropy(filtered_text_no_spaces)


# Энтропия биграмм в тексте без пробелов (1 - пересечение; 2 - без)
# entropy = count_bigram_entropy(filtered_text_no_spaces, 1)
# entropy = count_bigram_entropy(filtered_text_no_spaces, 2)


