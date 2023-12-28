from itertools import product

m = 31
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'

with open("09.txt", "r", encoding="utf-8") as file:
    ciphertext = file.read()

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def inverted(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m

def solve_equation(a, b, m):
    g = egcd(a, m)[0]
    if b % g != 0:
        return None
    else:
        a = a // g
        b = b // g
        m = m // g
        return (inverted(a, m) * b) % m

def top_bigrams(ciphertext):
    amount = {}
    total = len(ciphertext) - 1

    for i in range(0, total, 2):
        bigram = ciphertext[i:i+2]
        amount[bigram] = amount.get(bigram, 0) + 1

    sorted_bigrams = sorted(amount.items(), key=lambda x: x[1], reverse=True)

    top_bigrams_list = [bigram for bigram, amount in sorted_bigrams[:5]]
    print('Топ 5 біграм за частотами:')
    for bigram, amount in sorted_bigrams[:5]:
        freq = amount / total
        print(f'Біграма: {bigram}, частота: {freq:.5f}')

    return top_bigrams_list

bigrams = ['ст', 'но', 'то', 'на', 'ен'] + top_bigrams(ciphertext)

def alphabet_idx(letter):
    return alphabet.index(letter)

def x_count(pair, m):
    letter1, letter2 = pair[0], pair[1]
    index1, index2 = alphabet_idx(letter1), alphabet_idx(letter2)
    return index1 * m + index2

def txt_to_num(bigrams):
    results = []
    for pair in bigrams:
        x = x_count(pair, m)
        results.append(x)
    return results

output = txt_to_num(bigrams)
print()
print('Біграми в числовому значенні:')
for i in range(0, len(bigrams), 5):
    input_str = ', '.join(bigrams[i:i + 5])
    output_str = ', '.join(map(str, output[i:i + 5]))
    print(f"{input_str} : {output_str}.")

def decrypt_text(ciphertext, a, b):
    decrypted_text = ""
    for i in range(0, len(ciphertext), 2):
        bigram = ciphertext[i:i + 2]
        Y = x_count(bigram, m)
        a_inv = inverted(a, m ** 2)

        if a_inv is None:
            continue

        X = (a_inv * (Y - b)) % (m ** 2)
        letter1 = alphabet[X // m]
        letter2 = alphabet[X % m]
        decrypted_text += letter1 + letter2
    return decrypted_text

X, Y = output[:len(output)//2], output[len(output)//2:]

def find_keys(X1, Y1, X2, Y2, m):
    a = solve_equation(X1 - X2, Y1 - Y2, m ** 2)
    if a is None:
        return None, None
    b = solve_equation(1, Y1 - a * X1, m ** 2) % (m ** 2)

    if a < 0:
        a += m ** 2
    if b < 0:
        b += m ** 2

    return a, b

def combinations(X, Y):
    all_combs = list(product(X, Y, repeat=2))
    return all_combs

combs = combinations(X, Y)
unique_keys = set()

forbidden_bigrams = \
    ['аь', 'бй', 'бф', 'гщ', 'еь', 'жй', 'жц', 'жщ', 'жы', 'уь', 'фщ', 'хы', 'хь', 'цщ', 'цю', 'чф','чц',
    'чщ', 'чы', 'чю', 'шщ', 'шы', 'шю', 'щг', 'щж', 'щл', 'щх', 'щц', 'щч', 'щш', 'щы', 'щю','щя', 'ыь',
    'ьы', 'эа', 'эж', 'эи', 'эо', 'эу', 'эщ', 'эы', "эь", 'эю', 'эя', 'юы', 'юь', 'яы','яь', 'ьь']

def check_result(text):
    for bigram in forbidden_bigrams:
        if bigram in text:
            print(f"Forbidden: {bigram}")
            return False
    return True

print()
print('Розшифрування тексту ключами:')
for combination in combs:
    a, b = find_keys(*combination, m)
    if a is not None and (a, b) not in unique_keys:
        print(f"Key: {a} {b}")
        decrypted_text = decrypt_text(ciphertext, a, b)
        if not decrypted_text:
            print("Empty")
        else:
            if check_result(decrypted_text):
                print("Decrypted text:")
                print(decrypted_text)
                with open('decrypted_text.txt', 'w', encoding="utf-8") as file:
                    file.write(decrypted_text)
        unique_keys.add((a, b))