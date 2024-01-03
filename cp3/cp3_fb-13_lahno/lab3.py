alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
alph = 31
alph_sq = alph**2
mcrb = ['ст', 'но', 'то', 'на', 'ен']  # most common russian bigrams
mccb = ['хк', 'ек', 'вю', 'пн', 'вх']  # most common ciphered bigrams
mcrl = ['о', 'е', 'а']  # most common russian letters
mrrl = ['ф', 'щ', 'ь']  # most rare russian letters


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x


def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    return x % m if g == 1 else None


def solve_linear_congruence(a, b, m):
    roots = []
    a, b = a % m, b % m
    g = gcd(a, m)
    if g == 1:
        a_inv = mod_inverse(a, m)
        roots.append((a_inv * b) % m)
        return roots
    elif g > 1 and b % g == 0:
        a1 = a // g
        b1 = b // g
        m1 = m // g
        roots = solve_linear_congruence(a1, b1, m1)
        roots.extend((roots[0] + m1 * i) % m for i in range(g))
        return roots
    else:
        return None


def find_possible_keys(mcrb, mccb, alphabet):
    possible_keys = []
    for i in range(len(mcrb)):
        for j in range(len(mcrb)):
            if i != j:
                for k in range(len(mccb)):
                    for v in range(len(mccb)):
                        if k != v:
                            x1 = bigram_to_numeric(mcrb[i], alphabet)
                            y1 = bigram_to_numeric(mccb[k], alphabet)
                            x2 = bigram_to_numeric(mcrb[j], alphabet)
                            y2 = bigram_to_numeric(mccb[v], alphabet)
                            x = x1 - x2
                            y = y1 - y2
                            if gcd(x, alph_sq) == 1 and mod_inverse(x, alph_sq):
                                c = solve_linear_congruence(x, y, alph_sq)
                                if c:
                                    for a in c:
                                        if a > 0 and gcd(a, alph_sq) == 1 and mod_inverse(a, alph_sq):
                                            b = (y1 - a * x1) % alph_sq
                                            possible_keys.append((a, b))
    return possible_keys


def bigram_to_numeric(bigram, alphabet):
    index1 = alphabet.index(bigram[0])
    index2 = alphabet.index(bigram[1])
    numeric = index1 * len(alphabet) + index2
    return numeric


def numeric_to_bigram(int, alphabet):
    bigram = ""
    letter1 = int // 31
    letter2 = int % 31
    bigram += alphabet[letter1]
    bigram += alphabet[letter2]
    return bigram


def decrypt_text_from_file(text, keys, alphabet):
    decrypted_texts = []
    for key in keys:
        decrypted = ""
        for letter in range(0, len(text) - 1, 2):
            bigram = text[letter: letter + 2]
            y = bigram_to_numeric(bigram, alphabet)
            c, b = key
            x = mod_inverse(c, alph_sq) * (y - b) % alph_sq
            decrypted += numeric_to_bigram(x, alphabet)
        decrypted_texts.append([key, decrypted])

    return decrypted_texts


def find_readible_text(text):
    counter = {char: text.count(char) for char in set(text) if char.isalpha() or char.isspace()}
    sorted_letters = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
    mcl = list(sorted_letters.keys())[:3]
    mrl = list(sorted_letters.keys())[-3:]
    return sum(i in mcrl for i in mcl) + sum(j in mrrl for j in mrl)


def final_text_checking(texts):
    for key, text in texts:
        if find_readible_text(text) > 1:
            return [key, text]


def opening(filename):
    with open(filename, 'r', encoding='utf8') as file:
        text = file.read()
    return text


if __name__ == "__main__":
    possible_keys = find_possible_keys(mcrb, mccb, alphabet)
    print("Possible Keys:")
    for key in possible_keys:
        print("a =", key[0],", b =", key[1])
    print(len(possible_keys))

    input_file = input("Введіть ім'я файлу для читання: ")
    ciphered_text = opening(input_file)
    all_decrypted_texts = decrypt_text_from_file(ciphered_text, possible_keys, alphabet)
    result = final_text_checking(all_decrypted_texts)

    if result:
        output_file = input("Введіть ім'я файлу для запису: ")
        key, text = result
        print("\nТекст розшифровано з ключем ({}, {})".format(key[0], key[1]))
        with open(output_file, 'w', encoding='utf8') as file:
            file.write(text)
    else:
        print("Розшифрування не вдалось.")


