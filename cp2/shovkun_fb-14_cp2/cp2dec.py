import matplotlib.pyplot as plt
from collections import Counter

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

with open('encrypted_text.txt', 'r', encoding='utf-8') as file:
    text = file.read().lower()

def filter_text(text):
    punctuation = '!"#$%&\'()*+,-./:;<=>?»–«@[\\]^_`{|}~ \n'
    return ''.join(char for char in text if char not in punctuation)

def decrypt(encrypted_text, key):
    decrypted_text = ""
    key_len = len(key)
    mod = len(alphabet)

    for i in range(len(encrypted_text)):
        char = encrypted_text[i]
        if char in alphabet:
            key_index = i % key_len
            key_char = key[key_index]
            shift = alphabet.index(key_char)
            new_char_code = (alphabet.index(char) - shift) % mod
            decrypted_char = alphabet[new_char_code]
            decrypted_text += decrypted_char
        else:
            decrypted_text += char

    return decrypted_text

def to_blocks(text, r):
    return [text[i::r] for i in range(r)]

def calculate_index(text, r):
    blocks = to_blocks(text, r)
    index = 0.0

    for block in blocks:
        freqs = Counter(block)
        total_pairs = sum(f*(f-1) for f in freqs.values())
        index += total_pairs / (len(block) * (len(block) - 1))

    return index / r

def freq_count(text):
    freqs = Counter(text)
    most_freq = max(freqs, key=freqs.get)
    return most_freq

def find_key(text, r):
    russian_letter_o = 14
    mod = len(alphabet)
    blocks = to_blocks(text, r)
    key = ''.join([alphabet[((alphabet.index(freq_count(i)) - russian_letter_o) % mod)] for i in blocks])
    print(f'possible key: {key}')
    return key

filtered_text = filter_text(text)

indexes = []
r_values = list(range(2, 33))

for i in r_values:
    ic = calculate_index(filtered_text, i)
    indexes.append(ic)

plt.bar(r_values, indexes)
plt.xlabel('r')
plt.ylabel('Index')
plt.title('Index for different r values')
plt.show()

find_key(filtered_text, r=int(input('Value for r = ')))

decrypted_text = decrypt(filtered_text, key=input('Your key: '))
print(decrypted_text)

with open('decrypted_text.txt', 'w', encoding='utf-8') as file:
    file.write(decrypted_text)