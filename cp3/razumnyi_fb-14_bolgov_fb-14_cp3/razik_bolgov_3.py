allowed_letters = 'абвгдежзийклмнопрстуфхцчшщьыэюя'  # m = 31

# this dict was created by dict_allowed_letters()
allowed_letters_dict = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6,
                        'з': 7, 'и': 8, 'й': 9, 'к': 10, 'л': 11, 'м': 12, 'н': 13,
                        'о': 14, 'п': 15, 'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20,
                        'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ь': 26, 'ы': 27,
                        'э': 28, 'ю': 29, 'я': 30}


# def dict_allowed_letters():
#     """ Enumerate alphabet 0-31 """
#
#     global allowed_letters
#     enumerated_allowed_letters = {}
#
#     for i, j in enumerate(allowed_letters):
#         enumerated_allowed_letters[j] = i
#
#     print(enumerated_allowed_letters)


most_freq_bigram_lang = ['ст', 'но', 'то', 'на', 'ен']

most_freq_bigram_lab_1 = {'ст': 0.014725851715501, 'то': 0.011596177141305, 'ов': 0.011466851745677,
                          'но': 0.011406499894384, 'по': 0.011402189047863, 'на': 0.01097110439577,
                          'ко': 0.010496911278468, 'ал': 0.010346031650235, 'ли': 0.009958055463351,
                          'ос': 0.009936501230747, 'ен': 0.009776999909472}

not_allowed_bigrams_2 = ['аы', 'аь', 'бй', 'вй', 'гй', 'гф', 'гх', 'гц', 'гш', 'гщ', 'гы', 'гь', 'гю', 'дй',
                         'дф', 'дщ', 'еы', 'еь', 'жй', 'жх', 'жш', 'жщ', 'жы', 'жю', 'зй', 'зщ', 'иь', 'йй',
                         'йы', 'йь', 'кй', 'кщ', 'кы', 'кь', 'мй', 'нй', 'оы', 'оь', 'пй', 'пц', 'пщ', 'сй',
                         'сщ', 'тй', 'уы', 'уь', 'фг', 'фж', 'фз', 'фй', 'фк', 'фх', 'фц', 'фч', 'фш', 'фщ',
                         'фэ', 'фю', 'фя', 'хй', 'хщ', 'хы', 'хю', 'цб', 'цж', 'цй', 'цц', 'цш', 'цщ', 'ць',
                         'цю', 'ця', 'чй', 'чх', 'чц', 'чы', 'чю', 'шг', 'шж', 'шз', 'шй', 'шф', 'шщ', 'шы',
                         'шэ', 'шя', 'щд', 'щж', 'щз', 'щй', 'щл', 'щм', 'щп', 'щх', 'щц', 'щч', 'щш', 'щы',
                         'щэ', 'щю', 'щя', 'ыы', 'ыь', 'ьй', 'ьы', 'ьь', 'эа', 'эв', 'эе', 'эж', 'эз', 'эи',
                         'эо', 'эу', 'эц', 'эч', 'эщ', 'эы', 'эь', 'ээ', 'эю', 'эя', 'юы', 'юь', 'яы', 'яь']


def gcd_(a, b):
    """ Euclid algorithm to find gcd """

    if a == 0:
        return b, 0, 1

    gcd, v1, u1 = gcd_(b % a, a)

    u = u1 - (b // a) * v1
    v = v1

    return gcd, u, v


def find_reverse_a(a, m):
    """ Find a**-1 mod m """

    g, x, y = gcd_(a, m)
    if g != 1:
        return None
    else:
        return x % m


def solve_linear_congruence(a, b, m):
    """ Solve ax = b mod(m) """

    gcd, x, y = gcd_(a, m)

    if not b % gcd == 0:
        return []
    else:
        a = a // gcd
        b = b // gcd
        m = m // gcd

        x = b * find_reverse_a(a, m) % m
        solutions = [(x + m * k) for k in range(gcd)]  # x_formula = x + m*k, k є Z

        return solutions


def bigram_frequency(text_to_freq):
    """ Count the frequency of top 5 bigrams """

    global allowed_letters
    bigram_freq_dict = {}

    mass = []
    for i in range(0, len(text_to_freq), 2):
        bigram = text_to_freq[i:i + 2]
        mass.append(bigram)
    mass_unique = []
    [mass_unique.append(x) for x in mass if x not in mass_unique]

    for i in mass_unique:
        bigram_freq_dict[i] = mass.count(i)

    for i in bigram_freq_dict:
        bigram_freq_dict[i] = round(bigram_freq_dict[i] / len(mass), 15)

    # print(bigram_freq_dict)
    sorted_f = dict(sorted(bigram_freq_dict.items(), key=lambda item: item[1], reverse=True)[:5])

    # print(sorted_f)
    return sorted_f


def bigram_to_number(bigram):
    """ Find bigram (x1, x2) letter equivalent
     example:
     (в, б) -> X = 2*31+1=63 """

    x1 = allowed_letters_dict[bigram[0]]
    x2 = allowed_letters_dict[bigram[1]]

    X = x1 * 31 + x2

    return X


def key_finder():
    """ Find all possible keys with given bigrams """

    potential_keys = []
    potential_bigram_comp = []

    for i in most_freq_bigram_lang:
        for j in bigram_freq_top:
            potential_bigram_comp.append((i, j))
    # print(potential_bigram_comp)

    for i in potential_bigram_comp:
        for j in potential_bigram_comp:

            if i == j:
                continue

            x_ = bigram_to_number(i[0])
            x__ = bigram_to_number(j[0])

            # print(x_, x__)

            y_ = bigram_to_number(i[1])
            y__ = bigram_to_number(j[1])

            # print(y_, y__)

            a_a = solve_linear_congruence(x_ - x__, y_ - y__, 31**2)
            # print(a_a)

            for a in a_a:
                b_b = (y_ - a*x_) % (31**2)
                potential_keys.append((a, b_b))

        # print(potential_keys)
    return set(potential_keys)  # to avoid repetitions


def decrypt_text(poten_keys):
    """ Decrypt text using affine cipher """

    possible_keys = poten_keys
    for i in possible_keys:

        a = i[0]
        b = i[1]

        plaintext = ''
        if find_reverse_a(a, 31**2) is None:
            continue

        for j in range(0, len(ciphertext)-1, 2):
            Xi = (find_reverse_a(a, 31**2) * (bigram_to_number(ciphertext[j:j + 2]) - b)) % (31**2)
            plaintext += allowed_letters[Xi // 31] + allowed_letters[Xi % 31]

        if not_allowed_bigram_test(plaintext):
            print(f'Key: ({a}, {b}) with text: {plaintext}')   # (13, 151)
        else:
            continue


def not_allowed_bigram_test(text):
    """ Check whether the text is genuine """

    global not_allowed_bigrams_2

    for i in not_allowed_bigrams_2:
        if i in text:
            return False
    return True


if __name__ == '__main__':

    # Open ciphertext
    with open('to_decrypt_01.txt', 'r', encoding='utf8') as f1_read:
        ciphertext = f1_read.read()
        ciphertext = ciphertext.replace('\n', '')

    # Find top 5 bigram frequencies of ciphertext
    bigram_freq_top = bigram_frequency(ciphertext)
    print(bigram_freq_top)

    # Compare bigrams to find possible keys
    all_potential_keys = key_finder()
    print(all_potential_keys)

    # Decrypt text using found keys and check whether this text is valid for language
    decrypt_text(all_potential_keys)

