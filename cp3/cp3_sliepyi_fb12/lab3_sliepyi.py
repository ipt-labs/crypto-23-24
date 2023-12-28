# Define the alphabet and its corresponding numeric values
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
alphabet_nums={'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ж': 6, 'з': 7, 'и': 8, 'й': 9, 'к': 10, 'л': 11, 'м': 12, 'н': 13, 'о': 14, 'п': 15, 
          'р': 16, 'с': 17, 'т': 18, 'у': 19, 'ф': 20, 'х': 21, 'ц': 22, 'ч': 23, 'ш': 24, 'щ': 25, 'ь': 26, 'ы': 27, 'э': 28, 'ю': 29, 'я': 30}

# Define frequently occurring bigrams and banned bigrams
bigrams = ['то', 'но', 'на', 'не', 'ст']
banned_bigrams = ['аь', 'еь', 'иь', 'оь', 'уь', 'ыь', 'ьь', 'эь', 'юь', 'яь', 'аы', 'еы', 'ыы', 'иы', 'оы', 'уы', 'ыы', 'ьы', 'эы', 'юы', 'яы']

# Math functions code block
""" 
    Calculate the greatest common divisor of two numbers.
    Calculate the modular multiplicative inverse of a number.
    Solve a linear congruence equation ax ≡ b (mod m).
"""

def gcd_(a, b):
    if a == 0:
        return b, 0, 1
    gcd, v1, u1 = gcd_(b % a, a)
    u = u1 - (b // a) * v1
    v = v1
    return gcd, u, v

def inverse_element(a, m):
    gcd, x, y = gcd_(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def solve_linear_congruence(a, b, m):
    gcd, x, y = gcd_(a, m)
    if not b % gcd == 0:
        return []
    else:
        a = a // gcd
        b = b // gcd
        m = m // gcd
        x = b * inverse_element(a, m) % m
        solution = [(x + m * k) for k in range(gcd)]  
        return solution

# Bigram functions code block
""" 
    Count the frequency of bigrams in the given text.
    Convert a bigram to its corresponding numeric value.
"""
def calculate_bigram_frequency(input_text):
    bigram_freq_dict = {}
    bigrams = [input_text[i:i + 2] for i in range(0, len(input_text) - 1)]
    for bigram in bigrams:
        bigram_freq_dict[bigram] = bigram_freq_dict.get(bigram, 0) + 1
    total_bigrams = len(bigrams)
    bigram_freq_dict = {k: round(v / total_bigrams, 8) for k, v in bigram_freq_dict.items()}
    sorted_freq_dictionary = dict(sorted(bigram_freq_dict.items(), key=lambda item: item[1], reverse=True)[:5])
    return sorted_freq_dictionary

def bigram_to_number(bigram):
    x1 = alphabet_nums[bigram[0]]
    x2 = alphabet_nums[bigram[1]]
    X = x1 * 31 + x2
    return X

# Find key functions code block
""" 
    Find potential keys by comparing frequently occurring bigrams with the top bigrams in the given text
"""
def find_keys():
    potential_keys = []
    potential_bigram_comp = [(i, j) for i in bigrams for j in bigram_freq_top]
    for i in potential_bigram_comp:
        for j in potential_bigram_comp:
            if i == j:
                continue
            x1 = bigram_to_number(i[0])
            x2 = bigram_to_number(j[0])
            y1 = bigram_to_number(i[1])
            y2 = bigram_to_number(j[1])
            a_list = solve_linear_congruence(x1 - x2, y1 - y2, 31 ** 2)
            for _ in a_list:
                b_list = (y1 - _ * x1) % (31 ** 2)
                potential_keys.append((_, b_list))
    #print(len(set(potential_keys)))
    return set(potential_keys)

# Language check and decoding functions code block
""" 
    Check if the given text contains any banned bigrams.
    Decrypt the text using potential keys and check for banned bigrams.
"""

def banned_bigrams_check(text):
    for _ in banned_bigrams:
        if _ in text:
            return False
    return True

def decrypt_text(poten_keys):
    possible_keys = poten_keys
    for key in possible_keys:
        a = key[0]
        b = key[1]
        plaintext = ''
        if inverse_element(a, 31 ** 2) is None:
            continue
        for j in range(0, len(ciphertext) - 1, 2):
            Xi = (inverse_element(a, 31 ** 2) * (bigram_to_number(ciphertext[j:j + 2]) - b)) % (31 ** 2)
            plaintext += alphabet[Xi // 31] + alphabet[Xi % 31]
        if banned_bigrams_check(plaintext):
            with open('decrypted_text.txt', 'w', encoding='utf8') as decrypted_file:
                print(f'Key found K(a,b) = {a, b} and decoded text written to "decrypted_text.txt"')
                decrypted_file.write(plaintext)
        else:
            continue

# Main code block
"""
    Call all previously defined functions
"""
if __name__ == '__main__':
    with open('11.txt', 'r', encoding='utf8') as file_read:
        ciphertext = file_read.read()
        ciphertext = ciphertext.replace('\n', '')
    bigram_freq_top = calculate_bigram_frequency(ciphertext)
    print(bigram_freq_top)
    all_keys = find_keys()
    print(all_keys)
    decrypt_text(all_keys)