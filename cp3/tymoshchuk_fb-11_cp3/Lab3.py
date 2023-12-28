from collections import Counter
from itertools import product
import re 


alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"

def find_possible_mappings(top_encrypted_bigrams, top_plain_bigrams):
    possible_mappings = []

    for i, encrypted_bigram1 in enumerate(top_encrypted_bigrams):
        for j, plain_bigram1 in enumerate(top_plain_bigrams):
            for k, encrypted_bigram2 in enumerate(top_encrypted_bigrams):
                for l, plain_bigram2 in enumerate(top_plain_bigrams):
                    # Перевіряємо, що Y1* не дорівнює Y1** і X1* не дорівнює X1**
                    if (encrypted_bigram1 != encrypted_bigram2) and (plain_bigram1 != plain_bigram2):
                        # Перевіряємо, чи обернута група не вже міститься в результаті
                        reverse_group = [
                            [encrypted_bigram2, plain_bigram2],
                            [encrypted_bigram1, plain_bigram1]
                        ]
                        if reverse_group not in possible_mappings:
                            mapping = [
                                [encrypted_bigram1, plain_bigram1],
                                [encrypted_bigram2, plain_bigram2]
                            ]
                            possible_mappings.append(mapping)

    return possible_mappings

def top_5_bigrams(text):
    bigrams = [text[i:i+2] for i in range(0, len(text)-1, 1)]
    bigram_freq = Counter(bigrams)
    sorted_bigram_freq = dict(sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True))
    top_5 = list(sorted_bigram_freq.keys())[:5] 
    
    return top_5

def validate_decryption(decrypted_text):
    # Забороені біграми
    forbidden_bigrams = ['аъ', 'аь', 'бй', 'бф', 'гщ', 'гъ', 'еъ', 'еь', 'жй', 'жц', 'жщ', 'жъ', 'жы', 'йъ', 'къ', 'лъ', 'мъ', 'оъ', 'пъ', 'ръ', 'уъ','уь', 'фщ', 'фъ', 'хы', 'хь', 'цщ', 'цъ', 'цю', 'чф', 'чц', 'чщ', 'чъ', 'чы', 'чю', 'шщ', 'шъ', 'шы', 'шю', 'щг', 'щж','щл', 'щх', 'щц', 'щч', 'щш', 'щъ', 'щы', 'щю', 'щя', 'ъа', 'ъб', 'ъг', 'ъд', 'ъз', 'ъй', 'ък', 'ъл', 'ън', 'ъо', 'ъп', 'ър','ъс', 'ът', 'ъу', 'ъф', 'ъх', 'ъц', 'ъч', 'ъш', 'ъщ', 'ъъ', 'ъы', 'ъь', 'ъэ', 'ыъ', 'ыь', 'ьъ', 'ьы', 'эа', 'эж', 'эи', 'эо','эу', 'эщ', 'эъ', 'эы', 'эь', 'эю', 'эя', 'юъ', 'юы', 'юь', 'яъ', 'яы', 'яь', 'ьь', 'гг']

    # Перевірка на наявність заборонених біграм
    for forbidden_bigram in forbidden_bigrams:
        if forbidden_bigram in decrypted_text:
            return False

    # Перевірка на наявність біграми "ст"
    top_5 = top_5_bigrams(decrypted_text)
    if "ст" not in top_5:
        return False
    
    return True

def convert_bigram_to_number(bigram):
    first_letter_index = alphabet.index(bigram[0])
    second_letter_index = alphabet.index(bigram[1])
    numeric_representation = first_letter_index * 31 + second_letter_index
    return numeric_representation

