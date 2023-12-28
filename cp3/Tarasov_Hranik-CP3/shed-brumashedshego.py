from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
BIGRAMS = ["ст", "но", "то", "на", "ен"]
M = len(ALPHABET)
IMPOSSIBLE_BIGRAMS_BIGRAMS = ['аы', 'аь', 'бй', 'бф', 'вй', 'гй', 'гф', 'гщ', 'гы', 'гь', 'гэ', 'гю', 'дй']

def formatter(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower().replace('\n', '')
    return text

def count_top_bigrams(text, top_n=5):
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    bigram_counts = Counter(bigrams)
    return {b: round(bigram_counts[b] / len(bigrams), 10) for b in sorted(bigram_counts, key=bigram_counts.get, reverse=True)[:top_n]}

def bigram_indexator_to_numerical(bigrams):
    return [ALPHABET.index(b[0]) * M + ALPHABET.index(b[1]) for b in bigrams]

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def modular_inversion(a, m):
    g, x, _ = extended_gcd(a, m)
    return x % m if g == 1 else None

def solve_equation(x1, y1, x2, y2):
    inverted_element = modular_inversion(x1 - x2, M**2)
    if inverted_element:
        a = (inverted_element * (y1 - y2)) % M**2
        b = (y1 - a * x1) % M**2
        return a, b

def bigram_indexator_to_alphabetical(num):
    return ALPHABET[num // M] + ALPHABET[num % M]

def analyzer(plaintext):
    return all(bigram not in plaintext for bigram in IMPOSSIBLE_BIGRAMS_BIGRAMS)

def affine_decrypt(ciphertext, keys):
    for a, b in keys:
        result = ''
        for i in range(0, len(ciphertext) - 1, 2):
            n = bigram_indexator_to_numerical([ciphertext[i:i+2]])[0]
            inverted_element = modular_inversion(a, M**2)
            if inverted_element is not None:
                result += bigram_indexator_to_alphabetical((n - b) * inverted_element % M**2)
        if result and analyzer(result):
            print(f'Key ({a},{b}) gives a result:', result)

if __name__ == "__main__":
    text = formatter('/home/mhranik/kpi-labs/crypto-23-24/cp3/Tarasov_Hranik-CP3/07.txt')

    X = bigram_indexator_to_numerical(BIGRAMS)
    Y = bigram_indexator_to_numerical(list(count_top_bigrams(text).keys()))

    keys = set()
    for x1 in X:
        for y1 in Y:
            for x2 in X:
                for y2 in Y:
                    if x1 != x2 and y1 != y2:
                        result = solve_equation(x1, y1, x2, y2)
                        if result:
                            keys.add(result)

    affine_decrypt(text, keys)
