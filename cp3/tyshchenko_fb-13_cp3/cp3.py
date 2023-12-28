#!/bin/python3

from collections import Counter
import sys

ALPHABET = "абвгдежзийклмнопрстуфхцчшщыьэюя"
M = len(ALPHABET)
FREQ_L = "оеа"
RARE_L = "щэф"
BIGRAMS = ["ст", "но", "то", "на", "ен"]

# Calculate gcd(a, b).
def euclid(a: int, b: int) -> list:
    # Make positive.
    a, b = abs(a), abs(b)
    # Initialize base values.
    u = [1, 0]
    v = [0, 1]
    a0, b0 = a, b
    # Swap values if necessary.
    if a > b:
        a, b = b, a
        u, v = v, u
        a0, b0 = b, a
    r = a % b
    q = [a // b]
    # Find gcd(a, b) and inverses.
    while a % b:
        a = b
        b = r
        r = a % b
        u.append(u[-2] - q[-1] * u[-1])
        v.append(v[-2] - q[-1] * v[-1])
        q.append(a // b)
    if u[-1] < 0:
        u[-1] += b0
    if v[-1] < 0:
        v[-1] += a0
    # Return [gcd(a, b), a^(-1), b^(-1)].
    return [b, u[-1], v[-1]]

# Solve a * x = b mod n.
def lin_cmp(a: int, b: int, n: int):
    lst = euclid(n, a)
    # Case gcd(a, n) == 1.
    if lst[0] == 1:
        return [(lst[2] * b) % n]
    # Case gcd(a, n) = d > 1 and b % d != 0.
    if b % lst[0] != 0:
        return [-1]
    # Case gcd(a, n) = d > 1 and b % d == 0. 
    else:
        a //= lst[0]
        b //= lst[0]
        n //= lst[0]
        x = (euclid(n, a)[2] * b) % n
        return [x + i * n for i in range(lst[0])]

# Count bigrams of a text.
def count_bigrams(text: str, overlap=False) -> dict:
    text_len = len(text)
    # Set step for text traversing.
    step = overlap + 1
    bigrams = [text[s:s + 2] for s in range(0, text_len - 1, step)]
    # Return bigrams sorted by their count.
    return dict(sorted(Counter(bigrams).items(), reverse=True, key=lambda item: item[1]))

# Encode letter or bigram.
def encode(ngram: str) -> int:
    if len(ngram) == 1:
        return ALPHABET.index(ngram)
    else:
        return ALPHABET.index(ngram[0]) * M + ALPHABET.index(ngram[1])

# Decode letter or bigram.
def decode(code) -> str:
    # Actual decoding function.
    def get_str(c: int) -> str: 
        if c < M:
            return ALPHABET[c]
        else:
            first = c // M
            second = c % M
            return f"{ALPHABET[first]}{ALPHABET[second]}"
            
    if isinstance(code, list):
        return ''.join([get_str(x) for x in code])
    else:
        return get_str(code)
    
# Decrypt ciphered text.
def decrypt(ct: str, key: tuple) -> str:
    pt = ''
    for i in range(0, len(ct), 2):
        pt = pt + decode(lin_cmp(key[0], encode(ct[i:i+2]) - key[1], M ** 2))
    return pt

# Find candidates for keys.
def find_keys(ct: str) -> list:
    keys = []
    ct_bigrams = list(count_bigrams(ct))
    # Loop through every possible combination of X*, X**, Y*, Y**.
    for i in ct_bigrams[:5]:
        for j in ct_bigrams[:5]:
            for k in BIGRAMS:
                for l in BIGRAMS:
                    if i != j and k != l:
                        a = lin_cmp(encode(k) - encode(l), encode(i) - encode(j), M ** 2)
                        for n in a:
                            # Skip found keys and equations without solutions.
                            if n in [k[0] for k in keys] or n == -1:
                                continue
                            b = (encode(i) - n * encode(k)) % M ** 2
                            keys.append((n, b))
    return keys

# Check if text is sensible.
def sensible(text: str) -> int:
    score = 0
    # Count letters of text and store them by values in descending order.
    letters = list(dict(sorted(Counter(text).items(), reverse=True, key=lambda item: item[1])))
    # Check the most frequent letters.
    for l in letters[:3]:
    	if l in FREQ_L:
            score += 1
    # Check the least frequent letters.
    for l in letters[-3:]:
    	if l in RARE_L:
            score += 1
    # Check the most frequent bigrams.
    bigrams = list(count_bigrams(text, overlap=True))[:5]
    for b in range(5):
        if bigrams[b] in BIGRAMS:
            score += 1
    return score 

def tests(f1: str, f2: str):
    # Find inverse.
    print(euclid(155, 29))
    print(euclid(2, -5))
    print(euclid(-15, 40))
    # Solve linear comparison (case 1).
    print(lin_cmp(7, 19, 41))
    # Solve linear comparison (case 3).
    print(lin_cmp(39, 30, 111))
    # Count bigrams of "hello world!" without and with overlap.
    print(count_bigrams("hello world! hello mum"))
    print(count_bigrams("hello world! hello mum", overlap=True))
    # Encode and decode bigram.
    print(f"{decode(63)} ({encode('вб')})")
    # Check sensibility of text.
    data = open(f1, 'r').read().strip()
    print(f"sensible: score = {sensible(data)}")
    data = open(f2, 'r').read().strip()
    print(f"nonsensible: score = {sensible(data)}")
    # Find canditates for keys.
    candidates = find_keys(data)
    keys = []
    for k in candidates:
        if sensible(decrypt(data, k)) > 4:
            keys.append(k)
    print(keys)
    for k in keys:
        print(f"key = {k}\n{decrypt(data, k)}\n\n")
        
def solve(f: str) -> None:
    # Read input file.
    data = open(f, 'r').read().strip()
    # Show 5 most common bigrams of CT.
    ct_bigrams = list(count_bigrams(data))[:5]
    print(f"The most common bigrams of CT:\n\t{ct_bigrams}")
    # Find canditates for keys.
    candidates = find_keys(data)
    keys = []
    for k in candidates:
        pt = decrypt(data, k)
        if sensible(pt) > 5:
            keys.append(k)
    # Show found keys.
    print(f"Found keys (a, b):\n\t{keys}")
    for k in keys:
        print(f"Decrypted with key {k}:\n{decrypt(data, k)}\n\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"""USAGE: {sys.argv[0]} VAR3FILE
[*] VAR3FILE\t- path to var3 text file.""")
    else:
        f = sys.argv[1]
        solve(f)

