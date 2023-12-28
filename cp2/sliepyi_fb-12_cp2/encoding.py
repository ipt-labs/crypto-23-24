#encoding
import re
#file processing
def process_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.lower()
    text = re.sub(r'[^а-яё]', '', text)
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)
#message reading
def read(output_file):
    with open(output_file, 'r', encoding='utf-8') as file:
        message = file.read()
    return message
#key generation(get+extend)
def generateKey(message, key):
    key_length = int(input("Enter key length (number of letters): "))
    key = input("Enter a keyword: ").lower()
    while len(key) != key_length or not all(char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' for char in key):
        print(f"Key length must be {key_length} characters.")
        key = input("Enter a keyword(in Russian): ").lower()
    print(f'Encrypting message using "{key}"-key')
    key = list(key)
    if len(message) == len(key):
        return key
    else:
        for i in range(len(message) - len(key)):
            key.append(key[i % len(key)])
    return "".join(key)
#encode message
def cipherText(message, key):
    cipher_text = []
    for i in range(len(message)):
        x = (ord(message[i]) + ord(key[i])) % 32
        x += ord('а')   
        cipher_text.append(chr(x))
    return "".join(cipher_text)
#Here we go
if __name__ == "__main__":
    input_file = "vig.input.txt"  # Замініть на ваш файл
    output_file = "vig.unencrypted.txt"  # Назва файлу для збереження результату
    process_text(input_file, output_file)
    message = read(output_file)
    key=''
    key = generateKey(message, key)
    encrypted_text = cipherText(message, key)
    with open("vig.encrypted.txt", "w", encoding='utf-8') as file:
        file.write(encrypted_text)
    print("Encrypted message has been saved to 'vig.encrypted.txt'")