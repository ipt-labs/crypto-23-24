def vigenere_decrypt(ciphertext, key):
    decrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_length].lower()) - ord('а')
            if char.islower():
                decrypted_char = chr(((ord(char) - ord('а') - shift) % 32) + ord('а'))
            else:
                decrypted_char = chr(((ord(char) - ord('А') - shift) % 32) + ord('А'))
        else:
            decrypted_char = char
        decrypted_text += decrypted_char
    return decrypted_text

# Зчитуємо шифртекст з файлу
file_path = "C:\\Users\\Polya\\Desktop\\KPI\\crypto\\crypto-23-24\\cp2\\gogoleva_fb-12_cp2\\decode.txt"
with open(file_path, "r", encoding="cp1251") as file:
    ciphertext = file.read()

# Ключ для розшифрування
key = "делолисоборотней"

# Розшифровуємо текст
decrypted_text = vigenere_decrypt(ciphertext, key)

# Виводимо розшифрований текст
print(decrypted_text)
