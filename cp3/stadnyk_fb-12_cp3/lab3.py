ALPHABET = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
FREQUENT_BIGRAMS_OPEN_TEXT = ['ст', 'но', 'то', 'на', 'ен']
IMPOSSIBLE_BIGRAMS = ['аы', 'оы', 'иы', 'ыы', 'уы', 'еы', 'аь', 'оь', 'иь', 'ыь', 'уь', 'еь', 'юы', 'яы', 'эы', 'юь',
                      'яь', 'эь', 'ць', 'хь', 'кь']


def euclidean_algorithm(a, b):
    if not a:
        return b, 0, 1

    gcd, u1, v1 = euclidean_algorithm(b % a, a)
    u = v1 - (b // a) * u1
    v = u1

    return gcd, u, v


def modular_linear_equation_solver(a, b, n):
    a = a % n
    b = b % n

    d, u, v = euclidean_algorithm(a, n)
    if b % d != 0:
        return []

    x0 = (u * (b // d)) % n
    if x0 < 0:
        x0 += n

    return [(x0 + i * (n // d)) % n for i in range(d)]


def calculate_frequencies(text):
    frequencies = {}
    bigrams_count = 0
    for i in range(0, len(text) - 1, 2):
        bigram = text[i:i + 2]
        bigrams_count += 1
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1
    normalized_frequencies = {bigram: frequency / bigrams_count for bigram, frequency in frequencies.items()}
    return normalized_frequencies


def decipher_text(text, a=None, b=None):
    if a is None or b is None:
        return text
    deciphered_text = ''
    for i in range(0, len(text) - 1, 2):
        y = get_bigram_id(text[i:i + 2])
        x = (euclidean_algorithm(a, len(ALPHABET) ** 2)[1] * (y - b)) % (len(ALPHABET) ** 2)
        deciphered_text += ALPHABET[x // len(ALPHABET)] + ALPHABET[x % len(ALPHABET)]
    return deciphered_text


def get_bigram_id(bigram):
    return ALPHABET.index(bigram[0]) * len(ALPHABET) + ALPHABET.index(bigram[1])


def generate_key(bigram1, bigram2):
    x1, y1 = get_bigram_id(bigram1[0]), get_bigram_id(bigram1[1])
    x2, y2 = get_bigram_id(bigram2[0]), get_bigram_id(bigram2[1])
    roots = modular_linear_equation_solver(x1 - x2, y1 - y2, len(ALPHABET) ** 2)
    if not roots:
        return
    keys = []
    for root in roots:
        a = root
        b = (y1 - a * x1) % (len(ALPHABET) ** 2)
        keys.append((a, b))
    return keys


def generate_keys(open_bigrams, cyphered_bigrams):
    pairs = [(open_bigram, cyphered_bigram) for open_bigram in open_bigrams for cyphered_bigram in cyphered_bigrams]
    keys = []
    for i in pairs:
        for j in pairs:
            if i == j or i[1] == j[1]:
                continue
            roots = generate_key(i, j)
            if roots:
                keys.extend(roots)
    return set(keys)


if __name__ == '__main__':
    with open('input.txt', 'r', encoding='utf8') as file:
        input_text = file.read()

    frequencies = calculate_frequencies(input_text)
    frequencies_list = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:5]
    top_bigrams_cyphered = [bigram[0] for bigram in frequencies_list]

    possible_keys = generate_keys(FREQUENT_BIGRAMS_OPEN_TEXT, top_bigrams_cyphered)
    print(f'Found {len(possible_keys)} possible keys')

    for a_value, b_value in possible_keys:
        deciphered_text = decipher_text(input_text, a=a_value, b=b_value)
        if all(impossible_bigram not in deciphered_text for impossible_bigram in IMPOSSIBLE_BIGRAMS):
            print(
                f'Found possible solution: a = {a_value}, b = {b_value}, deciphered text = {deciphered_text[:100]}...')
