import re
import string
from collections import Counter
import math
import matplotlib.pyplot as plt
import os, sys
import codecs
from typing import List, Any
import numpy as np

file = open(r'C:\Users\Igor\Desktop\3 курс 1-й семестр\Крипта\[CP-2] FB-11 Dankova Kovalenko\crypto2.txt', encoding ='utf-8')
text = file.read()

file2 = open(r'C:\Users\Igor\Desktop\3 курс 1-й семестр\Крипта\[CP-2] FB-11 Dankova Kovalenko\encrypted_text_var6.txt', encoding ='utf-8')

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
la = len(alphabet) # 31

#preproccessing
text = re.sub(r'[^а-яА-ЯёЁ]', '', text)
text = text.lower()

def vigenere_encrypt(plain_text, key):
    encrypted_text = ""
    key_repeated = (key * (len(plain_text) // len(key))) + key[:len(plain_text) % len(key)]

    for i in range(len(plain_text)):
        shift = ord(key_repeated[i].lower()) - ord('а')
        encrypted_char = chr((ord(plain_text[i].lower()) - ord('а') + shift) % 32 + ord('а'))
        encrypted_text += encrypted_char

    return encrypted_text

def vigenere_decrypt(plain_text, key):
    decrypted_text = []
    for i in range(len(plain_text)):
        decrypted_text.append((plain_text[i] - key[i % len(key)]) % la)
    return decrypted_text

def index_of_coincidence(text):
    total_chars = len(text)
    char_frequency = {}

    for char in text:
        if char in char_frequency:
            char_frequency[char] += 1
        else:
            char_frequency[char] = 1

    ic = sum(n * (n - 1) for n in char_frequency.values()) / (total_chars * (total_chars - 1))
    return ic

def replace(continious_text):
    clean = ''
    continious_text = continious_text.replace('ё', 'е')
    for i in continious_text:
        if i in alphabet:
            clean += i
    return clean
def to_nums(text):
    nums = [alphabet.index(i) for i in text]
    return nums

def from_nums(nums):
    text = ''.join(alphabet[i] for i in nums)
    return text


# Ключі
keys = ["ты", "они", "гады", "укроп", "неонацисты", "бутербродики", "аявамсейчаспокажу"]
encrypted_texts = []

# Шифруємо текст для кожного ключа
for key in keys:
    encrypted_text = vigenere_encrypt(text, key)
    encrypted_texts.append(encrypted_text)

# Обчислюємо індекс відповідності для відкритого тексту
open_text_ic = index_of_coincidence(text)

# Обчислюємо індекс відповідності для кожного шифртексту
encrypted_texts_ic = [index_of_coincidence(text) for text in encrypted_texts]

print("Original Text:", text)
for i in range(len(keys)):
    print(f"Encrypted Text with Key {keys[i]}: {encrypted_texts[i]}")

print(f"Index of Coincidence for Open Text: {open_text_ic}")
for i in range(len(keys)):
    print(f"Index of Coincidence for Encrypted Text with Key {keys[i]}: {encrypted_texts_ic[i]}")


# Графік
plt.figure(figsize=(8, 5))
text_types = ['Open Text'] + [f'r{len(key)}' for key in keys]
ics = [open_text_ic] + encrypted_texts_ic
plt.bar(text_types, ics, color=['blue'] + ['green']*len(keys))
plt.title('Index of Coincidence Comparison')
plt.xlabel('')
plt.ylabel('Index of Coincidence')
plt.ylim(0, 0.06)
plt.show()

##333
ciphertext= file2.read()
ciphertext = replace(ciphertext)

def coincidences(text, r):
    d = 0
    for i in range(len(text) - r):
        if text[i] == text[i + r]:
            d += 1
    return d
print('#########3\n')
D = []
for i in range(2, 32):
    D.append(coincidences(ciphertext, i))
    print('r =', i, 'D =', D[i - 2])
period = D.index(max(D)) + 2
def getKey(text, r):
    y = []
    x = ord('о')
    for block in [text[i::r] for i in range(r)]:
        y.append(ord(Counter(block).most_common(1)[0][0]))
    key = ''
    for i in range(len(y)):
        key += alphabet[(y[i] - x) % la]
    return key
key = getKey(ciphertext, period)
#key = 'возвращениеджинна'
print('key =', key)

decrypted_text = from_nums(vigenere_decrypt(to_nums(ciphertext), to_nums(key)))
print('Decrypted Text with Key:')
print(decrypted_text)

r_values = list(range(2, 32))
coincidence_values = D

# Построение диаграммы
plt.bar(r_values, coincidence_values, color='blue', alpha=0.7)
plt.title('Index of Coincidence')
plt.xlabel('Value of r')
plt.ylabel('Coincidence Count')
plt.show()