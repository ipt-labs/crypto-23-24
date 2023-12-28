import re
import math
from collections import defaultdict
def filter_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.lower()
    text = re.sub(r'[^а-яё\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)
def calculate_char_frequency(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    char_count = defaultdict(int)
    total_chars = len(text)
    for char in text:
        char_count[char] += 1
    char_frequency = {char: count / total_chars for char, count in char_count.items()}
    return char_frequency
def calculate_entropy(char_frequency):
    entropy = -sum(p * math.log2(p) for p in char_frequency.values() if p > 0)
    return entropy
def calculate_bigram_frequency(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    bigram_count = defaultdict(int)
    total_bigrams = len(text) - 1
    for i in range(total_bigrams):
        bigram = text[i:i+2]
        bigram_count[bigram] += 1
    bigram_frequency = {bigram: count / total_bigrams for bigram, count in bigram_count.items()}
    return bigram_frequency
def calculate_bigram_entropy(bigram_frequency):
    entropy = (-sum(p * math.log2(p) for p in bigram_frequency.values() if p > 0))/2
    return entropy
if __name__ == "__main__":
    input_file = "first.txt"
    output_file = "filtered_text.txt"
    filter_text(input_file, output_file)
    char_frequency = calculate_char_frequency(output_file)
    char_entropy = calculate_entropy(char_frequency)
    print("Character Frequency:")
    print(char_frequency)
    print("Character Entropy:", char_entropy)
    bigram_frequency = calculate_bigram_frequency(output_file)
    bigram_entropy = calculate_bigram_entropy(bigram_frequency)
    print("\nBigram Frequency:")
    print(bigram_frequency)
    print("Bigram Entropy:", bigram_entropy)