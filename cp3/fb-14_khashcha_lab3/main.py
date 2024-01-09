import math

alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
modulus = 31 ** 2

def gcd_extended(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        gcd, x, y = gcd_extended(b, a % b)
        return (gcd, y, x - (a // b) * y)

def calculate_modular_inverse(element):
    if math.gcd(element, modulus) != 1:
        return None
    _, inverse, _ = gcd_extended(element, modulus)
    return inverse % modulus

def compute_congruence_solutions(coeff, constant):
    gcd_val, inverse, _ = gcd_extended(coeff, modulus)
    if constant % gcd_val != 0:
        return None

    solution_set = []
    base_solution = (inverse * (constant // gcd_val)) % modulus
    for i in range(gcd_val):
        solution_set.append((base_solution + i * (modulus // gcd_val)) % modulus)
    return solution_set

def get_frequent_bigrams(text, gap=1):
    bigrams = [text[i:i+2] for i in range(len(text)-gap)]
    bigram_freq = {b: bigrams.count(b) for b in set(bigrams)}
    return sorted(bigram_freq, key=bigram_freq.get, reverse=True)[:5]

def find_bigram_correspondences(common, observed):
    return [(c, o) for c in common for o in observed if c != o]

def extract_possible_keys(bigram_pairs):
    potential_keys = []
    for b1, b2 in bigram_pairs:
        x1, y1 = alphabet.index(b1[0]) * 31 + alphabet.index(b1[1]), alphabet.index(b2[0]) * 31 + alphabet.index(b2[1])
        solutions = compute_congruence_solutions(x1 - x1, y1 - y1)
        if solutions:
            for sol in solutions:
                potential_keys.append((sol, (y1 - sol * x1) % modulus))
    return potential_keys

def decrypt_cipher(cipher, key_pair):
    decrypted_text = ""
    inv_key = calculate_modular_inverse(key_pair[0])
    if inv_key is None:
        return None

    for i in range(0, len(cipher), 2):
        y = alphabet.index(cipher[i]) * 31 + alphabet.index(cipher[i + 1])
        x = (inv_key * (y - key_pair[1])) % modulus
        decrypted_text += alphabet[x // 31] + alphabet[x % 31]
    return decrypted_text

def try_decrypting(ciphered_text, keys):
    invalid_bigrams = {'аы', 'оы', 'иы', 'ыы', 'уы', 'еы', 'аь', 'оь', 'иь', 'ыь', 'уь', 'еь', 'юы', 'яы', 'эы', 'юь', 'яь', 'эь', 'ць', 'хь', 'кь', 'ьь', 'йй', 'йь', 'йы', 'ыю'}
    for key in keys:
        decrypted = decrypt_cipher(ciphered_text, key)
        if decrypted and not any(bg in decrypted for bg in invalid_bigrams):
            print(f'Decryption Key: {key}')
            with open("decrypted.txt", 'w', encoding='utf-8') as output_file:
                output_file.write(decrypted)
            break

with open('07.txt', 'r', encoding='utf-8') as file:
    cipher_text = file.read().replace('\n', '')

top_bigrams = ['ст', 'но', 'то', 'на', 'ен']
observed_top_bigrams = get_frequent_bigrams(cipher_text)
print(f'Top 5 bigrams in encrypted text: {observed_top_bigrams}')

matched_bigrams = find_bigram_correspondences(top_bigrams, observed_top_bigrams)
key_candidates = extract_possible_keys(matched_bigrams)
try_decrypting(cipher_text, key_candidates)
