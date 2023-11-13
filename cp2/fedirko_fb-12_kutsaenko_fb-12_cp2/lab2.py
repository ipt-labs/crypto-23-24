﻿from collections import Counter
import re
import random

alp = ['а','б','в','г','д','е','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']

def read_file(filename):
    with open(filename, 'r', encoding = 'utf-8') as file_read:
        return file_read.read()

def write_file(filename, data):
    with open(filename, 'w', encoding = 'utf-8') as file:
        file.write(data)

def clear_text(text):
    cleared_text = text.replace('\n', ' ').replace('\r', ' ').replace('ё', 'е').lower()
    cleared_text = re.sub('[^а-я]', '', cleared_text)
    return cleared_text

def get_freq(text):
    return dict(Counter(text).most_common())

def char_int(a):
    return ord(a) - 1072

def int_char(a):
    return chr(a + 1072)

def encryption(text, key):
    encrypted = ''
    for i, char in enumerate(text):
        x = char_int(char)
        y = (x + char_int(key[i % len(key)])) % 32
        encrypted = encrypted + int_char(y)
    return encrypted
    
def decryption(text, key):
    decrypted = ''
    for i, char in enumerate(text):
        x = char_int(char)
        y = (x - char_int(key[i % len(key)])) % 32
        decrypted = decrypted + int_char(y)
    return decrypted

def generate_key(length):
    key = ''.join(random.choice(alp) for _ in range(length))
    print("key:", key)
    return key
    

def get_blocks(text, length):
    blocks = []
    for i in range(length):
        blocks.append(text[i::length] )
    return blocks

def compliance_index(subtext):
    alp_counts = {}
    n = len(subtext)

    for let in subtext:
        if let in alp_counts:
            alp_counts[let] += 1
        else:
            alp_counts[let] = 1
    ind = 0
    for count in alp_counts.values():
        ind += count * (count - 1)
    ind *= 1 / (n * (n - 1))
    return ind


def calculate_index_for_blocks(text): 

    for i in range(1, len(alp)):
        total_index = 0
        for block in get_blocks(text, i): 
            total_index += compliance_index(block)
        average_index = total_index / len(get_blocks(text, i)) 
        print('Довжина ключа =', i, 'індекс відповідності =', average_index)

def find_a_key(text, length, let):
    blocks = get_blocks(text, length)
    key = ""
    for block in blocks:
        frequency_counts = {char: 0 for char in alp}
        for char in block:
            if char in alp:
                frequency_counts[char] += 1

        most_frequent_char = max(frequency_counts, key=frequency_counts.get)
        n = (alp.index(most_frequent_char) - alp.index(let)) % len(alp)
        key += alp[n]
    return key

def key_2_5(text):                                   
    print("Початковий індекс відповідності= ", compliance_index(text))

    for i in range(2,6):
        print("\nДовжина ключа = ",i)
        key=generate_key(i)
        enc=encryption(text,key)
        print("Закодований текс: ",enc)
        print("Звичайний: ",decryption(enc,key))
        print("Індекс відповідності: ",compliance_index(enc))
def key_10_20(text):                                    
    print("Початковий індекс відповідності= ", compliance_index(text))

    for i in range(10,21):
        print("\nДовжина ключа = ",i)
        key=generate_key(i)
        enc=encryption(text,key)
        print("Закодований текс: ",enc)
        print("Звичайний: ",decryption(enc,key))
        print("Індекс відповідності: ",compliance_index(enc))


#task1,2
input_file_path = 'H:/криптографія лаби/cleared_for2.txt'
text = read_file(input_file_path)
print("\nДля ключів довжиною 2-5\n")
key_2_5(text)
print("\nДля ключів довжиною 10-20\n")
key_10_20(text)

#task3
input_file_path = 'H:/криптографія лаби/cleared_encrypted.txt'
text = read_file(input_file_path)
print(text)
calculate_index_for_blocks(text)

key = find_a_key(text, 14, 'о')
print(key)
key = "экомаятникфуко"
print(key)
dec = decryption(text, key)
print(dec)
