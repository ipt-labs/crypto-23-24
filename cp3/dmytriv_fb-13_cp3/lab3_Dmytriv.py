from collections import Counter

ciphered = '13.txt'
result = 'encrpt_t13.txt'

alph = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = len(alph)
M = m**2

bi_in_lan = ['ст', 'но', 'то', 'на', 'ен']
often = ['о', 'е', 'а']
rarely = ['ф', 'щ', 'ь']
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
#a^-1
def inverse_mod(a, mod, v = None):
    if v is None:
        v = [0, 1]
    if a == 0 or gcd(a, mod) != 1:
        return None
    else:
        d = mod % a
        q = mod // a
        v.append((v[len(v) - 2] - q * v[len(v) - 1]))
        if d != 0:
            mod, a = a, d
            return inverse_mod(a, mod, v)
        else:
            return v[len(v) - 2]

# ax = b(mod n)
def l_comp(a, b, n, x):
    if x is None:
        x = []
    a, b = a % n, b % n
    d = gcd(a, n)
    if d == 1:
        if inverse_mod(a, n) is not None:
            a_inv = inverse_mod(a, n)
            x.append((a_inv*b) % n)
            return x
    elif d > 1 and b % d == 0:
        a1, b1, n1 = int(a/d), int(b/d), int(n/d)
        l_comp(a1, b1, n1, x)
        for i in range(1, d):
            x1 = x[0]
            r = (x1 + n1*i) % n
            x.append(r)
        return x
    else:
        return None

def often_bigram(text, option):
    bigrams = [text[num: num + 2] for num in range(0, len(text) - 1, 2)]
    no_duplicates = set(bigrams)
    res = {bigram: bigrams.count(bigram) / len(bigrams) for bigram in no_duplicates}
    if option == 1: # 5 найчастіших біграм
        keys = list(set(res.values()))
        keys.sort(reverse=True)
        return [key for key, value in res.items() if value in keys[:4]]
    else: #відсортований словник частот біграм
        return dict(sorted(res.items(), key=lambda item: item[1], reverse=True))

def convert_bigram(bi):
    return (alph.index(bi[0]))*m+alph.index(bi[1])

def check_text(text):
    check = 0
    dict_with_res = Counter(text)
    sorted_dict = dict(sorted(dict_with_res.items(), key=lambda item: item[1], reverse=True))
    l_text = list(sorted_dict.keys())[:3]
    for i in l_text:
        if i in often:
            check += 1
    l_text = list(sorted_dict.keys())[-3:]
    for j in l_text:
        if j in rarely:
            check += 1
    bi_text = often_bigram(text, 1)
    for b in bi_text:
        if b in bi_in_lan:
            check += 1
    return check

def decryption(data, a, b):
    decrpt = ""
    for num in range(0, len(data) - 1, 2):
        bi = data[num: num + 2]
        Y = convert_bigram(bi)
        X = (l_comp(a, Y - b, M, None)[0])
        bi1 = X // 31
        bi2 = X % 31
        decrpt += alph[int(bi1)]
        decrpt += alph[int(bi2)]
    return decrpt


def what_key(text, bi_in_lan, res_file):
    bi_in_cph = often_bigram(text,  1)
    print("Біграми з найбільшою частотою: ", bi_in_cph)
    var_keys = []
    for i in range(len(bi_in_lan)):
        for j in range(len(bi_in_lan)):
            for q in range(len(bi_in_cph)):
                for w in range(len(bi_in_cph)):
                    if i != j and q != w:
                        X1, X2 = convert_bigram(bi_in_lan[i]), convert_bigram(bi_in_lan[j])
                        Y1, Y2 = convert_bigram(bi_in_cph[q]), convert_bigram(bi_in_cph[w])
                        X, Y = X1 - X2, Y1 - Y2
                        if inverse_mod(X, m**2,None) is not None:
                            a = l_comp(X, Y, m**2, None) # a = (X1 - X2)^(-1) (Y1-Y2) mod m^2
                            if a is not None:
                                for c in a:
                                    if c > 0 and inverse_mod(c, M, None) is not None and c not in [key[0] for key in var_keys]:
                                        b = (Y1 - c*X1) % M #b = (Y1 - aX1) mod m^2
                                        if b > 0:
                                            decr_t = decryption(text, c, b)
                                            var_keys.append((c, b))
                                            if check_text(decr_t) > 7:
                                                print(f'Ключ а - {c}, b - {b}')
                                                print("Розшифрований текст: ", decr_t)
                                                res_file.write(decr_t)

    return var_keys

with open(ciphered, 'r', encoding='utf-8') as t:
    cphrd_text = t.read()
with open(result, 'w', encoding='utf-8') as ws:
    what_key(cphrd_text, bi_in_lan, ws)


