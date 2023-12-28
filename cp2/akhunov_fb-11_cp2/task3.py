from random import choice
import csv


# Алфавіт
ALPHABET: str = 'абвгдежзийклмнопрстуфхцчшщыъьэюя'


# Ця функція зчитує текстовий файл та поверає string з текстом цього файлу
def file_read(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        text: str = file.read()
    return text


# Ця функція створює ключ певної довжини
def key_generate(key_len: int) -> str:
    key = ''.join(choice(ALPHABET) for i in range(key_len))
    return key


# Ця функція розшифровує текст
# def decryption(text: str, key: str) -> str:
#     global ALPHABET
#     key_index: int = 0
#     decrypted_text: str = ''
#     for char in text:
#         decrypted_char_index = (ALPHABET.index(char) - ALPHABET.index(key[key_index])) % len(ALPHABET)
#         decrypted_char = ALPHABET[decrypted_char_index]
#         decrypted_text += decrypted_char
#         key_index = (key_index + 1) % len(key)
#     return decrypted_text


# Ця функція розбиває текст на блоки
def create_blocks(encrypted_text: str, key_len: int) -> list:
    blocks: list = []
    for i in range(key_len):
        block = encrypted_text[i::key_len]
        blocks.append(block)
    return blocks


# Ця функція рахує індекси відповідності
def affinity_index(encrypted_text: str) -> float:
    frequency: dict = {}
    affinity: float = 0.0
    for char in encrypted_text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    for char in frequency:
        affinity += (frequency[char] * (frequency[char] - 1)) / (len(encrypted_text) * (len(encrypted_text) - 1))
    return affinity


# Ця функція створює csv файл з результатами
def create_csv_file(filename: str, affinity_dict: dict):
    with open(filename, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Довжина ключа", "Індекс"])
        for affinity in affinity_dict:
            key_len = len(affinity)
            affinity = affinity_dict[affinity]
            affinity = str(affinity).replace('.', ',')
            writer.writerow([key_len, affinity])


def main():
    text: str = file_read('cp2_var15.txt')
    affinity_dict: dict = {}
    for i in range(2, 51):
        key = key_generate(i)
        text_blocks = create_blocks(text, len(key))
        affinity: int = 0
        for block in text_blocks:
            affinity += affinity_index(str(block))
        affinity_dict[key] = affinity / len(key)
    create_csv_file('Affinities_task3.csv', affinity_dict)


if __name__ == "__main__":
    main()
