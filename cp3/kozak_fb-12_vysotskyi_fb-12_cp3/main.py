from re import sub

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
forbidden_bigrams = ['аь', 'ьь', 'ыы', 'ыь']


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


#save_text("encrypted_text.txt", clean_text("09_utf.txt"))


def count_bigrams(filepath, step=2):    # Підрахунок біграм
    text = read_text(filepath)
    bigram_dict = {}
    for i in range(0, len(text) - 1, step):
        bigram = text[i:i+2].replace(" ", "_")
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    bigram_dict = dict(sorted(bigram_dict.items(), key=lambda x: x[1], reverse=True))  # Сортування за значеннями ключів
    return bigram_dict


def extended_euclid(a, b):   # Розширений алгоритм Евкліда
    """ Повертає d=НСД(x,y) і x, y такі, що ax + by = d """
    if b == 0:
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y


def mod_inverse(a, m):   # Обернене за модулем
    gcd, x, y = extended_euclid(a, m)
    if gcd == 1:
        return x % m
    else:
        return None


def solve_equation(x1, x2, y1, y2):
    inverse = mod_inverse(x1 - x2, (len(ALPHABET) * len(ALPHABET)))
    if inverse:
        a = (inverse * (y1 - y2)) % (len(ALPHABET) * len(ALPHABET))
        b = (y1 - a * x1) % (len(ALPHABET) * len(ALPHABET))
        return [a, b]

def bigram_to_num(bigrams):
    list = []
    for bigram in bigrams:
        list.append(ALPHABET.index(bigram[0]) * len(ALPHABET) + ALPHABET.index(bigram[1]))
    return list

def bigram_to_letters(num):
    return ALPHABET[num // len(ALPHABET)] + ALPHABET[num % len(ALPHABET)]

def text_selection(text):
    return all(bigram not in text for bigram in forbidden_bigrams)


def affine_decrypt(encrypted_text, keys):
    for key in keys:
        a = key[0]
        b = key[1]
        text = ''
        for i in range(0, len(encrypted_text) - 1, 2):
            n = bigram_to_num([encrypted_text[i:i+2]])[0]
            inverse = mod_inverse(a, (len(ALPHABET) * len(ALPHABET)))
            if inverse is not None:
                text += bigram_to_letters((n - b) * inverse % (len(ALPHABET) * len(ALPHABET)))
        if text and text_selection(text):
            print(f"[{a},{b}]: ", text)


if __name__ == "__main__":

    encrypted_bigrams_frequency = list(count_bigrams("encrypted_text.txt").keys())[:5]  # 5 найчастіших біграм шифртексту
    print(encrypted_bigrams_frequency)
    most_frequent_bigrams = ["ст", "но", "то", "на", "ен"]  # 5 найчастіших біграм російської мови

    x = bigram_to_num(most_frequent_bigrams)
    y = bigram_to_num(encrypted_bigrams_frequency)

    keys = []
    for x1 in x:
        for y1 in y:
            for x2 in x:
                for y2 in y:
                    if x1 != x2 and y1 != y2:
                        res = solve_equation(x1, x2, y1, y2)
                        if res is not None and res not in keys:
                            keys.append(res)

    affine_decrypt(read_text('encrypted_text.txt'), keys)
