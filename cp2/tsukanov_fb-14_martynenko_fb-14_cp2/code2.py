def vigenere_cipher(text, key):
    alphabet = 'абвгдеєжзийклмнопрстуфхцчшщґіьїюя'
    key_length = len(key)

    encrypted_text = []

    for i in range(len(text)):
        if text[i] in alphabet:
            text_letter_index = alphabet.index(text[i])
            key_letter_index = alphabet.index(key[i % key_length])

            encrypted_letter_index = (text_letter_index + key_letter_index) % 33
            encrypted_letter = alphabet[encrypted_letter_index]

            encrypted_text.append(encrypted_letter)
        else:
            encrypted_text.append(text[i])

    return ''.join(encrypted_text)
with open("my_text.txt", "r", encoding="utf-8") as f:
    plain_text = f.read()
keys = ["ок", "жах", "кров", "петля", "хелоуін","васильсимоненко"]

def calculate_index_of_coincidence(text):
    frequencies={}    
    for char in text:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1

    ic_value = sum([(count * (count - 1)) for count in frequencies.values()]) / (len(text) * (len(text) - 1))

    return ic_value

print(plain_text)
print(f"Індекс відповідності: {calculate_index_of_coincidence(plain_text)}\n")

for key in keys:
    encrypted_text = vigenere_cipher(plain_text, key)
    print(f"Зашифрований текст, key = {key}, r = {len(key)}: {encrypted_text}")
    print(f"Індекс відповідності: {calculate_index_of_coincidence(encrypted_text)}\n")
    