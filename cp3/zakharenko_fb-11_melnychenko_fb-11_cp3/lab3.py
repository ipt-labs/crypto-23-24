from math import gcd

def euclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = euclid(b % a, a)
        return g, y - (b // a) * x, x

def solver(a, b, mod):
    g = gcd(a, mod)
    if b % g != 0:
        return None
    x0 = (euclid(a // g, mod // g)[1] * (b // g)) % (mod // g)
    return [x0 + i * (mod // g) for i in range(g)]

def decrypt(text, key, symbols):
    result = ""
    mod = len(symbols) ** 2
    for i in range(0, len(text), 2):
        y = symbols.index(text[i]) * len(symbols) + symbols.index(text[i+1])
        x = (euclid(key[0], mod)[1] * (y - key[1])) % mod
        result += symbols[x // len(symbols)] + symbols[x % len(symbols)]
    return result

def find_key_and_decrypt(text, freq_bigrams, top_v_enc_bigrams, symbols):
    mod = len(symbols) ** 2
    for normal in freq_bigrams:
        for encrypted in top_v_enc_bigrams:
            x1, y1 = symbols.index(normal[0]) * len(symbols) + symbols.index(normal[1]), symbols.index(encrypted[0]) * len(symbols) + symbols.index(encrypted[1])
            for normal2 in freq_bigrams:
                for encrypted2 in top_v_enc_bigrams:
                    if normal != normal2 and encrypted != encrypted2:
                        x2, y2 = symbols.index(normal2[0]) * len(symbols) + symbols.index(normal2[1]), symbols.index(encrypted2[0]) * len(symbols) + symbols.index(encrypted2[1])
                        roots = solver(x1 - x2, y1 - y2, mod)
                        if roots:
                            for a in roots:
                                b = (y1 - a * x1) % mod
                                decrypted = decrypt(text, (a, b), symbols)
                                # Перевірка на відсутність неправдоподібних біграм
                                if all(bigram not in decrypted for bigram in ['аь', 'еь', 'юы', 'яы', 'эы', 'юь', 'яь', 'оь', 'иь', 'ыь', 'уь', 'аы', 'эь', 'ць', 'хь', 'кь', 'оы', 'иы', 'ыы', 'уы', 'еы']):
                                    return decrypted, (a, b)
    return None, None

def main():
    symbols = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    freq_bigrams = ['ст', 'но', 'то', 'на', 'ен']
    top_v_enc_bigrams = ['жц', 'дэ', 'цэ', 'ыб', 'оц']

    with open('08.txt', 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', '')

    decrypted_text, key = find_key_and_decrypt(text, freq_bigrams, top_v_enc_bigrams, symbols)
    if decrypted_text:
        print("Розшифрований текст:", decrypted_text)
        print("Використаний ключ:", key)
    else:
        print("Не вдалося розшифрувати текст.")

if __name__ == "__main__":
    main()

