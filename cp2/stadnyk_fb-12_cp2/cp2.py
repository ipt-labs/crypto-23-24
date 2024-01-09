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

with open('text.txt', 'r', encoding='utf-8') as file:
    original_text = file.read()

filtered_text = filter_text(original_text)

keys = ['аб', 'вгд', 'ежз', 'ийкл', 'мнопрсту', 'фхцчшщъыьэюя']
encrypted_texts = []
for key in keys:
    encrypted_texts.append(vigenere_encrypt(filtered_text, key))

original_index = calculate_index_of_coincidence(filtered_text)
encrypted_indices = [calculate_index_of_coincidence(text) for text in encrypted_texts]

print(f"Original Text: {filtered_text}")
print(f"Original Index of Coincidence: {original_index}")
for i, key in enumerate(keys):
    print(f"Key {i + 1}: {key}, Encrypted Text: {encrypted_texts[i]}, Index of Coincidence: {encrypted_indices[i]}")

keys.append('Original')
indices = encrypted_indices + [original_index]

plt.bar(keys, indices)
plt.xlabel('')
plt.ylabel('Index of Coincidence')
plt.title('Index of Coincidence Comparison')
plt.show()
