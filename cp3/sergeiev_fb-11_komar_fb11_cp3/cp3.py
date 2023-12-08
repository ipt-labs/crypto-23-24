from math import gcd

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'


# ---------------- завдання 1
def extended_euclidean(a, m):
    if m == 0:
        return a, 1, 0
    gcd_num, x, y = extended_euclidean(m, a % m)
    x, y = y, x - (a // m) * y
    return gcd_num, x, y


def modular_inverse(a, m):
    if gcd(a, m) != 1:
        return None

    _, x, _ = extended_euclidean(a, m)
    return x % m


def lin_congr(a, b, m):
    gcd_num, x, y = extended_euclidean(a, m)
    if b % gcd_num != 0:
        return None

    x0 = (x * (b // gcd_num)) % m
    solutions = []
    for i in range(gcd_num):
        solution = (x0 + i * (m // gcd_num)) % m
        solutions.append(solution)
    return solutions


# ---------------- завдання 2
def frequency_bigram(text, step_num):
    bigrams = {}
    for i in range(len(text) - step_num):
        bigram = text[i] + text[i + step_num]
        if bigram in bigrams:
            continue
        else:
            bigrams[bigram] = text.count(bigram)

    freq_bigram = {num: bigrams[num] / sum(bigrams.values()) for num in bigrams.keys()}
    sorted_bigrams = dict(sorted(freq_bigram.items(), key=lambda x: x[1], reverse=True))
    return list(sorted_bigrams.keys())[:5]


# ---------------- завдання 3
def bigrams_pairs(bigram_teor, bigram_encr):
    bigrams = [(teor, encr) for teor in bigram_teor for encr in bigram_encr]
    pairs = []
    for i in bigrams:
        for j in bigrams:
            if not (j, i) in pairs and i[0] != j[0] and i[1] != j[1]:
                pairs.append((i, j))
    return pairs


def find_key(pairs):
    keys = []
    for pair in pairs:
        x1, y1 = alphabet.index(pair[0][0][0]) * 31 + alphabet.index(pair[0][0][1]), \
                 alphabet.index(pair[0][1][0]) * 31 + alphabet.index(pair[0][1][1])

        x2, y2 = alphabet.index(pair[1][0][0]) * 31 + alphabet.index(pair[1][0][1]), \
                 alphabet.index(pair[1][1][0]) * 31 + alphabet.index(pair[1][1][1])

        solutions = lin_congr(x1 - x2, y1 - y2, 31 ** 2)
        if solutions is not None:
            key = [(a, (y1 - a * x1) % (31 ** 2)) for a in solutions]
            keys.extend(key)
    return keys


# ---------------- завдання 4-5
def decrypt(text, key):
    result = ""
    for i in range(0, len(text) - 1, 2):
        inverted = modular_inverse(key[0], 31 ** 2)
        if inverted is None:
            return None

        y = alphabet.index(text[i]) * 31 + alphabet.index(text[i + 1])
        x = (inverted * (y - key[1])) % (31 ** 2)
        result += (alphabet[x // 31] + alphabet[x % 31])
    return result


def check_text(text, keys):
    impossible = ['аы', 'оы', 'иы', 'ыы', 'уы', 'еы', 'аь', 'оь', 'иь', 'ыь', 'уь', 'еь', 'юы', 'яы',
                  'эы', 'юь', 'яь', 'эь', 'ць', 'хь', 'кь', 'ьь', 'йй', 'йь', 'йы', 'ыю']
    for key in keys:
        result = decrypt(text, key)
        if result is not None and not any(bigram in result for bigram in impossible):
            print(f'Ключ: {key}')
            with open("decrypted.txt", 'w', encoding='utf-8') as file:
                file.write(result)
            return


with open('07.txt', 'r', encoding='utf-8') as file:
    text = file.read().replace('\n', '')

freq_bigrams_teor = ['ст', 'но', 'то', 'на', 'ен']
freq_bigrams_encr = frequency_bigram(text, 1)
print(f'5 найчастіших біграм шифротексту: {freq_bigrams_encr}')

pairs = bigrams_pairs(freq_bigrams_teor, freq_bigrams_encr)

keys = find_key(pairs)

check_text(text, keys)
