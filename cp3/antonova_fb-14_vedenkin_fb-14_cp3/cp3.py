import math
from collections import Counter

alph = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

# НСД
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# обчисленням оберненого елементу за модулем із використанням розширеного алгоритму Евкліда
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return (x % m + m) % m

# розв’язуванням лінійних порівнянь
def solve_linear_equation(a, b, m):
    d, x, y = extended_gcd(a, m)
    ans = []
    if b % d == 0:
        a, b, m = a // d, b // d, m // d
        inv_a = modinv(a, m)
        x = (inv_a * b) % m
        for i in range(d):
            ans.append((x + i * m) % (m * d))
    return ans

def frequency_of_bigrams(txt, alph):
    c = Counter()
    for letter_first in alph:
        for letter_second in alph:
            bigram = letter_first + letter_second
            c[bigram] = 0
    for i in range(len(txt) - 1):
        bigram = txt[i] + txt[i + 1]
        c[bigram] += 1
    total_bigrams = sum(c.values())
    frequencies = {bigram: count / total_bigrams for bigram, count in c.items()}
    sorted_frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:5]
    return sorted_frequencies

def bigram_to_number(bigram, alph):
    if bigram[0] in alph and bigram[1] in alph:
        num = alph.index(bigram[0]) * len(alph) + alph.index(bigram[1])
        return num
    else:
        raise ValueError('Invalid bigram: {}'.format(bigram))

def make_system(txt):
    mode_bigrams_cipher = frequency_of_bigrams(txt, alph)
    bgrms = [(i, j[0]) for i in frequent_bigrams for j in mode_bigrams_cipher]
    math_statement = [(bgrm1, bgrm2) for bgrm1 in bgrms for bgrm2 in bgrms if bgrm1 != bgrm2 and bgrm1[0] != bgrm2[0] and bgrm1[1] != bgrm2[1]]
    return math_statement

def find_roots(set, alph):
    roots = []
    sub1 = bigram_to_number(set[0][0], alph) - bigram_to_number(set[1][0], alph)
    sub2 = bigram_to_number(set[0][1], alph) - bigram_to_number(set[1][1], alph)
    a = solve_linear_equation(sub1, sub2, len(alph) ** 2)
    for dig in a:
        if gcd(dig, len(alph) ** 2) == 1:
            b = (bigram_to_number(set[0][1], alph) - dig * bigram_to_number(set[0][0], alph)) % (len(alph) ** 2)
            roots.append((dig, b))
    return roots

def select_keys(txt):
    k = []
    system = make_system(txt)
    for pair in system:
        our_roots = find_roots(pair, alph)
        if our_roots:
            k.extend(our_roots)
    return k

def entropy(txt):
    total = 0
    frequency = Counter(txt)
    for i in frequency.values():
        i /= len(txt)
        if i > 0:
            total += i * math.log2(i)
    H = -total
    return H

def decrypt(txt, revealed_keys):
    deciphered = []
    a, b = revealed_keys[0], revealed_keys[1]
    for i in range(0, len(txt) - 1, 2):
        x = (modinv(a, len(alph) ** 2) * (bigram_to_number(txt[i:i + 2], alph) - b)) % (len(alph) ** 2)
        deciphered.append(alph[x // len(alph)] + alph[x % len(alph)])
    decrypted = ''.join(i for i in deciphered)
    return decrypted

def find_correct_keys(revealed_keys, txt):
    for i in revealed_keys:
        deciphered = decrypt(txt, i)
        d = [item[0] for item in sorted(Counter(deciphered).items(), key=lambda x: x[1], reverse=True)]
        if d[0] in frequent_letters:
            h_theor = 4.35
            h = entropy(decrypt(txt, i))
            if h_theor - 0.2 < h < h_theor + 0.2:  # перевіряємо чи ентропія розшифрованого тексту приближена до теоретичного значення
                return i
    return -1

with open("08.txt", encoding='utf-8') as file:
    file_to_decrypt = file.read()
encrypted_text = ''.join(i for i in file_to_decrypt if i in alph)

frequent_bigrams = ['ст', 'но', 'то', 'на', 'ен']
frequent_letters = ['о', 'а', 'е']

more_frequent_bigrams = frequency_of_bigrams(encrypted_text, alph)
print("5 найчастіших біграм шифртексту: ", more_frequent_bigrams)

all_keys = select_keys(encrypted_text)
print("Всі кандидати на ключ: ", all_keys)

key = find_correct_keys(select_keys(encrypted_text), encrypted_text)
print("Пара правильних ключів: ", key)

decrypted_text_attempt = decrypt(encrypted_text, key)
print("Розшифрований текст: ", decrypted_text_attempt)