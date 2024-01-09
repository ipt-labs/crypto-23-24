from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

with open('lab2.txt', 'r', encoding='utf-8') as file:
    text = file.read().lower()

def filter_text(text):
    punctuation = '!"#$%&\'()*+,-./:;<=>?»–«@[\\]^_`{|}~ \n'
    return ''.join(char for char in text if char not in punctuation)

def encrypt(text, key):
    encrypted_text = ""
    key_len = len(key)
    mod = len(alphabet)

    for i in range(len(text)):
        char = text[i]
        if char in alphabet:
            key_index = i % key_len
            key_char = key[key_index]
            shift = alphabet.index(key_char)
            new_char_code = (alphabet.index(char) + shift) % mod
            encrypted_char = alphabet[new_char_code]
            encrypted_text += encrypted_char
        else:
            encrypted_text += char

    return encrypted_text

def calculate_index(text):
    text_length = len(text)
    letter_freq = Counter(text)
    index = 0.0

    for frequency in letter_freq.values():
        if frequency > 1:
            index += (frequency * (frequency - 1)) / (text_length * (text_length - 1))

    return index

keys = ["аб", "где", "ежзи", "йклмн", "опрстуфхцчшщьыьэюя"]

filtered_text = filter_text(text)

print(f'Index of clean text: {calculate_index(filtered_text)}\n')

for key in keys:
    print(f'Key: {key}')
    encrypted_text = encrypt(filtered_text, key)
    with open(f'encrypted_{len(key)}.txt', 'w', encoding='utf-8') as file:
        file.write(encrypted_text)
    print(f'Encrypted text written to encrypted_{len(key)}.txt')
    print(f'Index: {calculate_index(encrypted_text)}\n')



