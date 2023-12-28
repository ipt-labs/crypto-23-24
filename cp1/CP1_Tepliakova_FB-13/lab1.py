#закоментовані рядки - я не враховувала перетини біграм, але в основному коді врахувала 
import re
import math
from collections import Counter

def edit_textfile(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    text = re.sub(r'[^a-zA-Zа-яА-Я\s\n]', ' ', text)
    text = text.lower()
    text = text.replace("ё", "е")
    text = text.replace("ъ", "ь")
    text = re.sub(r'\s+', ' ', text)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def character_frequency(text):
    frequency = {}
    for character in text:
        if character in frequency:
            frequency[character] += 1
        else:
            frequency[character] = 1
    return frequency

"""def bigram_frequency(text):
    bigram_frequencies = {}
    for i in range(len(text) - 1):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            if bigram in bigram_frequencies:
                bigram_frequencies[bigram] += 1
            else:
                bigram_frequencies[bigram] = 1
    return bigram_frequencies"""

def bigram_frequency(text, step=1):
    bigram_frequencies = {}
    for i in range(0, len(text) - 1, step):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            if bigram in bigram_frequencies:
                bigram_frequencies[bigram] += 1
            else:
                bigram_frequencies[bigram] = 1
    return bigram_frequencies

def calculate_H(frequency):
    entropy = 0
    total = sum(frequency.values())
    for freq in frequency.values():
        probability = freq / total
        entropy += -probability * math.log2(probability)
    return entropy

def calculate_R(entropy, alphabet_size=34):
    R = 1 - (entropy/math.log2(alphabet_size))
    return R


def letters_entropy_without_spaces(text):
    text = text.replace(" ", "")  
    frequency = Counter(text)
    total = len(text)
    
    entropy = 0
    for count in frequency.values():
        probability = count / total
        entropy += -probability * math.log2(probability)
    
    return entropy

def bigram_entropy_without_spaces(text):
    text = text.replace(" ", "") 
    bigram_frequencies = Counter(zip(text, text[1:]))
    total_bigrams = len(text) - 1
    
    entropy = 0
    for count in bigram_frequencies.values():
        probability = count / total_bigrams
        entropy += -probability * math.log2(probability)/2 #підправила
    
    return entropy

input_file_path = "D:\\crypto_github\\crypto-23-24\\cp1\\CP1_Tepliakova_FB-13\\Хоббіт.txt"
output_file_path = "D:\\crypto_github\\crypto-23-24\\cp1\\CP1_Tepliakova_FB-13\\Форматований Хоббіт.txt"

edit_textfile(input_file_path, output_file_path)

with open(output_file_path, 'r', encoding='utf-8') as output_file:
    text = output_file.read()
    text = text.lower()

char_freq = character_frequency(text)
#bigram_freq = bigram_frequency(text)
bigram_freq_intersect = bigram_frequency(text, step=1)  # біграми перетинаються
bigram_freq_non_intersect = bigram_frequency(text, step=2)  # біграми не перетинаються

entropy_char = calculate_H(char_freq)
#entropy_bigram = calculate_H(bigram_freq)
entropy_bigram_intersect = calculate_H(bigram_freq_intersect)/2 #підправила
entropy_bigram_non_intersect = calculate_H(bigram_freq_non_intersect)/2 #підправила

R_char = calculate_R(entropy_char, alphabet_size=len(char_freq))
#R_bigram = calculate_R(entropy_bigram, alphabet_size=len(bigram_freq))
R_bigram_intersect = calculate_R(entropy_bigram_intersect, alphabet_size=len(bigram_freq_intersect))
R_bigram_non_intersect = calculate_R(entropy_bigram_non_intersect, alphabet_size=len(bigram_freq_non_intersect))
entropy_without_spaces_result = letters_entropy_without_spaces(text)
bigram_entropy_without_spaces_result = bigram_entropy_without_spaces(text)

print("Н1 для тексту з пробілами: ", entropy_char, "    ", "R = ", R_char * 100, "%")
#print("Н2 для тексту з пробілами: ", entropy_bigram , "    ", "R = ", R_bigram * 100, "%") 
print("Н2 для тексту з пробілами (біграми перетинаються): ", entropy_bigram_intersect , "    ", "R = ", R_bigram_intersect * 100, "%") 
print("Н2 для тексту з пробілами (біграми не перетинаються): ", entropy_bigram_non_intersect , "    ", "R = ", R_bigram_non_intersect * 100, "%") 
print("H1 без пробілів: ", entropy_without_spaces_result)
print("H2 без пробілів(біграми перетинаються): ", bigram_entropy_without_spaces_result)

def print_frequency_table(frequency, header):
    total = sum(frequency.values())
    print(header)
    print("{:<5} {:<10} {:<10}".format("Символ", "Кількість", "Частота"))
    print("-" * 30)
    for symbol, count in frequency.items():  
        r = count/total 
        print(f"{symbol:<5} {count:<10} {r:.5f}".format(symbol, count))
    print("\n")

#print_frequency_table(char_freq, "Таблиця кількості букв:")
#print_frequency_table(bigram_freq, "Таблиця кількості біграм:")
print_frequency_table(char_freq, "Таблиця кількості букв:")
print_frequency_table(bigram_freq_intersect, "Таблиця кількості біграм (біграми перетинаються):")
print_frequency_table(bigram_freq_non_intersect, "Таблиця кількості біграм (біграми не перетинаються):")









