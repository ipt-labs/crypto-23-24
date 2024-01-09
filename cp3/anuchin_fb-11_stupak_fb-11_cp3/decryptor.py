import itertools

alletters = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й',
             'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
             'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'э', 'ю', 'я']

def modinv(a, m):
    g, x, _ = extended_gcd(a, m)
    if g == 1:
        return x % m
    raise Exception('Modular inverse does not exist')

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

def decrypt_affine(ciphertext, a, b, m):
    plaintext = ""
    a_inv = modinv(a, m**2)
    for i in range(0, len(ciphertext), 2):
        x = (alletters.index(ciphertext[i]) * m) + alletters.index(ciphertext[i+1])
        x = (a_inv * (x - b)) % (m**2)
        plaintext += alletters[x // m] + alletters[x % m]
    return plaintext

with open("16.txt", "r", encoding="utf-8") as file:
    encrypted_text = file.read().replace('\n', '')

with open("filtered.txt", "r", encoding="utf-8") as file:
    keys_content = file.read()

keys = []
for line in keys_content.splitlines():
    parts = line.split(' ')
    if len(parts) == 2:
        a = int(parts[0].split('=')[1].strip('[]'))
        b = int(parts[1].split('=')[1].strip('[]'))
        keys.append((a, b))

def letter_frequency(text):
    freq = {}
    for letter in text:
        if letter in alletters:
            freq[letter] = freq.get(letter, 0) + 1
    total = sum(freq.values())
    return {k: v / total for k, v in freq.items()}

def is_meaningful(text):
    common_words = ["не", "на", "я", "что", "тот", "быть", 'за', 'время' "весь"]
    return any(word in text for word in common_words)

expected_freq = {'о': 0.09, 'е': 0.08, 'а': 0.08, 'и': 0.07, 'н': 0.06, 'т': 0.06, 'с': 0.05, 'р': 0.05, 'в': 0.05}

def check_frequency(text, tolerance=0.03):
    freq = letter_frequency(text)
    for letter, exp_freq in expected_freq.items():
        if abs(freq.get(letter, 0) - exp_freq) > tolerance:
            return False
    return True

for key in keys:
    try:
        decrypted_text = decrypt_affine(encrypted_text, key[0], key[1], 31)
        if check_frequency(decrypted_text) and is_meaningful(decrypted_text):
            print(f"Key={key}, Decrypted text: {decrypted_text[:100]}")
    except Exception as e:
        continue




