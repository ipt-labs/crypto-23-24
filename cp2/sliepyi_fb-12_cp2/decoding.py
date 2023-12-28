#get key+extend
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
#decrypt ciphered text
def decipherText(cipher_text, key):
    deciphered_text = []
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) - ord(key[i])) % 32
        x += ord('а')
        deciphered_text.append(chr(x))
    return "".join(deciphered_text)
#Here we go
if __name__ == "__main__":
    input_file = "variant.txt"  
    output_file = "variant.decrypted.txt"  
    with open(input_file, 'r', encoding='utf-8') as file:
        cipher_text = file.read()
    key = generateKey(cipher_text, "")  
    decrypted_text = decipherText(cipher_text, key)
    with open(output_file, "w", encoding='utf-8') as file:
        file.write(decrypted_text)
    print("Decrypted message has been saved to 'vig.decrypted.txt'")
