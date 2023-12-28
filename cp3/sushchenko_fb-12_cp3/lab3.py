alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
alph_len = len(alphabet)
bigram_top_freq = ["ст", "но", "то", "на", "ен"]


def bigram_freq(text):
    freqs = {}
    for i in range(0, len(text)-1, 2):
        bigram = text[i] + text[i+1]
        if bigram in freqs:
            freqs[bigram] += 1
        else:
            freqs[bigram] = 1

    freqs = dict(sorted(freqs.items(), key=lambda x: x[1], reverse=True))
    print(list(freqs.keys())[:5])
    return list(freqs.keys())[:5]


def alph_to_num(alph):
    result = []
    for i in alph:
        a = alphabet.index(i[0])
        b = alphabet.index(i[1])
        result.append(a * alph_len + b)
    return result


def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = ext_gcd(b % a, a)
        return gcd, y - (b // a) * x, x


def solve_congruence(a, b, n, d):
    if b % d == 0:
        gcd, a_inv, y = ext_gcd(a // d, n // d)
        x0 = (a_inv * (b // d)) % (n // d)

        solutions = [(x0 + i * (n // d)) % n for i in range(d)]
        return solutions
    else:
        return False


def find_keys(X, Y):
    keys = []
    for x1 in X:
        for y1 in Y:
            for x2 in X:
                for y2 in Y:
                    if x1 == x2 or y1 == y2:
                        pass
                    else:
                        gcd, x, y = ext_gcd(x1-x2, alph_len**2)
                        if gcd == 1:
                            a = ((y1-y2)*x) % alph_len**2
                            b = (y1 - a*x1) % alph_len**2
                            keys.append((a, b))
                        elif gcd > 1:
                            result = solve_congruence((x1-x2), (y1-y2), alph_len**2, gcd)
                            if result:
                                for a in result:
                                    b = (y1 - a * x1) % alph_len ** 2
                                    keys.append((a, b))
    print(keys)
    return keys


def decrypt(text, key):
    result = ""
    bigrams = []
    gcd, a, y = ext_gcd(key[0], alph_len ** 2)

    for i in range(0, len(text)-1, 2):
        bigrams.append(text[i] + text[i+1])
    bigrams = alph_to_num(bigrams)

    for i in bigrams:
        x = (a*(i-key[1])) % alph_len ** 2
        x_i1 = x // 31
        x_i2 = x % 31
        result += alphabet[x_i1]
        result += alphabet[x_i2]

    return result


def find_prop_text(text):
    denied = ["аь", "ьь", "ээ", "ыь", "йь", "йй", "цщ", "уь", "оь", "иь"]
    for i in denied:
        if i in text:
            return False
    return True


if __name__ == '__main__':
    with open("text.txt", "r", encoding="utf-8") as f:
        text = f.read()
        print(text)

    bigram_aplh = bigram_freq(text)
    keys = find_keys(alph_to_num(bigram_top_freq), alph_to_num(bigram_aplh))
    for key in keys:
        decrypted_text = decrypt(text, key)
        if find_prop_text(decrypted_text):
            print(decrypted_text)
            print(key)
