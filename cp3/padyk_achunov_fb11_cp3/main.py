import csv

COMMON_BIGRAMS: tuple = ("то", "ст", "на", "ов", "ал", "не", "го", "он", "ос", "ко")
IMPOSSIBLE_BIGRAMS: tuple = ('уь', 'эь', 'хь', 'яь', 'оь', 'еь', 'иь', 'аы', 'ыь', 'юь', 'ць', 'уы', 'иы', 'еы', 'яы', 'оы', 'аь', 'юы', 'эы')
ALPHABET: str = 'абвгдежзийклмнопрстуфхцчшщьыэюя'


def extended_euclidean(a: int, b: int) -> tuple:
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean(b % a, a)
        return gcd, y - (b // a) * x, x


def equation_solving(a: int, b: int, n: int) -> list or None:
    k1 = a // n
    k2 = b // n
    a = a - k1 * n
    b = b - k2 * n

    d, u, v = extended_euclidean(a, n)

    if d == 1:
        answ = u * b
        k = answ // n
        return [answ - k * n]
    else:
        if b % d == 0:
            a1 = a // d
            b1 = b // d
            n1 = n // d
            x0 = equation_solving(a1, b1, n1)
            return x0 + [i * n1 for i in range(d)]
        else:
            return None


def inverse(a):
    gcd, null, null = extended_euclidean(a, len(ALPHABET) ** 2)
    if gcd != 1:
        return None

    null, x, null = extended_euclidean(a, len(ALPHABET) ** 2)
    return x % len(ALPHABET) ** 2


def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    return text



def text_edit(text: str) -> str:
    text = text.strip()
    text = text.lower()
    text = ''.join(char for char in text if char in ALPHABET)
    return text


def bigram_create(text: str, step: int) -> list:
    return [text[i:i+2] for i in range(0, len(text), step)]


def bigram_to_number(bigram: str) -> int:
    return ALPHABET.index(bigram[0]) * len(ALPHABET) + ALPHABET.index(bigram[1])


def bigram_count(text: str, step: int) -> dict:
    bigram_dict: dict = {}
    for i in range(0, len(text), step):
        bigram = text[i:i+2]
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    return bigram_dict


def bigram_frequency(bigram_dict: dict) -> dict:
    frequency_dict: dict = {}
    bigram_amount: int = 0
    for value in bigram_dict.values():
        bigram_amount += value
    for bigram in bigram_dict:
        frequency_dict[bigram] = bigram_dict[bigram] / bigram_amount
    return frequency_dict


def return_top(frequency_dict: dict, count: int) -> tuple:
    sorted_bigrams = tuple(sorted(frequency_dict.keys(), key=lambda x: frequency_dict[x], reverse=True))
    top_bigrams = sorted_bigrams[:count]
    return top_bigrams


def generate_keys(common_bigrams: tuple, encrypted_bigrams: tuple) -> list:
    global ALPHABET
    keys: list = []
    for i in range(len(common_bigrams)):
        for j in range(len(common_bigrams)):
            for i1 in range(len(encrypted_bigrams)):
                for j1 in range(len(encrypted_bigrams)):
                    x1 = bigram_to_number(common_bigrams[i])
                    y1 = bigram_to_number(encrypted_bigrams[i1])
                    x2 = bigram_to_number(common_bigrams[j])
                    y2 = bigram_to_number(encrypted_bigrams[j1])
                    if x1 != x2 and y1 != y2:
                        solutions = equation_solving(x1 - x2, y1 - y2, len(ALPHABET) ** 2)
                        if solutions is not None:
                            key = [(solution, (y1 - solution * x1) % (len(ALPHABET) ** 2)) for solution in solutions]
                            keys.extend(key)
    return list(set(keys))


def save_dict_to_csv(data_dict, file_name):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Bigram', 'Freq'])
        writer.writerows(data_dict.items())


def decrypt_affine(encrypted_text: str, a: int, b: int) -> str or None:
    global ALPHABET
    decrypted_text: str = ''
    a_inverse = inverse(a)
    if a_inverse is None:
        return None

    for i in range(0, len(encrypted_text)-1, 2):
        bigram = encrypted_text[i:i+2]
        y = bigram_to_number(bigram)
        x = (a_inverse * (y - b)) % (len(ALPHABET) ** 2)
        decrypted_text += ALPHABET[x // len(ALPHABET)] + ALPHABET[x % len(ALPHABET)]

    return decrypted_text


def main():
    encrypted_text = read_file('15.txt')
    encrypted_text = text_edit(encrypted_text)
   

    count = bigram_count(encrypted_text, step=2)
    freq = bigram_frequency(count)
    save_dict_to_csv(freq, 'Frequencies.csv')

    encrypted_bigrams = return_top(count, 5)
    print(f'Most common bigrams in encrypted text: {encrypted_bigrams}')

    keys = generate_keys(COMMON_BIGRAMS, encrypted_bigrams)
    print(f'Found {len(keys)} possible keys')

    for key in keys:
        decrypted_text = decrypt_affine(encrypted_text, key[0], key[1])
        if decrypted_text and all(bigram not in decrypted_text for bigram in IMPOSSIBLE_BIGRAMS):
            print(f'Key: {key}')
            print(f'Possible decrypted text: {decrypted_text}')


if __name__ == '__main__':
    main()
