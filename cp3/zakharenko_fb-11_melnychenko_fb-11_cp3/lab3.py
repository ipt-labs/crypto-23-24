
from math import gcd

with open('08.txt', 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', '')

symbols = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
top_v_enc_bigrams = ['жц', 'дэ', 'цэ', 'ыб', 'оц']
freq_bigrams = ['ст', 'но', 'то', 'на', 'ен']

def euclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = euclid(b % a, a)
        return g, y - (b // a) * x, x


def solver(a, b, mod=31):
    g = gcd(a, mod)
    if g == 1:
        return [(euclid(a, mod)[1] * b) % mod]
    elif g > 1:
        if b % g != 0:
            return None
        x0 = (euclid(a // g, mod // g)[1] * (b // g)) % (mod // g)
        roots = []
        for i in range(g):
            roots.append(x0 + i * (mod // g))
        return roots


def create_pairs(b1, b2):
    bigrams = []
    pairs = []
    for normal in b1:
        for encrypted in b2:
            bigrams.append((normal, encrypted))
    for i in bigrams:
        for j in bigrams:
            if not i == j and not (j, i) in pairs and i[0] != j[0] and i[1] != j[1]:
                pairs.append((i, j))
    return pairs


pairs = create_pairs(freq_bigrams, top_v_enc_bigrams)


def get_x(bigram):
    return symbols.index(bigram[0]) * 31 + symbols.index(bigram[1])


def get_bigram(value):
    return symbols[value // 31] + symbols[value % 31]


def find_key(pair):
    x1, y1 = get_x(pair[0][0]), get_x(pair[0][1])
    x2, y2 = get_x(pair[1][0]), get_x(pair[1][1])
    roots = solver(x1 - x2, y1 - y2, 31 * 31)
    if roots is None:
        return None
    key = []
    for a in roots:
        key.append((a, (y1 - a * x1) % (31 * 31)))
    return key


def get_keys(pairs):
    keys = []
    for pair in pairs:
        key = find_key(pair)
        if key:
            for k in key:
                keys.append(k)
    return keys


keys = get_keys(pairs)


def decrypt(text, key):
    result = ""
    for i in range(0, len(text) - 1, 2):
        y = get_x(text[i: i + 2])
        x = (euclid(key[0], 31 * 31)[1] * (y - key[1])) % (31 * 31)
        result += get_bigram(x)
    return result


def check(text, keys):
    net = ['аь','еь', 'юы', 'яы', 'эы', 'юь', 'яь', 'оь', 'иь', 'ыь', 'уь', 'аы', 'эь', 'ць', 'хь', 'кь', 'оы', 'иы', 'ыы', 'уы', 'еы']
    yes = True
    for key in keys:
        result = decrypt(text, key)
        for bigram in net:
            if bigram in result:
                yes = False
        if yes:
            print(key)
            print(result)
            return
        yes = True


check(text, keys)
