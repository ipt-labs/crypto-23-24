from itertools import combinations

file_path = "12.txt"
with open(file_path, "r") as file:
    ciphertext = file.read()

text_bi = ['хк','ек', 'вю', 'пн', 'вх']

language_bi = ['ст', 'но', 'то', 'на', 'ен']

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
def gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd_value, x, y = gcd(b, a % b)
        return gcd_value, y, x - (a // b) * y


def inverse(a, m):
    gcd_value, x, y = gcd(a, m)

    if gcd_value != 1:
        # Оберненого за модулем числа не існує
        return None
    else:
        # Повертаємо обернене за модулем число (x модуло m)
        return x % m


def linear_congruence_solver(a, b, m):
    # Визначаємо найбільший спільний дільник та коефіцієнти x, y
    gcd_value, x, y = gcd(a, m)

    # Перевіряємо, чи рівняння має розв'язок
    if b % gcd_value != 0:
        # Рівняння не має розв'язків
        return []

    # Обчислюємо x0
    x0 = (inverse(a // gcd_value, m // gcd_value) * (b // gcd_value)) % (m // gcd_value)

    # Знаходимо всі можливі розв'язки x
    all_x = [(x0 + i * (m // gcd_value)) % m for i in range(gcd_value)]

    return all_x

def get_alphabet_index(letter):
    russian_alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
    return russian_alphabet.index(letter)

def simple_math_operation(a, b, m=31):
    result = a * m + b
    return result



def find_possible_key(text_bi, language_bi, alphabet):
    key_candidates = []

    for text_x, text_y in combinations(text_bi, 2):
        for language_x, language_y in combinations(language_bi, 2):
            try:
                a = (text_x - text_y) * inverse(language_x - language_y, alphabet ** 2) % (
                            alphabet ** 2)
                b = (text_x - a * language_x) % (alphabet ** 2)
                key_candidates.append((a, b))
            except TypeError:
                pass

    return key_candidates

def affine_decrypt(ciphertext, key_candidates):
    a, b = key_candidates
    m = 31  # Для английского алфавита, можно изменить для других языков

    if gcd(a, m) != 1:
        raise ValueError('Key "a" must be coprime to the modulus')

    decrypted_text = ''
    a_inv = inverse(a, m)

    for char in ciphertext:
        if char.isalpha():
            is_upper = char.isupper()
            char_index = ord(char.upper()) - ord('A')
            decrypted_index = (a_inv * (char_index - b)) % m
            decrypted_char = chr(decrypted_index + ord('A'))
            decrypted_text += decrypted_char.upper() if is_upper else decrypted_char.lower()
        else:
            decrypted_text += char

    return decrypted_text

def is_valid_decrypted_text(decrypted_text, invalid_bigrams=[]):
    for bigram in invalid_bigrams:
        if bigram.upper() in decrypted_text.upper():
            return False
    return True