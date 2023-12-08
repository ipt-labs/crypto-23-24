from collections import Counter

ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
BIGRAMS = ["ст", "но", "то", "на", "ен"]
M = len(ALPHABET)
not_existing_bigrams = ['аы', 'аь', 'бй', 'бф', 'вй', 'гй', 'гф', 'гщ', 'гы', 'гь', 'гэ', 'гю', 'дй']

def read_file(t):
    with open(t, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def filter_text(t):
    text = read_file(t).lower()
    return text.replace('\n', '')

def count_bigrams(text):

    # Create bigrams with overlapping characters
    bigram = [text[i:i + 2] for i in range(len(text))]
    count_b = Counter(bigram)

    # Calculate bigram frequencies
    freq_b = {i: round(count_b[i] / len(bigram), 10) for i in count_b}
    return dict(sorted(freq_b.items(), key=lambda item: item[1], reverse=True)[:5])

def bigram_to_number(bigrams):
    b_nums = []
    for b in bigrams:
        b_nums.append(ALPHABET.index(b[0])*M+ALPHABET.index(b[1]))
    return b_nums

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def invert(a, m):
    g, x, _ = extended_gcd(a, m)

    if g == 1:
        return x % m

def solve_eq(x1, y1, x2, y2):

    if invert(x1-x2, M**2):
        a = (invert(x1-x2, M**2)*(y1-y2)) % M**2
        b = (y1-a*x1) % M**2
        return [a, b]
    print (a, b)

def number_to_bigram(num):
    _2 = num % M
    _1 = int((num - _2) / M)
    return ALPHABET[_1] + ALPHABET[_2]

def meaningful(plaintext):
    for i in not_existing_bigrams:
        if i in plaintext:
            return False
    return True


def decrypt(text, keys):

    for key in keys:
        a = key[0]
        b = key[1]
        plaintext = ''
        for y in range(0, len(text) - 1, 2):
            n = ALPHABET.index(text[y:y+2][0]) * M + ALPHABET.index(text[y:y+2][1])
            if invert(a, M**2) != None:
                plaintext += number_to_bigram((n - b) * invert(a, M**2) % M**2)

        #test
        if plaintext and meaningful(plaintext):
            print(f'Для ключа ({a},{b}):', plaintext)

if __name__ == "__main__":
    text = filter_text('05.txt')

    X = bigram_to_number(BIGRAMS)
    Y = bigram_to_number(count_bigrams(text).keys())

    combinations = []
    keys = []
    for x1 in X:
        for y1 in Y:
            for x2 in list(filter(lambda x: x != x1, X)):
                for y2 in list(filter(lambda y: y != y1, Y)):
                    result = solve_eq(x1, y1, x2, y2)
                    if result:
                        keys.append(result)
    keys_unique = []
    [keys_unique.append(x) for x in keys if x not in keys_unique]
    decrypt(text, keys_unique)
