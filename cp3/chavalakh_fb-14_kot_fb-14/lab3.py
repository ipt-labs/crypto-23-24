import math
from itertools import product


def extended_euclidean(a, m):
    if m == 0:
        return a, 1, 0
    gcd_num, x, y = extended_euclidean(m, a % m)
    x, y = y, x - (a // m) * y
    return gcd_num, x, y


def modular_inverse(a, m):
    if math.gcd(a, m) != 1:
        return None
    _, x, _ = extended_euclidean(a, m)
    return x % m


def make_bigram_list(text):
    bigrams = []
    for i in range(0, len(text) - 1, 2):
        bigram = text[i:i+2]
        bigrams.append(bigram)
    return bigrams


def to_num(bigrams):
    bigrams_nums = []
    flipped_enum = {v: k for k, v in dict(enumerate(russian_alphabet)).items()}
    for i in range(len(bigrams)):
        bigrams_nums.append(flipped_enum[bigrams[i][0]] * mod + flipped_enum[bigrams[i][1]])
    return bigrams_nums


def find_ab():
    ab_list = []
    most_freq_bigram_num = to_num(most_freq_bigram_russian)
    most_freq_bigram_text_num = to_num(most_freq_bigram_text)
    combinations = [(q, w, e, r) for q, w, e, r in product(most_freq_bigram_num, most_freq_bigram_text_num, repeat=2) if r != w and e != q]
    for i in range(len(combinations)):
        x1, y1, x2, y2 = combinations[i]
        if modular_inverse(x1-x2, mod**2):
            a = (y1-y2) * modular_inverse(x1-x2, mod**2) % mod**2
            b = (y1 - a*x1) % mod**2
            ab_list.append((a, b))
    return set(ab_list)


def affine_cipher_decode(ab_list, bigrams):
    impossible = ['дй', 'юь', 'юы', 'эь', 'эы', 'фй']
    for key in ab_list:
        decoded_bigrams = []
        bigrams_txt = []
        if modular_inverse(key[0], mod**2):
            a = modular_inverse(key[0], mod**2)
            b = key[1]

        for bigram in bigrams:
            decoded = (bigram-b)*a % mod**2
            decoded_bigrams.append(decoded)
            
        for i in range(len(decoded_bigrams)):
            bigram = dict(enumerate(russian_alphabet))[math.floor(decoded_bigrams[i] / mod)] + dict(enumerate(russian_alphabet))[decoded_bigrams[i] % mod]
            bigrams_txt.append(bigram)
        decoded_text = "".join(bigrams_txt)
        
        finder = False
        for i in impossible:
            if i in decoded_text:
                finder = True
        if not finder:    
            print(f'Для ключа {key} розшифровано текст:\n{decoded_text}')



with open("path", "r", encoding="utf-8") as file:
    text = file.read().replace('\n', '')
    
russian_alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
mod = len(russian_alphabet)
most_freq_bigram_russian = ["ст", "но", "то", "на", "ен"]
most_freq_bigram_text = ['ээ', 'вд', 'чф', 'цг', 'гн']

affine_cipher_decode(find_ab(), to_num(make_bigram_list(text)))
