'''
Dear Maintainer

When I wrote this code, only I and God
knew what it was.
Now, only God knows!

So if you are done trying to 'optimize'
this routine (and failed),
please increment the following counter
as a warning
to the next guy:

total_hours_wasted_here = 13
'''

import re
from collections import Counter
from operator import itemgetter

BASEFOLDER = "/home/mhranik/kpi-labs/crypto-23-24/cp2/Tarasov_Hranik-lab2/"
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def calculate_ic(text):
    n = len(text)
    frequencies = [text.count(char) for char in set(text)]
    ic = sum(f * (f - 1) for f in frequencies) / (n * (n - 1))
    return ic


def text_filter(input_file : str):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    text = text.lower()
    text = re.sub(r'[^а-яА-Я]+', '', text)
    
    with open(input_file, "w", encoding='utf-8') as file:
        file.write(text)
    return text

ic_theoretical = calculate_ic(text_filter(f"{BASEFOLDER}sample.txt"))

text_filter(f"{BASEFOLDER}golubki.txt")

def vigenere_encode(input_key):
    with open(f'{BASEFOLDER}golubki.txt') as file:
        text = file.read()
    with open(f"{BASEFOLDER}{input_key}.txt") as file:
        key = file.read()

    alphabet = ALPHABET

    key_repeated = (key * (len(text) // len(key) + 1))[:len(text)]

    result = ''

    for i in range(len(text)):
        if text[i] in alphabet:
            to_encode = alphabet.index(text[i])
            encoded_char = alphabet[(to_encode + alphabet.index(key_repeated[i])) % 32]
            result += encoded_char

    return result

for i in range(1, 6):
    with open(f"{BASEFOLDER}encoded-{i}.txt", 'w', encoding="utf-8") as file:
        file.write(vigenere_encode(f"key{i}"))


ic_arr = []
for i in range(1,6):
    with open(f"{BASEFOLDER}encoded-{i}.txt", 'r', encoding='UTF-8') as file:
        text = file.read()
    ic_arr.append(calculate_ic(text))
ic_arr.append(calculate_ic(text_filter(f"{BASEFOLDER}golubki.txt")))

def blocks(period):
    text = text_filter(f"{BASEFOLDER}var7.txt")
    arr = []
    offset = 0
    for i in range(0, period):
        arr.append(text[offset::period])
        offset += 1

    return arr

def calculate_avg_ic(arr):
    resulting = 0
    result_arr = []
    for i in range(0, len(arr)):
        resulting += calculate_ic(arr[i])
        result_arr.append([i, calculate_ic(arr[i])])
    return resulting / len(arr)

def find_period():
    dick = {}
    for i in range(2,40):
        dick[i] = calculate_avg_ic(blocks(i))
    print(dick)
    dick = dict(sorted(dick.items(), key=lambda item: item[1]))
    tmp_arr = []
    for key, value in dick.items():
        tmp_arr.append([key, value])#/ic_theoretical
    print(tmp_arr)
    sorted_arr = sorted(tmp_arr, reverse=True, key=itemgetter(1,0))
    
    return sorted_arr[1][0]

def right_blocks(r):
    return blocks(r)

#I HATE MAINTAINERS OF THIS CODE

def find_freq(arr):
    tmp_arr = []
    for i in arr:
        counter = Counter(i)
        counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))
        for key,value in counter.items():
            tmp_arr.append(key)
            break
    return tmp_arr

def find_key(arr):
    tmp_arr = []
    for i in arr:
        tmp_arr.append((ALPHABET.index(i)-ALPHABET.index('о')) % len(ALPHABET))
    second_tmp_arr = []
    for i in tmp_arr:
        second_tmp_arr.append(ALPHABET[i])
    return ''.join(second_tmp_arr)

def vigener_decode(key):
    text = text_filter(f'{BASEFOLDER}var7.txt')
    decoded = []
    key = key*((len(text)//len(key)) + 1)
    key = key[0:-1]
    for i in range(0, len(text)//2):
        decoded.append(((ALPHABET.index(text[i]))-ALPHABET.index(key[i])) % len(ALPHABET))
    result_decoded = []
    for i in decoded:
        result_decoded.append(ALPHABET[i])
    return ''.join(result_decoded)

def main():
    find_period()
    practical_key = "арудазовархимаг"
    theoretical_key = find_key(find_freq(right_blocks(find_period())))
    result = vigener_decode(practical_key)
    print("[*]" + '-'*60 + "[*]")
    print(f"Array of IC for encoded and cleartext:\n Key-1: {ic_arr[0]}\n Key-2: {ic_arr[1]}\n Key-3: {ic_arr[2]}\n Key-4: {ic_arr[3]}\n Key-5: {ic_arr[4]}\n Cleartext: {ic_arr[5]}")
    print("[*]" + '-'*60 + "[*]")
    print(f"Calculated theoretical key: {theoretical_key}")
    print("[*]" + '-'*60 + "[*]")
    print(f"Manually edited practical key: {practical_key}")
    print("[*]" + '-'*60 + "[*]")
    print(f"Cleartext decoded by using practical key:\n{result}")
    print("[*]" + '-'*60 + "[*]")
    with open(f"{BASEFOLDER}decoded.txt", 'w', encoding='UTF-8') as file:
        file.write(result)
    

if __name__ == "__main__":
    main()

