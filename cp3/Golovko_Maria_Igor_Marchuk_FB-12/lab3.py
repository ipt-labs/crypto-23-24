from itertools import permutations
import math


alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
theoretical_bigrams = ('ст', 'но', 'то', 'на', 'ен')


def gcd(b, n):
    x0, x1 = 1, 0
    while n:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1

    return b, x0

def modinv(a, m):

    d, x = gcd(a, m)
    if d == 1:
        return d, x % m
    return d, None

def solve_linear_congruence(a, b, m):
    d, a_inv = modinv(a, m)

    if a_inv:
        return [(a_inv * b) % m]

    if not b % d:
        a, b, m = a / d, b / d, m / d
        x0 = (b * modinv(a, m)[1]) % m
        return [int(x0 + (i - 1) * m) for i in range(1, d + 1)]


def count_bigrams_from_text(text):
    bigram_without_overlap_counts = {}


    for i in range(len(text) - 1):
        bigram_without_overlap = text[i:i + 2]
        if bigram_without_overlap in bigram_without_overlap_counts:
            bigram_without_overlap_counts[bigram_without_overlap] += 1
        else:
            bigram_without_overlap_counts[bigram_without_overlap] = 1


    sorted_bigram_without_overlap = sorted(bigram_without_overlap_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_bigram_without_overlap

def count_a(x1, x2, y1, y2):
    x1 = alphabet.index(x1[0]) * len(alphabet) + alphabet.index(x1[1])
    x2 = alphabet.index(x2[0]) * len(alphabet) + alphabet.index(x2[1])

    y1 = alphabet.index(y1[0]) * len(alphabet) + alphabet.index(y1[1])
    y2 = alphabet.index(y2[0]) * len(alphabet) + alphabet.index(y2[1])

    results = solve_linear_congruence(y1 - y2, x1 - x2, len(alphabet) ** 2)

    if results is not None:
        return [x for x in [modinv(i, len(alphabet) ** 2)[1] for i in results] if x is not None]


def count_b(x1, y1, a):
    x1 = alphabet.index(x1[0]) * len(alphabet) + alphabet.index(x1[1])
    y1 = alphabet.index(y1[0]) * len(alphabet) + alphabet.index(y1[1])

    return (y1 - a * x1) % len(alphabet) ** 2


def all_possible_keys(cleaned_text, key_size=5):
    f_list = count_bigrams_from_text(cleaned_text)[:key_size]
    possible_keys = set() 

    for i in permutations(theoretical_bigrams, 2):
        for j in range(len(f_list) - 1):
            key_1 = count_a(i[0], i[1], f_list[j][0], f_list[j + 1][0])

            if key_1 is None:
                continue

            for solution in key_1:
                key = solution, count_b(i[0], f_list[j][0], solution)
                possible_keys.add(key)  

    return list(possible_keys) 

def decrypt(string, key):
    new_str = ''

    for i in range(0, len(string), 2):
        try:
            y = alphabet.index(string[i]) * len(alphabet) + alphabet.index(string[i + 1])
            x = (modinv(key[0], len(alphabet) ** 2)[1] * (y - key[1])) % len(alphabet) ** 2
            new_str += alphabet[x // len(alphabet)] + alphabet[x % len(alphabet)]
        except ValueError:
            print(f"Non-alphabet character found at position {i}: '{string[i]}' or '{string[i + 1]}'")
            return None

    return new_str

def find_entropy(decrypted_text):
    entropy_letter = 0.0
    total_letters = len(decrypted_text)

    # Підрахунок ентропії для літер
    sorted_letter_counts = {}
    for letter in decrypted_text:
        if letter in sorted_letter_counts:
            sorted_letter_counts[letter] += 1
        else:
            sorted_letter_counts[letter] = 1

    for count in sorted_letter_counts.values():
        probability = count / total_letters
        entropy_letter -= probability * math.log2(probability)

    return entropy_letter

def check_the_text(decrypted_text):
    if find_entropy(decrypted_text)>4.2 and find_entropy(decrypted_text)<4.4:
        return decrypted_text

def decrypt_and_check(file_path):
    with open(file_path, 'r', encoding='windows-1251') as file:
        text = file.read()

    cleaned_text = ''.join([char for char in text.lower() if char in alphabet])

    keys = all_possible_keys(cleaned_text)
    for key in keys:
        decrypted_text = decrypt(cleaned_text, key)
        if check_the_text(decrypted_text):
            print(f"Decrypted Text with Key {key}:")
            print(decrypted_text)
        

file_path = r"D:\\uni year 3\\crypto labs\\crypto-23-24\\cp3\\igor_marchuk_maria_holovko_fb-12\\ciphertext_variant1.txt"
print(decrypt_and_check(file_path))
