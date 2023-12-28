import re
import pandas as pd
from collections import defaultdict
from random import choice
import numpy as np
import matplotlib.pyplot as plt
from typing import List

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
#           01234567890123456789012345678901

# from lab1
def process_text(file_name:str):
    with open(file_name, "rt", encoding='utf-8') as file:
        text = file.read().lower().replace("\n", "").replace("ё", "е").replace(" ", "")
        symbols = "? , . … ; “ „ : -  ! ( ) * « » \ / — 1 2 3 4 5 6 7 8 9 0 №"
        for symbol in symbols.split():
            text = text.replace(symbol, "")
    return text

def frequency(text:str, symbols_list:str = alphabet):
    freq_dict = defaultdict(int)
    for i in symbols_list:
        matches = re.findall(rf'{i}', text)
        freq_dict[i] = len(matches)
    return freq_dict

# 2
def encryption(text:str, key:str, output_file:str, alphabet:str = alphabet): 
    encrypted_text = ""
    for i in range(len(text)):
        letter_index = alphabet.index(text[i])
        key_index = alphabet.index(key[i % len(key)])
        c = (letter_index + key_index) % len(alphabet)
        encrypted_text += alphabet[c]

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(encrypted_text)


def decryption(text:str, key:str, output_file:str, alphabet:str = alphabet):
    decrypted_text = ""
    for i in range(len(text)):
        letter_index = alphabet.index(text[i])
        key_index = alphabet.index(key[i % len(key)])
        c = (letter_index - key_index + len(alphabet)) % len(alphabet)
        decrypted_text += alphabet[c]
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(decrypted_text)

def draw_graph(dictionary:dict):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    plt.bar(keys, values, color='b')
    plt.title('')
    plt.xlabel('Довжина ключа')
    plt.ylabel('Індекси сумісності')
    plt.show()

# індекс відповідності
def get_I(text:str, alphabet:str = alphabet):
    letters_frequency = frequency(text, alphabet)
    denominator = len(text) * (len(text) - 1)
    if denominator == 0:
        return 0
    return sum([(letters_frequency[i] * (letters_frequency[i] - 1)) for i in letters_frequency]) / denominator


def get_I_statistics(encrypted_text_files: List[str], alphabet: str = alphabet):
    vals = {}

    for file_name in encrypted_text_files:
        text = process_text(file_name)
        nums = re.findall(r'\d+', file_name)
        num = ""
        for n in nums:
            num += n
        current_I = get_I(text)
        vals[num] = current_I
    print(vals)


def get_keys_I(text:str, alphabet:str = alphabet):
    keys_ci = defaultdict(int)
    for r in range(2, len(alphabet)):
        parts = ['']*r
        for i,symbol in enumerate(text):
            parts[i%r] += symbol
        keys_ci[r] = sum([get_I(part) for part in parts])/len(parts)
    draw_graph(keys_ci)

def get_key(text:str, key_length:int, alphabet:str = alphabet): 
    parts = ['']*key_length
    for i,symbol in enumerate(text):
        parts[i%key_length] += symbol

    key_data = ""
    for i, part in enumerate(parts):
        letters_frequency = frequency(part)
        letter = max(letters_frequency.items(), key=lambda x: x[1])[0]

        decoded_letter = alphabet[(alphabet.index(letter) - 14) % len(alphabet)]
        key_data += decoded_letter
    
    return key_data

def get_MI(frequency:dict, text:str):
    if len(text) == 0:
        return 0
    return sum([(val / len(text))**2 for val in frequency.values()])

plain_text = process_text("text.txt")
text_to_decrypt = process_text("task.txt")

# шифрування - тести з довільними ключами
keys = {"ня":2, "мур":3, "лоля":4, "чайник":6, "оставьнадежду":13}
encrypted_texts = []

for key, value in keys.items():
    encryption(plain_text, f'{key}', f'output_encrypted_test_{value}.txt')
    encrypted_texts.append(f'output_encrypted_test_{value}.txt')

    file = open(f'output_encrypted_test_{value}.txt', "rt", encoding='UTF-8')
    text_to_decrypt = file.read()
    # print(f'{value}:  {get_I(text_to_decrypt)}')
    get_keys_I(text_to_decrypt)
    decryption(text_to_decrypt, f'{key}', f'output_decrypted_test_{value}.txt')

# test_text = process_text("output_encrypted_test_")
# get_keys_I()
# print(encrypted_texts)

# індекс відповідності - тести
# for key, value in keys.items():
#    print(f'оригінальний текст: I = {get_I(plain_text)}')
#   test_ci = process_text('test_outputs\\output_encrypted_test_2.txt')
#   print(get_I(test_ci))

# # математичне очікування
# print(f'MI = {get_MI(frequency(text_to_decrypt), text_to_decrypt)}')

# індекс відповідності - oh shit, here we go again
get_keys_I(text_to_decrypt)

# ключ
print(get_key(text_to_decrypt, 12))

# FINALLLLLLLLYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
decryption(text_to_decrypt, "вшебспирбуря", "output_decrypted_test.txt")

# залежність між довжиною ключа та індексом відповідності шифротексту

vals = {2:0.044370781512317124, 3:0.04186795491143317, 4:0.039116730051050125, 6:0.03451194024737041, 12:get_I(text_to_decrypt), 13:0.034212149244526674}
key_lengths = list(vals.keys())
key_Is = list(vals.values())

plt.plot(key_lengths, key_Is)
plt.title("співставлення довжин ключів та їхіндексів відповідності у зашифрованих текстах")
plt.xlabel("довжини ключів")
plt.ylabel("індекс відповідності шифротексту")
plt.xticks(key_lengths)
plt.show()