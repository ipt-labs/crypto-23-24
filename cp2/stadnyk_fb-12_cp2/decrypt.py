import matplotlib.pyplot as plt

def filter_text(text):
    russian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    filtered_text = ''.join(char.lower() for char in text if char.lower() in russian_alphabet)
    return filtered_text

def vigenere_encrypt(plain_text, key):
    encrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(plain_text):
        shift = ord(key[i % key_length]) - ord('а')
        encrypted_char = chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
        encrypted_text += encrypted_char
    return encrypted_text

def calculate_index_of_coincidence(text):
    n = len(text)
    frequencies = [text.count(letter) for letter in set(text)]
    index_of_coincidence = sum((f * (f - 1) for f in frequencies)) / (n * (n - 1))
    return index_of_coincidence

def calculate_average_index_of_coincidence(text, key_length):
    subtexts = ['' for _ in range(key_length)]
    for i, char in enumerate(text):
        subtexts[i % key_length] += char

    average_index = sum(calculate_index_of_coincidence(subtext) for subtext in subtexts) / key_length
    return average_index

with open('vr12.txt', 'r', encoding='utf-8') as file:
    encrypted_text = file.read()

filtered_text = filter_text(encrypted_text)

key_lengths = list(range(2, 31))
average_indices = [calculate_average_index_of_coincidence(filtered_text, length) for length in key_lengths]

plt.plot(key_lengths, average_indices, marker='o')
plt.xlabel('Key Length')
plt.ylabel('Average Index of Coincidence')
plt.title('Vigenere Cipher: Key Length Analysis')
plt.grid(True)
plt.show()

def filter_text(text):
    russian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    filtered_text = ''.join(char.lower() for char in text if char.lower() in russian_alphabet)
    return filtered_text

def vigenere_decrypt(ciphertext, key):
    decrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        shift = ord(key[i % key_length]) - ord('а')
        decrypted_char = chr((ord(char) - ord('а') - shift) % 32 + ord('а'))
        decrypted_text += decrypted_char
    return decrypted_text

def find_most_frequent_letter(text):
    frequencies = {char: text.count(char) for char in set(text)}
    most_frequent_letter = max(frequencies, key=frequencies.get)
    return most_frequent_letter

def find_key_letter(text, language_letter):
    most_frequent_text_letter = find_most_frequent_letter(text)
    shift = (ord(most_frequent_text_letter) - ord(language_letter)) % 32
    return chr(ord('а') + shift)

with open('vr12.txt', 'r', encoding='utf-8') as file:
    encrypted_text = file.read()

filtered_text = filter_text(encrypted_text)

key_length = 14
subtexts = ['' for _ in range(key_length)]
for i, char in enumerate(filtered_text):
    subtexts[i % key_length] += char

auto_generated_key = ''
for subtext in subtexts:
    key_letter = find_key_letter(subtext, 'о')
    auto_generated_key += key_letter

decrypted_text = vigenere_decrypt(filtered_text, auto_generated_key)

print(f"Auto-generated Key: {auto_generated_key}")

user_key = input("Введіть свій ключ для розшифрування: ")

decrypted_text_user_key = vigenere_decrypt(filtered_text, user_key)

print(f"Decrypted Text (User Key): {decrypted_text_user_key}")







