alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
m = len(alphabet)
def calculate_index_of_coincidence(text):
    frequencies = {}
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    ic_value = sum([(count * (count - 1)) for count in frequencies.values()]) / (len(text) * (len(text) - 1))
    return ic_value


def count_bi(text):
    c2_nocross = dict()
    i = 0
    while True:
        if (i >= len(text) - 1):
            break
        b = text[i] + text[i + 1]
        
        if b not in c2_nocross.keys():
            c2_nocross[b] = 0
        c2_nocross[b] += 1
        i += 2
    return c2_nocross


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None
    else:
        return x % m


def count_a_b(bi, most_bi):
    for bi1 in bi:
        Y1 = alphabet.find(bi1[0]) * m + alphabet.find(bi1[1])
        for bi2 in bi:
            if bi2 != bi1:
                
                Y2 = alphabet.find(bi2[0]) * m + alphabet.find(bi2[1])
                
                result = dict()
                for mos1 in most_bi:
                    X1 = alphabet.find(mos1[0]) * m + alphabet.find(mos1[1])
                    for mos2 in most_bi:
                        if mos2 != mos1:
                            X2 = alphabet.find(mos2[0]) * m + alphabet.find(mos2[1])
                            d = extended_gcd(X1 - X2, m ** 2)[0]
                            if d == None:
                                continue
                            if d == 1:
                                a = ((Y1 - Y2) * mod_inverse(X1-X2, m**2)) % (m ** 2)
                                b = (Y1 - a * X1) % (m**2)
                                result[a] = b

                            elif d > 1:
                                if (Y1 - Y2) % d == 0:
                                    X0 = (Y1 - Y2) // d * mod_inverse((X1 - X2) // d, (m ** 2) // d)
                                    for i in range(d):
                                        a = (X0 + i * ((m ** 2) // d)) % (m ** 2)
                                        b = (Y1 - a * X1) % (m ** 2)
                                        result[a] = b

    return result


def decrypt(text, a, b):
    result = ''
    a = mod_inverse(a, m ** 2)
    if a == None:
        return -1
    i = 0
    while True:
        if (i >= len(text) - 1):
            break
        Y = alphabet.find(text[i]) * m + alphabet.find(text[i + 1])
        X = a * (Y - b) % (m ** 2)
        result += alphabet[X // m] + alphabet[X % m]
        i += 2
    return result


def decrypt_keys(text, keys):
    textes = dict()
    for i in keys:
        d_text = decrypt(text, i, keys[i]) 
        index = calculate_index_of_coincidence(d_text)

        if abs(index - 0.0553) < 0.01:
            textes[i, keys[i]] = d_text
    return textes



with open("04.txt", "r", encoding="utf8") as f:
    text = f.read().replace('\n', '')


the_most_uses_bi = ['ст', 'но', 'ен', 'то', 'на', 'ов', 'ни', 'ра', 'во', 'ко']
bi = list(dict(sorted(count_bi(text).items(), key=lambda item: -item[1])))[:5]
print(bi)
keys = count_a_b(bi, the_most_uses_bi)
print(decrypt_keys(text, keys))
