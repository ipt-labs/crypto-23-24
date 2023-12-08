def calculate_index_of_coincidence(text):
    text = ''.join(filter(str.isalpha, text))
    text = text.lower()

    n = len(text)
    letter_frequencies = {}

    for letter in text:
        if letter in letter_frequencies:
            letter_frequencies[letter] += 1
        else:
            letter_frequencies[letter] = 1

    index_of_coincidence = sum(f * (f - 1) for f in letter_frequencies.values()) / (n * (n - 1))

    return index_of_coincidence

def vigenere_cipher(plaintext, key):
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя" 
    encrypted_text = ""

    for i in range(len(plaintext)):
        plaintext_char = plaintext[i]
        if plaintext_char in alphabet:
            p = alphabet.index(plaintext_char)
            k = alphabet.index(key[i % len(key)])
            encrypted_char = alphabet[(p + k) % len(alphabet)]
            encrypted_text += encrypted_char
        else:
            encrypted_text += plaintext_char

    return encrypted_text

big_key = "унасоченьдлинныйключ"

file_path = r"C:\Users\Polya\Desktop\KPI\crypto\crypto-23-24\cp2\gogoleva_fb-12_cp2\cleaned.txt"

with open(file_path, "r", encoding="cp1251") as file:
    plaintext = file.read()

original_index = calculate_index_of_coincidence(plaintext)
print(f"Індекс відповідності для оригінального тексту: {original_index:.4f}")

key_lengths = [2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

for key_length in key_lengths:
    current_key = big_key[:key_length]
    encrypted_text = vigenere_cipher(plaintext, current_key)
    index = calculate_index_of_coincidence(encrypted_text)
    print(f"Індекс відповідності для шифру з ключем довжини {key_length}: {index:.4f}")
