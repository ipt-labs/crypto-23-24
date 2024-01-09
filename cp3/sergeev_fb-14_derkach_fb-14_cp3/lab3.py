import collections

ALLOWED = 'абвгдежзийклмнопрстуфхцчшщьыэюя' 

allowed_dict = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6,
                        'з': 7, 'и': 8, 'й': 9, 'к': 10, 'л': 11, 'м': 12, 'н': 13,
                        'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20,
                        'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ь': 26, 'ы': 27,
                        'э': 28, 'ю': 29, 'я': 30}

frequent_bigram = ['ст', 'но', 'то', 'на', 'ен']

bigram_lab1 = {'ст': 0.0129641469,'но': 0.0121003107, 'то': 0.0172635207, 'на': 0.0112991988, 'ен': 0.010665352}

unwanted_bigram = ['аы', 'аь', 'яы', 'яь']


def gcd(a, b):
    if a == 0:
        return b, 0, 1

    gcd_var, v1, u1 = gcd(b % a, a)

    u = u1 - (b // a) * v1
    v = v1

    return gcd_var, u, v


def find_reverse_a(a, m):
    g, x, y = gcd(a, m)
    if g != 1:
        return None
    else:
        return x % m


def congruence(a, b, m):

    gcd_var, x, y = gcd(a, m)

    if not b % gcd_var == 0:
        return []
    else:
        a = a // gcd_var
        b = b // gcd_var
        m = m // gcd_var

        x = b * find_reverse_a(a, m) % m
        solutions = [(x + m * k) for k in range(gcd_var)]  # xn = x + m*k, k є Z

        return solutions


def bigram_frequency(dictionary):
    global ALLOWED

    bigram_frequency = {}
    bigram_list = [dictionary[i:i + 2] for i in range(len(dictionary))]
    bigram_unique_list = list(set(bigram_list))
    count_b = collections.Counter(bigram_list)

    for i in bigram_unique_list:
        bigram_frequency[i] = round(count_b[i] / len(bigram_list), 15)

    sorted_f = dict(sorted(bigram_frequency.items(), key=lambda item: item[1], reverse=True)[:5])

    return sorted_f


def bigram_num(bigram):
    x1 = allowed_dict[bigram[0]]
    x2 = allowed_dict[bigram[1]]

    X = x1 * 31 + x2

    return X

def find_key():
    potential_keys = set()

    potential_bigram_comp = [(i, j) for i in frequent_bigram for j in bigram_freq_top]

    for i in potential_bigram_comp:
        for j in potential_bigram_comp:
            if i == j:
                continue

            x_ = bigram_num(i[0])
            x__ = bigram_num(j[0])

            y_ = bigram_num(i[1])
            y__ = bigram_num(j[1])

            a_a = congruence(x_ - x__, y_ - y__, 31**2)

            potential_keys.update((a, (y_ - a*x_) % (31**2)) for a in a_a)

    return potential_keys

def decrypt_text(keys):

    for a, b in keys:
        if find_reverse_a(a, 31**2) is None:
            continue

        plaintext = ''.join(
            ALLOWED[(find_reverse_a(a, 31**2) * (bigram_num(ciphertext[j:j + 2]) - b)) % (31**2) // 31] +
            ALLOWED[(find_reverse_a(a, 31**2) * (bigram_num(ciphertext[j:j + 2]) - b)) % (31**2) % 31]
            for j in range(0, len(ciphertext)-1, 2)
        )

        if unwanted_bigram_test(plaintext):
            print(f'\n---Ключ: ({a}, {b})---\nТекст:\n{plaintext}')


def unwanted_bigram_test(text):

    global unwanted_bigram

    for i in unwanted_bigram:
        if i in text:
            return False
    return True


if __name__ == '__main__':

    with open('06.txt', 'r') as f1_read:
        ciphertext = f1_read.read()
        ciphertext = ciphertext.replace('\n', '')

    
    # 5 найчастіших біграм тексту
    bigram_freq_top = bigram_frequency(ciphertext)
    print(bigram_freq_top)

    # Можливі ключі
    all_potential_keys = find_key()
    print(all_potential_keys)

    # Розшифрування тексту
    decrypt_text(all_potential_keys)
    
