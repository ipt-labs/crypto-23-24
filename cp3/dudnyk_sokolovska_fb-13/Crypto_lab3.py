from collections import defaultdict
from math import gcd
from typing import List
from itertools import combinations


frequent_bigrams = ["ст", "но", "то", "на", "ен"]
# ["то", "он", "на", "не", "по"]
alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
#           0123456789012345678901234567890 -> 31
non_tipical_bigrams = ["оь", "йы", "йъ", "йь", "эь", "ьь", "зь", "оы"]


# from lab1

def frequency_bigrams(text:str, stepUse:bool = True):
    step = 2 if stepUse else 1
    bigrams = defaultdict(int)
    for i in range(0, len(text)-1, step):
        bigram = text[i:i+2]
        bigrams[bigram] += 1
    return bigrams

def process_text(file_name:str):
    with open(file_name, "rt", encoding='utf-8') as file:
        text = file.read().lower().replace("\n", "").replace("ё", "е").replace(" ", "")
        symbols = "? , . … ; “ „ : -  ! ( ) * « » \ / — 1 2 3 4 5 6 7 8 9 0 №"
        for symbol in symbols.split():
            text = text.replace(symbol, "")
    return text

# 2
# for gcd: gcd(a, b)

def check_reversed_exist(num:int, modulo:int):

    """ шукаємо обернений елемент """

    if gcd(num, modulo) == 1: 
        for i in range(1, modulo):
            if (num * i) % modulo == 1:
                return i
        
    return None


def solve_linear_mod_expression(a:int, b:int, modulo:int):

    """ розв'язання рівнянь виду ax = b mod c """

    res = []
    if gcd(a , modulo) == 1:
        res.append(pow(a,-1,modulo) * b % modulo)
        # print(f"Рівняння {a}x = {b} mod({modulo}) : x =", res)
        return res
    elif gcd(a, modulo) > 1:
        d = gcd(a, modulo)
        # Перевірка на кратність b до НСД(a, modulo) та на можливість знайти обернений елемент
        if b % d != 0 or pow(a // d, -1, modulo // d) == None:  
            # print(f"Рівняння {a}x = {b} mod({modulo}) не має розв'язків")
            return res
        else:
            x = pow(a // d, -1, modulo // d) * (b // d) % (modulo // d)
            res = [x + (modulo // d) * i for i in range(d)]  # усі можливі корені
            # print(f"Усі можливі корені для рівняння {a}x = {b} mod({modulo}) : ", res)
            return res


# solve_linear_mod_expression(7, 4, 10)
# solve_linear_mod_expression(6, 1, 10)
# solve_linear_mod_expression(6, 8, 10)


def check_text(text:str, bigrams:List[str] = non_tipical_bigrams):

    """перевіряємо на наявність в тексті неможливих поєднань біграм"""

    if any(bigram in text for bigram in bigrams):
        return False
    return True


def encode_to_num(bigrams:List[str], alphabet:str = alphabet):

    """X = x[i] * m + x[i+1], де m це довжина алфавіту - нумерування біграм"""

    numsX = []
    for bigram in bigrams:
        a = bigram[0]
        b = bigram[1]
        numsX.append(alphabet.index(a) * len(alphabet) + alphabet.index(b))
    return numsX

def decode_to_bigram(bigrams_nums:List[int], alphabet:str = alphabet):

    """конвертувати біграми з циферного у буквенний вигляд"""

    bigrams  = []
    for bigram in bigrams_nums:
        l1 = alphabet[bigram // len(alphabet)]
        l2 = alphabet[bigram % len(alphabet)]

        decoded_bigram = l1+l2
        bigrams.append(decoded_bigram)

    return bigrams

def get_keys(text:str, frequent_bigrams:List[str] =frequent_bigrams, alphabet:str = alphabet):

    """шукаємо можливі ключі"""

    mod = len(alphabet)**2
    sorted_encrypted = sorted(frequency_bigrams(text).items(), key=lambda x: x[1], reverse=True)
    top_encrypted = list(dict(sorted_encrypted[:12]).keys())
    # print(top_encrypted)
    # print(frequent_bigrams)
    X = encode_to_num(frequent_bigrams)
    Y = encode_to_num(top_encrypted)

    X_combinations = list(combinations(range(len(X)), 2))
    Y_combinations = list(combinations(range(len(Y)), 2))
    # print(X)
    # print(Y)

    keys = defaultdict(int)

    for x in X_combinations:
        for y in Y_combinations:
            x1 = X[x[0]]
            x2 = X[x[1]]
            y1 = Y[y[0]]
            y2 = Y[y[1]]

            if x1 == y1 or x2 == y2 : continue
            # print(x1, x2, y1, y2)

            a_keys = solve_linear_mod_expression(x1 - x2, y1 - y2, mod)
            # print("a = ", a_keys, ", x1 = ", x1, ", x2 = ", x2, ", y1 = ", y1, ", y2 = ",  y2)
            b_keys = []
            for a in a_keys:
                b = (y1 - a*x1) % mod
                b_keys.append(b)
            keys[a] = b_keys
    # print(keys)
    return keys
            

def decipher(text: str, alphabet: str = alphabet):

    """ розшифровуємо текст"""

    mod = len(alphabet)**2
    keys = get_keys(text)
    numerated_bigrams = encode_to_num(list(frequency_bigrams(text).keys()))
    
    for a, b_vals in keys.items():
        for b in b_vals:
            if check_reversed_exist(a, mod) is None: 
                continue

            decrypted_nums = []

            for y in numerated_bigrams:
                x = (pow(a, -1, mod) * (y - b)) % mod
                decrypted_nums.append(x)
            # print(decrypted_nums)

            decrypted_text = ''

            decrypted_bigrams = decode_to_bigram(decrypted_nums)
            # print(decrypted_bigrams)
            # print(decrypted_bigrams)
            for bigram in decrypted_bigrams:
                decrypted_text += bigram
            # print(decrypted_text)

            if check_text(decrypted_text):
                print("Текст змістовний, створено файл")
                print(f"Ключі: a = {a}, b = {b}")

                with open("decrypted.txt", "w", encoding="utf-8") as file:
                    file.write(decrypted_text)
                    return
    print("Не вдалося знайти змістовний текст") 

# (13, 151)

def decipher_v2(text:str, alphabet:str=alphabet): 
    mod = len(alphabet)**2
    keys = get_keys(text)
    numerated_bigrams = encode_to_num(list(frequency_bigrams(text).keys()))

    decrypted_texts = {}    # [keys] : text

    for a, b_vals in keys.items():
        if check_reversed_exist(a, mod) is None: 
                continue
        for b in b_vals:
            decrypted_nums = []

            for y in numerated_bigrams:
                x = (pow(a, -1, mod) * (y - b)) % mod
                decrypted_nums.append(x)
            
            decrypted_text = ''
            decrypted_bigrams = decode_to_bigram(decrypted_nums)
            # print(decrypted_bigrams)
            for bigram in decrypted_bigrams:
                decrypted_text += bigram
            # print(decrypted_text)

            decrypted_texts[decrypted_text] = [a,b]

    for text, keys in decrypted_texts.items():
        if check_text(text):
            a, b = keys[0], keys[1]
            with open(f"decrypted_texts//decrypted{a}_{b}.txt", "w", encoding="utf-8") as file:
                    file.write(decrypted_text)

test_text = process_text("01_utf8.txt")
# get_keys(test_text)

decipher_v2(test_text)
# не виходить змістовний текст