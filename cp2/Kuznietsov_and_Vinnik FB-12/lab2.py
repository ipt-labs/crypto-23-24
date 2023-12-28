import re

def filter():
    with open("variant_2.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    # Робимо всі букви маленькими
    text = text.lower()

    # Прибираєм все, що не входить в російський алфавіт, лишаєм пробіли
    text = re.sub(r'[^\sа-я]', '', text)

    # Прибираємо подвійні пробіли, або всі пробіли
    text = re.sub(r'\s+', '', text)

    with open("variant_2.txt", 'w', encoding='utf-8') as file:
        file.write(text)

#filter()

def shifr_vigenera(key):

    with open('2.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    # Оголошуємо алфавіт, який ми будемо використовувати для шифрування.
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    result = []  # Список для зберігання зашифрованого тексту.

    key_index = 0  # Змінна для відстеження поточного індексу символа ключа.

    # Проходимо через кожен символ вхідного тексту.
    for char in text:

        char_index = alphabet.index(char)  # Знаходимо індекс поточної літери тексту.

        # Отримуємо поточний символ ключа
        key_char = key[key_index % len(key)]
        key_index += 1

        # Знаходимо індекс поточного символа ключа в алфавіті.
        key_char_index = alphabet.index(key_char)

        # Обчислюємо індекс символа зашифрованого тексту, додаючи індекси символів тексту та ключа.
        encrypted_char_index = (char_index + key_char_index) % len(alphabet)

        # Знаходимо символ зашифрованого тексту, використовуючи обчислений індекс.
        encrypted_char = alphabet[encrypted_char_index]

        # Додаємо символ зашифрованого тексту до списку зашифрованого тексту.
        result.append(encrypted_char)

    return ''.join(result)

key = 'суперкороваходитднем'

encrypted_text = shifr_vigenera(key)

with open('3.txt', 'w', encoding='utf-8') as file:
    file.write(encrypted_text)

def index_vidpovidnosti():
    with open("variant_2.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    dictionary = {}
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

    for char in alphabet:
        dictionary[char] = 0

    for item in list(text):
        if item in dictionary:
            dictionary[item] += 1

    print(dictionary)

    suma = 0
    for i in alphabet:
        suma += dictionary[i] * (dictionary[i] - 1)
    suma = (1/(len(text)*(len(text)-1))) * suma
    return print(suma)

#index_vidpovidnosti()

def index_vidpovidnosti_help(text):
    dictionary = {}
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

    for char in alphabet:
        dictionary[char] = 0

    for item in list(text):
        if item in dictionary:
            dictionary[item] += 1

    suma = 0
    for i in alphabet:
        suma += dictionary[i] * (dictionary[i] - 1)
    suma = suma/(len(text)*(len(text)-1))
    return suma

def find_r(r):
    with open("variant_2.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    suma_r = 0
    for offset in range(0, r):
        array = "".join([text[i] for i in range(offset, len(text) - r + 1, r)])
        suma_r += index_vidpovidnosti_help(array)

    suma_r = suma_r / r
    return print(suma_r)

def print_result():
    for i in range(2, 31):
        print(f"Lenkey: {i}")
        find_r(i)

print_result()

def find_key(r, mova):
    with open("variant_2.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    result_array = []

    for offset in range(0, r):
        array = "".join([text[i] for i in range(offset, len(text) - r + 1, r)])

        dictionary = {}
        alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

        for char in alphabet:
            dictionary[char] = 0

        for item in array:
            if item in dictionary:
                dictionary[item] += 1

        max_value = max(dictionary.values())
        keys_with_max_value = [key for key, value in dictionary.items() if value == max_value]
        keys_with_max_value_12 = keys_with_max_value[0]

        alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        alphabet_to_numbers = list(range(33))

        alphabet_to_numbers_dictionary = {}
        for word, number in zip(alphabet, alphabet_to_numbers):
            alphabet_to_numbers_dictionary[word] = number

        if keys_with_max_value_12 in alphabet_to_numbers_dictionary:
            keys_with_max_value_to_number = alphabet_to_numbers_dictionary[keys_with_max_value_12]

        if mova in alphabet_to_numbers_dictionary:
            mova_to_number = alphabet_to_numbers_dictionary[mova]

        result = (keys_with_max_value_to_number - mova_to_number) % 32

        number_to_leters_dictionary = {
            0: 'а',
            1: 'б',
            2: 'в',
            3: 'г',
            4: 'д',
            5: 'е',
            6: 'ж',
            7: 'з',
            8: 'и',
            9: 'й',
            10: 'к',
            11: 'л',
            12: 'м',
            13: 'н',
            14: 'о',
            15: 'п',
            16: 'р',
            17: 'с',
            18: 'т',
            19: 'у',
            20: 'ф',
            21: 'х',
            22: 'ц',
            23: 'ч',
            24: 'ш',
            25: 'щ',
            26: 'ъ',
            27: 'ы',
            28: 'ь',
            29: 'э',
            30: 'ю',
            31: 'я'
        }

        if result in number_to_leters_dictionary:
            result_in_buckva = number_to_leters_dictionary[result]

        result_array.append(result_in_buckva)

    a = ''.join(result_array)
    print(a)

find_key(14, "о")
find_key(28, "о")