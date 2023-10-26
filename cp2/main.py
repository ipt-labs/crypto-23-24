from re import sub

def prepare_key(message, key):
    key = key.lower()
    key = key * (len(message) // len(key)) + key[:len(message) % len(key)]
    return key

def vigenere_encrypt(text, key):
    text = text.lower()
    text = sub(r'\s+', ' ', text)
    key = prepare_key(text, key)
    encrypted_text = ""

    for i in range(len(text)):
        if text[i] == " ":
            encrypted_text += " "
        else:
            shift = ord(key[i]) - ord('А')
            encrypted_char = chr(((ord(text[i]) + shift - ord('А')) % 32) + ord('А'))
            encrypted_text += encrypted_char

    return encrypted_text

def main():
    input_file = "test.txt"
    output_file = "encrypted_test.txt"
    key = "да"  # Replace with your encryption key

    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()

    encrypted_text = vigenere_encrypt(text, key)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(encrypted_text)

    print(f"Text encrypted and saved to {output_file}")

def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key_length = len(key)
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():
            key_char = key[i % key_length]
            key_shift = ord(key_char) - ord('а')
            if char.isupper():
                decrypted_char = chr(((ord(char) - ord('А') - key_shift) % 32) + ord('А'))
            else:
                decrypted_char = chr(((ord(char) - ord('а') - key_shift) % 32) + ord('а'))
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)

# Function to read ciphertext and key from a file
def read_ciphertext_and_key(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    ciphertext = lines[0].strip()
    key = lines[65].strip()
    return ciphertext, key

# Specify the filename containing ciphertext and key
filename = "test2.txt"

# Read ciphertext and key from the file
ciphertext, key = read_ciphertext_and_key(filename)

# Decrypt the message
decrypted_message = vigenere_decrypt(ciphertext, key)

with open('decrypted_message.txt', "w", encoding="utf-8") as file:
    file.write(decrypted_message)

# Print the decrypted message
print("Decrypted message:", decrypted_message)




if __name__ == "__main__":
    main()

