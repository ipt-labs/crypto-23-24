from collections import Counter
from itertools import product
abc = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
         'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

file = open('14.txt', 'r', encoding="UTF-8")
text = file.read().lower().replace("\n", "")

probabilities_of_bigram2={}
def bigram_2_frequencies(text):
    bigrams = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    number_of_each_bigram = Counter(bigrams)
    total_number_of_bigrams = len(bigrams)
    for bigram, k in number_of_each_bigram.items():
        probabilities_of_bigram2[bigram] = k / total_number_of_bigrams
    return probabilities_of_bigram2

bigram_2_frequencies(text)

bigram_encrypted_text = sorted(probabilities_of_bigram2.items(), key=lambda item: item[1])
for bigram, probability in bigram_encrypted_text[-5:]:
    print(f"{bigram}: {probability}")

popular_bigrams_chipher_text = ["аж", "цп", "шы", "ки", "тя"]
popular_bigrams = ["ст", "но", "то", "на", "ен"]


def bigram_as_number(bigram):
    return [(abc.index(i[0]) * 31 + abc.index(i[1])) for i in bigram]


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        inverted = y - (b // a) * x
        return g, inverted, x


def solve_linear_congruence(a, b, n, d):
    if b % d == 0:
        gcd, inverted, y = extended_gcd(a // d, n // d)
        x0 = (inverted * (b // d)) % (n // d)

        solutions = [(x0 + i * (n // d)) % n for i in range(d)]
        return solutions
    else:
        return False


def find_keys(X, Y):
    keys = []
    for x1, y1 in product(X, Y):
        for x2, y2 in product(X, Y):
            if x1 == x2 or y1 == y2:
                continue

            gcd, x, y = extended_gcd(x1-x2, 31**2)
            if gcd == 1:
                a = ((y1-y2)*x) % 31**2
                b = (y1 - a*x1) % 31**2
                keys.append((a, b))
            elif gcd > 1:
                result = solve_linear_congruence((x1-x2), (y1-y2), 31**2, gcd)
                if result and a in result:
                    b = (y1 - a * x1) % 31 ** 2
                    keys.append((a, b))
    print(keys)
    return keys


def decrypt(text, key):
    result = ""
    gcd, a, y = extended_gcd(key[0], 31 ** 2)

    for i in range(0, len(text)-1, 2):
        bigram = text[i:i+2]
        bigram_number = bigram_as_number([bigram])[0]
        # Розшифрування кожної біграми
        # Розрахунок x за формулою розшифрування
        x = (a * (bigram_number - key[1])) % (31 ** 2)
        # Розрахунок індексів символів за числовим представленням
        x_i1, x_i2 = divmod(x, 31)

        result += abc[x_i1] + abc[x_i2]

    return result

print("\nMost frequent bigrams in russian language:")
print(popular_bigrams)
print(bigram_as_number(popular_bigrams))

print("\nMost frequent bigrams in ciphertext:")
print(popular_bigrams_chipher_text)
print(bigram_as_number(popular_bigrams_chipher_text))

print("\nAll possible keys:")
keys = find_keys(bigram_as_number(popular_bigrams), bigram_as_number(popular_bigrams_chipher_text))

def match_index(text):
    total_chars = len(text)
    frequencies = {}
    for char in text:
        if char.isalpha():
            char = char.lower()
            if char in frequencies:
                frequencies[char] += 1
            else:
                frequencies[char] = 1
    index_of_coincidence = sum(freq*(freq-1) for freq in frequencies.values()) / (total_chars*(total_chars-1))
    return index_of_coincidence

for key in keys:
    decrypted_text = decrypt(text, key)
    index = match_index(decrypted_text)
    if 0.05 < index < 0.06:
        best_key = key

decrypted_text = decrypt(text, best_key)
print(f"\nKey: {best_key}")
print(f"Decrypted Text: {decrypted_text}")




