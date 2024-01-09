from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
BIGRAMS = ["ст", "но", "то", "на", "ен"]
FORBIDEN_BIGRAMS = ['аь','эь','ыь','иь','юь','оь','уь','еь','яь','ьь','йь']
M = len(ALPHABET)

def decrypt(text, key):

    a = key[0]
    b = key[1]
    plaintext = ''

    for i in range(0, len(text) - 1, 2):
        if find_inverse(a, M ** 2) != None:
            bigram = (bigram_to_number(text[i:i+2]) - b) * find_inverse(a, M ** 2) % M ** 2
            plaintext += ALPHABET[bigram // M] + ALPHABET[bigram % M]

    if plaintext and is_valid(plaintext):
        print(f'Ключ [{a},{b}]:', plaintext)

def count_bigrams(text):

    top_bigrams = []
    for i in range(0, len(text), 2):
        top_bigrams.append(text[i:i + 2])

    nob = Counter(top_bigrams)
    top_bigrams = dict(sorted(nob.items(), key=lambda item: item[1], reverse=True)[:12])

    print(top_bigrams)

    return top_bigrams


def bigram_to_number(b):
    return ALPHABET.index(b[0])*M + ALPHABET.index(b[1])


def gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def find_inverse(a, m):
    g, x, y = gcd(a, m)

    if g == 1:
        return x % m

def find_key(eq1, eq2):

    [x1, y1], [x2, y2] = eq1, eq2
    m = M**2

    if find_inverse(x1 - x2, m):
        a = (find_inverse(x1 - x2, m) * (y1 - y2)) % m
        b = (y1-a*x1) % m
        return [a, b]

def is_valid(text):
    for i in FORBIDEN_BIGRAMS:
        if i in text:
            return False
    return True


if __name__ == "__main__":
    with open('06.txt', 'r', encoding='utf-8') as file:
        encrypted = file.read().replace('\n', '')

    X = []
    for b in BIGRAMS:
        X.append(bigram_to_number(b))
    Y = []
    for b in count_bigrams(encrypted).keys():
        Y.append(bigram_to_number(b))

    eqs = []
    for x in X:
        for y in Y:
            eqs.append([x, y])

    keys = []
    for i in eqs:
        for j in eqs:
            key = find_key(i, j)
            if key and key not in keys:
                keys.append(key)

    print(f'Потеціальні ключі:\n{keys}')
    print(len(keys))

    for key in keys:
        decrypt(encrypted, key)

# 441, 310
