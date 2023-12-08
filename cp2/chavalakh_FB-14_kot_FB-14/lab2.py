import string

def clean_text(text):
    return ''.join(char for char in text if char not in string.punctuation + ' ' + '\n')

def vigenere_encrypt(text, key):
    encrypted_text = ""
    key_len = len(key)
    
    for i in range(len(text)):
        char = text[i]
        key_char = key[i % key_len]
        shift = ord(key_char) - ord('а')      
        encrypted_char = chr(((ord(char) - ord('а') + shift) % 32) + ord('а'))
        encrypted_text += encrypted_char

    return encrypted_text

def vigenere_decrypt(encrypted_text, key):
    decrypted = []
    key_len = len(key)

    for i, char in enumerate(encrypted_text):
        char_index = russian_alphabet.index(char)
        key_char_index = russian_alphabet.index(key[i % key_len])
        decrypted_idx = (char_index - key_char_index) % len(russian_alphabet)
        decrypted_char = russian_alphabet[decrypted_idx]
        decrypted.append(decrypted_char)

    return "".join(decrypted)

def calculate_index(text):
    text = text.lower()
    text_length = len(text)
    letter_frequencies = {chr(ord('а') + i): 0 for i in range(32)}
    
    for char in text:
        if char in letter_frequencies:
            letter_frequencies[char] += 1

    index = 0.0
    for frequency in letter_frequencies.values():
        index += (frequency * (frequency - 1)) / (text_length * (text_length - 1))

    return index
    
def split_into_blocks(text, r):
    blocks = []
    for i in range(r):
        block = text[i::r]
        blocks.append(block)
    return blocks    

def calculate_index_for_encr(text, x):
    blocks = split_into_blocks(text, x)
    indexes = []
    
    for block in blocks:
        index = 0.0
        block_frequencies = {}
        for char in block:
            if char not in block_frequencies:
                block_frequencies[char] = 1
            else:
                block_frequencies[char] += 1 
        for frequency in block_frequencies.values():
            index += (frequency * (frequency - 1)) / (len(block) * (len(block) - 1))
        indexes.append(index)

    return sum(indexes) / x

def find_key(text, size):
    letter_o = 14
    block = split_into_blocks(text, size)
    key = ''
    for i in block:
        block_freq_letter = most_frequent_letter(i)
        key += russian_alphabet[((russian_alphabet.index(block_freq_letter) - letter_o) % 32)]
    print(key)
        
def most_frequent_letter(text):
    letter_freq_dict = {}

    for letter in text:
        if letter in letter_freq_dict:
            letter_freq_dict[letter] += 1
        else:
            letter_freq_dict[letter] = 1
    most_frequent = max(letter_freq_dict, key=letter_freq_dict.get)
    return most_frequent

russian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

with open('C:/Users/artem/Desktop/КРИПТА/lab2/text.txt', 'r', encoding='utf-8') as file:
    text = file.read().lower()

cleaned_text = clean_text(text)
keys = ["фу", "кот", "база", "баран", "авиасигнал", "абракадабра", "авантюристка", "дальновиденье", "кактусоводство", "легковыполнимый", "битторренттрекер", "максимализировать", "загранкомандировка", "автомобилестроитель", "латиноамериканизация"]
print(f'Index of clean text: {calculate_index(cleaned_text)}\n')
for kkey in keys:
    print(f'Key: {kkey}')
    print(f'Index: {calculate_index(vigenere_encrypt(cleaned_text, kkey))}\n')

with open('C:/Users/artem/Desktop/КРИПТА/lab2/text3.txt', 'r', encoding='utf-8') as file:
    text = file.read()

cleaned_text = clean_text(text)
print(f'Index of encrypted text: {calculate_index(cleaned_text)}\n')

for x in range(1, 33):
    ic = calculate_index_for_encr(cleaned_text, x)
    print(f"Index for r={x}: {ic}")

find_key(cleaned_text, 17)

print(vigenere_decrypt(cleaned_text, "войнамагаэндшпиль"))
input()