import numpy as np

def opening(filename):
    with open(filename, 'r', encoding='utf8') as file:
        text = file.read()
    return text


def conformity_index(text):
    text_len = len(text)
    counter = {}
    sum_of_chars = 0

    for char in text:
        if char in counter:
            counter[char] += 1
        else:
             counter[char] = 1

    for count in counter.values():
        sum_of_chars += count*(count-1)
    con_index = sum_of_chars/(text_len*(text_len - 1))

    return con_index


def ci_print(text):
    key_lengths = list(range(1, 31))
    indexes = []
    for key_length in key_lengths:
        rows = [input_text[i::key_length] for i in range(key_length)]
        conformity_indices = np.array([conformity_index(row) for row in rows])
        average_index = np.mean(conformity_indices)
        indexes.append(average_index)
    for i, index in enumerate(indexes):
        print(f"Key length {i + 1}: Conformity index = {index}")


def letter_count(text):
    counter = {}
    max_count = 0
    most_common = ''

    for char in text:
        if char in counter:
            counter[char] += 1
        else:
            counter[char] = 1
        if counter[char] > max_count:
            max_count = counter[char]
            most_common = char
    return most_common


def vigenere_decryption(text, key):
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    decrypted_text = ''
    key_len = len(key)

    for i in range(len(text)):
        char_index = alphabet.index(text[i])
        key_char = key[i % key_len]
        key_char_index = alphabet.index(key_char)
        decrypted_char_index = (char_index - key_char_index) % len(alphabet)
        decrypted_text += alphabet[decrypted_char_index]

    return decrypted_text


alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
input_text = opening(input("Input file: "))
ci_print(input_text)
print('='*100)
k = int(input("Enter length of possible key: "))

while True:
    let = (input("Type in new letter or 1, if you want go to the decryption: "))
    if let in alphabet:
        blocks = ['' for _ in range(k)]
        for i, char in enumerate(input_text):
            blocks[i % k] += char

        most_common_letters = [letter_count(block) for block in blocks]
        key = ''

        for letter in most_common_letters:
            mcl_index = alphabet.index(let)
            letter_index = alphabet.index(letter)
            key_letter_index = (letter_index - mcl_index) % len(alphabet)
            key_letter = alphabet[key_letter_index]
            key += key_letter

        for i, letter in enumerate(most_common_letters):
            print(f"Most common letter in block {i + 1}: {letter}")
        print('=' * 100)
        print("Possible key:", key)
    else:
        break
print('='*100)
key = input("Key: ")
output_file = input("Output file: ")
decrypted_text = vigenere_decryption(input_text, key)
with open(output_file, 'w', encoding='utf8') as file:
    file.write(decrypted_text)

