import re
from collections import Counter
import matplotlib.pyplot as plt

# Constants
UA_ALPHABET = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
RU_ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
def read_file(t):
    with open(t, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def clean_text(text):
    text = read_file(text).lower()
    return re.sub(r'[^абвгґдеєжзиіїйклмнопрстуфхцчшщьюя]', '', text)


def encrypt(plaintext, key, alphabet):
    key_length = len(key)
    key_as_int = [alphabet.index(i) for i in key]
    plaintext_int = [alphabet.index(i) for i in plaintext]
    ciphertext = ''
    for i in range(len(plaintext_int)):
        value = (plaintext_int[i] + key_as_int[i % key_length]) % len(alphabet)
        ciphertext += alphabet[value]
    return ciphertext


def decrypt(ciphertext, key, alphabet):
    key_length = len(key)
    key_as_int = [alphabet.index(i) for i in key]
    ciphertext_int = [alphabet.index(i) for i in ciphertext]
    plaintext = ''
    for i in range(len(ciphertext_int)):
        value = (ciphertext_int[i] - key_as_int[i % key_length]) % len(alphabet)
        plaintext += alphabet[value]
    return plaintext


def index_of_coincidence(text):
    n = len(text)
    quantity = Counter(text)
    index = sum(i * (i - 1) for i in quantity.values()) / (n * (n - 1))
    return index


def plot_histogram(indexes, lenghts):
    plt.plot(lenghts, indexes, marker='o', linestyle='-')
    plt.xlabel('Ключ')
    plt.ylabel('Індекс відповідності')
    plt.title('Індекси відповідності')
    plt.show()


def kron_symb(encrypted, r):
    dr = 0
    for i in range(len(encrypted[:-r])):
        if encrypted[i]==encrypted[i+r]:
            dr += 1
    print(f'Символ Кронекера для r = {r} : {dr}')
    return [r, dr]


if __name__ == '__main__':

    # ++++++++++ Завдання 1 ++++++++++
    text = clean_text('my.txt')
    keys = ['ой', 'три', 'чорт', 'пйать', 'скоровихідні', 'замісяцьновийрік']
    indexes = []

    print(f'Індекс відповідності ВТ: {index_of_coincidence(text)}\n')
    for i in keys:
        encrypted = encrypt(text, i, UA_ALPHABET)
        print(f'Ключ довжиною {len(i)}: {i}')
        print(encrypted)
        # Перевірка
        # print(decrypt(encrypted, i, UA_ALPHABET))

    # ++++++++++ Завдання 2 ++++++++++
        index = index_of_coincidence(encrypted)
        indexes.append(index)
        print(f'Індекс відповідності: {index}\n')

    indexes.insert(0, index_of_coincidence(text))
    keys.insert(0, '')
    plot_histogram(indexes, [len(i) for i in keys])



    # ++++++++++ Завдання 2 ++++++++++
    encrypted = read_file('var_6.txt').replace('\n', '')

    max_dr = [0, 0]
    for r in range(2, 37):
        dr = kron_symb(encrypted, r)
        if max_dr[1] < dr[1]:
            max_dr = dr
    # print(max_dr)

    # Знаходження ключа
    r = max_dr[0]
    blocks = [encrypted[i::r] for i in range(r)]

    l = 'о'
    key = ''
    for block in blocks:
        y = RU_ALPHABET.index(Counter(block).most_common()[0][0])
        x = RU_ALPHABET.index(l)
        key = key + (RU_ALPHABET[y - x])
    print(key)
    print(decrypt(encrypted, key, RU_ALPHABET))

    key = input('Введіть власний ключ: ')
    print(decrypt(encrypted, key, RU_ALPHABET))