def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = gcdExtended(b % a, a)
        x, y = y - (b // a) * x, x
        return gcd, x, y

def modInverse(a, m):
    gcd, x, y = gcdExtended(a, m)
    if gcd == 1:
        return (x % m + m) % m
    else:
        return 0  

def linearCongruence(a, b, n):
    a = a % n
    b = b % n
    d, u, v = gcdExtended(a, n)

    if (d == 0 or b % d != 0):
        return []  

    x0 = (u * (b // d)) % n
    if (x0 < 0):
        x0 += n

    results = []
    for i in range(d):
        res = (x0 + i * (n // d)) % n
        results.append(res)

    return results

def find_possible_a_b_values(processed_mappings, alphabet_size):
    keys = []

    for mappings in processed_mappings:
        y1 = convert_bigram_to_number(mappings[0][0])
        y2 = convert_bigram_to_number(mappings[1][0])
        x1 = convert_bigram_to_number(mappings[0][1])
        x2 = convert_bigram_to_number(mappings[1][1])
        x = x1 - x2
        y = y1 - y2
        answers = linearCongruence(x, y, alphabet_size ** 2)
        for a in answers:
            if gcdExtended(a, alphabet_size)[0] == 1:
                b = (y1 - a * x1) % (alphabet_size ** 2)
                keys.append([a, b])
    return keys

def remove_duplicate_keys(possible_keys):
    unique_keys = []
    for key in possible_keys:
        if key not in unique_keys:
            unique_keys.append(key)
    return unique_keys

def convert_number_to_bigram(n):
    second = n%31 
    first = (n-second)//31
    bigram = alphabet[first]+alphabet[second] 
    return bigram

def affine_decrypt(text, keys):
    a = keys[0]
    b = keys[1]
    decrypted_text_num = []
    decrypted_text_t = []
    bigram_t = []

    for i in range(0, len(text) - 1, 2):
        bigram = f'{text[i] + text[i + 1]}'
        bigram_t.append(bigram)

    bigram_num = []

    for i in range(len(bigram_t)):
        bigram_num.append(convert_bigram_to_number(bigram_t[i]))

    for i in bigram_num:
        x = (modInverse(a, 961) * (i - b)) % (961)
        decrypted_text_num.append(x)

    for i in range(0, len(decrypted_text_num) - 1):
        get_bi = convert_number_to_bigram(decrypted_text_num[i])
        decrypted_text_t.append(get_bi)

    clear_text = ''.join(decrypted_text_t)
    return clear_text


def try_decryption_with_keys(ciphertext, possible_keys):
    for key in possible_keys:
        decrypted_text = affine_decrypt(ciphertext, key)  # Функція для розшифрування з використанням ключа
        is_valid = validate_decryption(decrypted_text)  # Функція для перевірки правильності розшифрування

        if is_valid:
            print("Decryption successful!")
            print(decrypted_text[:100])  # Вивести перші 100 символів розшифрованого тексту
            user_input = input("Accept this key? (T/F): ").strip().lower()

            if user_input == "t":
                return key
            elif user_input == "f":
                continue
            else:
                print("Invalid input. Continuing with the next key.")
        else:
            continue

    return None  # Якщо не вдалося знайти правильний ключ

with open('02.txt', 'r', encoding='utf-8') as file:
    encrypted_text = file.read().lower()
    encrypted_text = " ".join(encrypted_text.split())
    encrypted_text = re.sub( r'[^а-яё]', '', encrypted_text)


encrypted_top5 = top_5_bigrams(encrypted_text)
print("Top 5 encrypted bigrams: ", encrypted_top5)
common_top5 = ["ст", "то", "ен", "но", "ни"]

possible_mappings = find_possible_mappings(encrypted_top5, common_top5)
possible_keys = find_possible_a_b_values(possible_mappings, 31)
possible_keys = remove_duplicate_keys(possible_keys)

decryption_key = try_decryption_with_keys(encrypted_text, possible_keys)

if decryption_key is not None:
    print(f"Decryption key: {decryption_key}")
    decrypted_text = affine_decrypt(encrypted_text, decryption_key)
    with open("decrypted_task.txt", "w", encoding="utf-8") as file:
        file.write(decrypted_text)
else:
    print("Decryption unsuccessful. No valid key found.")
