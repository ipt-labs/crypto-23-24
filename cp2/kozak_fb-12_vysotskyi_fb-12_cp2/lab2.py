"""
9 варіант

https://en.wikipedia.org/wiki/Index_of_coincidence
"""

from re import sub
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from typing import Iterable

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
ALPHABET_LEN = len(ALPHABET)

path = "idiot.txt"

KEYS = ("ха", "хм", "да", "по", "ле",
        "чур", "хэй", "три", "мда", "бот",
        "влад", "макс", "клад", "пиво", "чего",
        "зорко", "абвгд", "бвгде", "смысл", "жалко", "ботик", "бравл", "летал",
        "крипта", "ненадо", "почему",
        "джекпот", "человек",
        "стэнфорд", "младенец",
        "викакозак",
        "скажипаляниця", "оченьдолгийключшифрования")

def read_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        file_content = f.read()
    return file_content

def clean_text(filepath):
    text = read_text(filepath)
    text = text.lower()
    text = sub("[^а-яё ]", " ", text)
    text = sub("\s+", "", text)
    return text

def save_text(filepath, text):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

#save_text("clean_text.txt", clean_text(path))

def count_letters_from_text(text: str):
    letter_dict = {}
    for letter in text:
        if letter in letter_dict:
            letter_dict[letter] += 1
        else:
            letter_dict[letter] = 1
    letter_dict = dict(sorted(letter_dict.items(), key=lambda x: x[1], reverse=True))
    return letter_dict


def count_frequency_in_iterable(itetable: Iterable) -> dict:
    dictionary = {}
    for obj in itetable:
        if obj in dictionary:
            dictionary[obj] += 1
        else:
            dictionary[obj] = 1
    return dictionary


def find_max(dictionary: dict):
    max_index = None
    for i in dictionary:
        if max_index is None or dictionary[i] > dictionary[max_index]:
            max_index = i
    return max_index


def sort_frequency(frequency: dict) -> list:
    letters_by_frequency = list(frequency.keys())
    letters_by_frequency.sort(key=lambda i: frequency[i], reverse=True)
    print(letters_by_frequency)
    print(frequency)
    return letters_by_frequency


def count_letters_from_file(filepath):    # Підрахунок символів у тексті
    return count_letters_from_text(read_text(filepath))

def vigenere_encrypt(text: str, key: str) -> str:
    cipher_text = ''
    key_index = 0

    for char in text:

        char = "е" if char == "ё" else char
        char_index = ALPHABET.index(char.lower())
        key_char = key[key_index % len(key)]
        key_index += 1

        cipher_char = ALPHABET[(char_index + ALPHABET.index(key_char.lower())) % len(ALPHABET)]
        cipher_text += cipher_char if char.islower() else cipher_char.upper()

    return cipher_text


def vigenere_decrypt(text: str, key: str) -> str:
    open_text = ''
    key_index = 0

    for char in text:

        if char not in ALPHABET:
            continue
        char_index = ALPHABET.index(char.lower())
        key_char = key[key_index % len(key)]
        key_index += 1

        cipher_char = ALPHABET[(char_index - ALPHABET.index(key_char.lower())) % len(ALPHABET)]
        open_text += cipher_char if char.islower() else cipher_char.upper()

    return open_text

def generate_key(length):
    key = ''.join(random.choice(ALPHABET) for _ in range(length))
    return key


def index_of_coincidence(text: str) -> float:
    index_value = 0
    for symbol in ALPHABET:
        letter_occurences = text.count(symbol)
        index_value += letter_occurences * (letter_occurences - 1)
    return index_value / len(text) / (len(text) - 1)


def plot_coincidence_index(key_lengths, coincidence_values, main_coincedence):
    plt.figure(figsize=(10, 6))
    for i, key_length in enumerate(key_lengths):
        plt.plot(key_length, coincidence_values[i], marker='o')

    plt.plot((2, 6), (main_coincedence, main_coincedence))

    plt.title('Index of Coincidence / Key Length')
    plt.xlabel('Key Length')
    plt.ylabel('Index of Coincidence')
    plt.xticks(list(range(1, 6)))
    plt.grid(True)
    plt.show()


def find_key_length(encrypted_text: str):
    """За першим алгоритмом"""
    for key_length in range(6, 31):
        text_blocks = []
        for i in range(key_length):
            text_blocks.append(encrypted_text[i::key_length])

        coincedence_index = 0.0
        for text_block in text_blocks:
            coincedence_index += index_of_coincidence(text_block)
        coincedence_index /= key_length  # Середнє арифметичне
        print(f"r={key_length}: IoC={coincedence_index}")


def letter_diff(from_letter, to_letter):
    return (ALPHABET.index(to_letter) - ALPHABET.index(from_letter)) % ALPHABET_LEN


def caesar_analyse_text_block(text_block: str) -> str:
    """Повертає можливий ключ тексту, зашифрованого шифром Цезаря"""
    most_frequent = ("о", "е", "а", "и", "н", "т")

    frequencies = count_letters_from_text(text_block)
    frequencies = sort_frequency(frequencies)

    l = []
    print("", *most_frequent, sep="\t")
    for i in frequencies[:6]:
        print(i, end="\t")
        for j in most_frequent:
            print(letter_diff(j, i), end="\t")
            l.append(letter_diff(j, i))
        print()

    assumed_key: int = sort_frequency(count_frequency_in_iterable(l))[0]
    return ALPHABET[assumed_key]


def caesar_analyse_text(encrypted_text: str, key_length: int):
    text_blocks = []
    assumed_keys = ""
    for i in range(key_length):
        text_block = encrypted_text[i::key_length]
        text_blocks.append(text_block)
        assumed_keys += caesar_analyse_text_block(text_block)

    print(assumed_keys)
    print(vigenere_decrypt(encrypted_text, assumed_keys))


if __name__ == "__main__":
    open_text = read_text("clean_text.txt")
    encrypted_task = read_text("encrypted_task.txt")
    encrypted_coincedence = index_of_coincidence(encrypted_task)
    print(f"Відкритий текст. I_r={index_of_coincidence(open_text)}")
    print(f"Зашифрований текст (9 варіант)I_r={encrypted_coincedence}")
    for key in KEYS:
        encrypted_text = vigenere_encrypt(open_text, key)
        # print(encrypted_text, end="\n\n\n")
        print(f"Шифротекст з ключем \"{key}\" (r={len(key)}). "
              f"I_r={index_of_coincidence(encrypted_text)}")

    print(encrypted_task)
    find_key_length(encrypted_task)
    caesar_analyse_text(encrypted_task, 17)
    caesar_analyse_text(encrypted_task, 17)

    #key_lengths = [len(key) for key in KEYS if len(key) <= 5]
    #coincidence_values = [index_of_coincidence(vigenere_encrypt(open_text, key)) for key in KEYS if len(key) <= 5]
    #plot_coincidence_index(key_lengths, coincidence_values, encrypted_coincedence)

