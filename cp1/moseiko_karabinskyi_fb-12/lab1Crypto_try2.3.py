import re
import math
from math import log2
def filtrate(ini_text,  write_file):
    with open(ini_text, 'r', encoding='utf-8') as file:
          text = file.read()
    text = text.lower()
    text_i = re.sub('[^а-я]+', '', text)
    with open (write_file, 'w', encoding='utf-8') as file_2:
         file_2.write(text_i)
    file.close()
    file_2.close()

def filtrate_with_spaces(ini_text,  write_file):
    with open(ini_text, 'r', encoding='utf-8') as file:
          text = file.read()
    text = text.lower()
    text_i = re.sub('[^а-я]+', ' ', text)
    with open (write_file, 'w', encoding='utf-8') as file_2:
         file_2.write(text_i)
    file.close()
    file_2.close()

    
def open_ans_write(txt_file):
    with open(txt_file) as file:
        txt = file.read()
    return txt


def calculate_letter_frequencies(filtered_file):
    with open(filtered_file, 'r', encoding='utf-8') as file:
          text = file.read()
    letter_frequencies = {}
    for char in text:
        #if char.isalpha():
            if char in letter_frequencies:
                letter_frequencies[char] += 1
            else:
                letter_frequencies[char] = 1
    file.close()
    return letter_frequencies


def calculate_bigram_frequencies(filtered_file):
    with open(filtered_file, 'r', encoding='utf-8') as file:
        text = file.read()
    bigram_frequencies = {}
    for i in range(len(text) - 1):
        bigram = text[i:i + 2]
        #if bigram.isalpha():
        if bigram in bigram_frequencies:
            bigram_frequencies[bigram] += 1
        else:
            bigram_frequencies[bigram] = 1
    return bigram_frequencies

def calculate_bigram_frequencies_without_same(filtered_file):
    with open(filtered_file, 'r', encoding='utf-8') as file:
        text = file.read()
    bigram_set = set()
    bigram_frequencies = {}
    i = 0
    while i < len(text) - 1:
        char1 = text[i]
        char2 = text[i + 1]
        bigram = char1 + char2
        if bigram not in bigram_set:
            bigram_set.add(bigram)
            bigram_frequencies[bigram] = 1
        else:
            bigram_frequencies[bigram] += 1
            i += 2
    return bigram_frequencies


def total_letter_freq(letter_frequencies, file):
    with open(file, 'r', encoding='utf-8') as data:
        a = data.read()
    char_number = len(a)
    let_dict = {}
    for letter, frequency in letter_frequencies.items():
        let_dict[letter] = frequency / char_number
    return let_dict

def total_bigram_freq(bigram_frequencies):
    count = 0
    bigram_dict = {}
    for bigram, frequency in bigram_frequencies.items():
        count += frequency
    for bigram, frequency in bigram_frequencies.items():
       bigram_dict[bigram] = frequency / count
    return bigram_dict


def calculate_entropy(letter_frequencies):
    ent = 0.0
    for val in letter_frequencies.values():
     ent -= val*log2(val)
    return ent


def calculate_nadluskovist(tbf, num, num2):
    r = 1 - (num2*calculate_entropy(tbf)) / log2(num)
    return r

def calculate_nadluskovist_exp(entropy, num, num2):
    r = 1 - (num2*entropy) / log2(num)
    return r

ini_text = 'avidreaders.ru__prestuplenie-i-nakazanie-dr-izd.txt'
write_file = 'lab1CP_filtered.txt'
write_file_spaces = 'lab1CP_filtered_spaces.txt'
filtrate(ini_text, write_file)
filtrate_with_spaces(ini_text, write_file_spaces)
letter_frequencies = calculate_letter_frequencies(write_file)
letter_frequencies_space = calculate_letter_frequencies(write_file_spaces)
bigram_frequencies = calculate_bigram_frequencies(write_file)
bigram_frequencis_spaces = calculate_bigram_frequencies(write_file_spaces)
tlf = total_letter_freq(letter_frequencies, write_file)
tlf_spaces = total_letter_freq(letter_frequencies, write_file_spaces)
file_to_count = open(write_file_spaces, 'r', encoding='utf-8')
data_to_count = file_to_count.read()
tlf_spaces[' '] = letter_frequencies_space[' ']/ len(data_to_count)
tbf = total_bigram_freq(bigram_frequencies)
tbf_spaces = total_bigram_freq(bigram_frequencis_spaces)
bigram_differ_freq = calculate_bigram_frequencies_without_same(write_file)
bigram_differ_freq_spaces = calculate_bigram_frequencies_without_same(write_file_spaces)
tbf_not_same = total_bigram_freq(bigram_differ_freq)
tbf_not_same_spaces = total_bigram_freq(bigram_differ_freq_spaces)
print("Кількість букв:")
for letter, frequency in letter_frequencies.items():
    print(f"{letter}: {frequency}")
