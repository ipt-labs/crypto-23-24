from collections import Counter

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
mod = len(alphabet)
rus_bigram = ["ст", "но", "то", "на", "ен"]


def mod_inverse(a, m):
    def gcd_extended(a, m):
        if m == 0:
            return a, 1, 0
        else:
            gcd, x, y = gcd_extended(m, a % m)
            return gcd, y, x - (a // m) * y

    gcd, x, y = gcd_extended(a, m)
    if gcd != 1:
        return None
    else:
        return (x % m + m) % m


def calculate_bigram_and_frequency(text):
    bigrams_list = []
    i = 0
    while i < len(text) - 1:
        bigram = text[i:i+2]
        bigrams_list.append(bigram)
        i += 2

    bigram_frequency = Counter(bigrams_list)
    most_common_bigrams = [bigram for bigram, frequency in bigram_frequency.most_common(5)]
    print(f"text_bigrams = {most_common_bigrams}")
    return most_common_bigrams, bigrams_list


with open("10.txt", "r", encoding="utf-8") as file:
    text = file.read().replace('\n', '')
text_bigram, bigrams_list = calculate_bigram_and_frequency(text)


def bigrams_to_numbers(bigrams, alphabet):
    return [alphabet.index(bigram[0]) * len(alphabet) + alphabet.index(bigram[1]) for bigram in bigrams]


def find_keys():
    keys = []
    for bigram1 in rus_bigram:
        for bigram2 in text_bigram:
            for bigram3 in rus_bigram:
                for bigram4 in text_bigram:
                    if bigram1 != bigram3 and bigram2 != bigram4:
                        x1, y1 = bigrams_to_numbers([bigram1], alphabet)[0], bigrams_to_numbers([bigram2], alphabet)[0]
                        x2, y2 = bigrams_to_numbers([bigram3], alphabet)[0], bigrams_to_numbers([bigram4], alphabet)[0]
                        if mod_inverse(x1 - x2, mod**2):
                            a = (y1 - y2) * mod_inverse(x1 - x2, mod**2) % mod**2
                            b = (y1 - a * x1) % mod**2
                            keys.append((a, b))
    print(f'All keys: {keys}')
    return keys


def decode(keys, bigrams, alphabet):
    for key in keys:
        a_inv = mod_inverse(key[0], mod**2)
        if a_inv:
            b = key[1]
            decrypted_biagrams = [(bigram - b) * a_inv % mod**2 for bigram in bigrams]
            decrypted_text = "".join([alphabet[bigram // mod] + alphabet[bigram % mod] for bigram in decrypted_bigrams])
            if all(l_grams not in decrypted_text for l_grams in ['уь', 'юь', 'еь', 'эь', 'эы', 'фй', 'ьь', 'юы', 'оь', 'дй', 'яь']):
                print(f"Successful key: {key}")
                return decrypted_text, key
    return None, None


decrypted_text, successful_key = decode(find_keys(), bigrams_to_numbers(bigrams_list, alphabet), alphabet)

with open("10_decrypted.txt", "w", encoding="utf-8") as file:
    file.write(decrypted_text + "\n")