print("Кількість букв з пробілами:")
for letter, frequency in letter_frequencies_space.items():
    print(f"{letter}: {frequency}")
print("Частоти букв без пробілів:")
print(dict(sorted(tlf.items())))
print("Частоти букв з пробілами:")
print(dict(sorted(tlf_spaces.items())))
print("\nКількість біграм з повторами , без пробілів:")
print(dict(sorted(bigram_frequencies.items(), key=lambda x:x[1], reverse=True)))
#for bigram, frequency in bigram_frequencies.items():
    #print(f"{bigram}: {frequency}")
print("\nЧастоти біграм з повторами , без пробілів:")
print(dict(sorted(tbf.items(), key=lambda x:x[1], reverse=True)))
print("\nКількість біграм з повторами , з пробілами:")
print(dict(sorted(bigram_frequencis_spaces.items(), key=lambda x:x[1], reverse=True)))
print("\nЧастоти біграм з повторами, з пробілами:")
print(dict(sorted(tbf_spaces.items(), key=lambda x:x[1], reverse=True)))
#for bigram, frequency in bigram_frequencis_spaces.items():
    #print(f"{bigram}: {frequency}")
print("\nКількість біграм без повторів , без пробілів:")
print(dict(sorted(bigram_differ_freq.items(), key=lambda x:x[1], reverse=True)))
print("\nЧастоти біграм без повторів, без пробілів:")
print(dict(sorted(tbf_not_same.items(), key=lambda x:x[1], reverse=True)))
print("\nКількість біграм без повторів , з пробілами:")
print(dict(sorted(bigram_differ_freq_spaces.items(), key=lambda x:x[1], reverse=True)))
print("\nЧастоти біграм без повторів, з пробілами:")
print(dict(sorted(tbf_not_same_spaces.items(), key=lambda x:x[1], reverse=True)))
print("ентропія H1 для тексту без пробілів з повторами ", calculate_entropy(tlf))
print("ентропія H2 для тексту без пробілів з повторами ", 0.5*calculate_entropy(tbf))
print("ентропія H1 для тексту з пробілами з повторами ", calculate_entropy(tlf_spaces))
print("ентропія H2 для тексту з пробілами з повторами ", 0.5*calculate_entropy(tbf_spaces))
print("ентропія H2 для тексту без пробілів без повторів ", 0.5*calculate_entropy(tbf_not_same))
print("ентропія H2 для тексту з пробілами без повторів", 0.5*calculate_entropy(tbf_not_same_spaces))
print("надлишковість для H1 без пробілів", calculate_nadluskovist(tlf, 33, 1))
print("надлишковість для H1  з пробілами", calculate_nadluskovist(tlf_spaces, 34, 1))
print("надлишковість для H2 без пробілів з повторами", calculate_nadluskovist(tbf, 33, 0.5))
print("надлишковість для H2 з пробілами з повторами", calculate_nadluskovist(tbf_spaces, 34, 0.5))
print("надлишковість для H2 без пробілів без повторів", calculate_nadluskovist(tbf_not_same, 33, 0.5))
print("надлишковість для H2 з пробілами без повторів", calculate_nadluskovist(tbf_not_same_spaces, 34, 0.5))
h10_min = 2.63135469716452
h10_max = 3.1964130274445
h20_min = 1.77853580300508
h20_max = 2.41972183240961
h30_min = 1.85070573575709
h30_max = 2.55380065575603
print(calculate_nadluskovist_exp(h10_min, 34, 1), "< R10 <", calculate_nadluskovist_exp(h10_max, 34, 1))
print(calculate_nadluskovist_exp(h20_min, 34, 1), "< R20 <", calculate_nadluskovist_exp(h20_max, 34, 1))
print(calculate_nadluskovist_exp(h30_min, 34, 1), "< R30 <", calculate_nadluskovist_exp(h30_max, 34, 1))
