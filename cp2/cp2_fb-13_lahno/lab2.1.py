def opening(filename):
    with open(filename, 'r', encoding='utf8') as file:
        text = file.read()
    return text


def vigenere_encryption(text, key):
    alphabet = "абвгдежзийклмнопрстуфхцчшщыьэюя"
    encrypted_text = ''
    key_len = len(key)

    for i in range(len(text)):
        char_index = alphabet.index(text[i])
        key_char = key[i % key_len]
        key_char_index = alphabet.index(key_char)
        encrypted_char_index = (char_index + key_char_index) % len(alphabet)
        encrypted_text += alphabet[encrypted_char_index]

    return encrypted_text


def conformity_index(text):
    text_len = len(text)
    counter = {}
    sum_of_chars = 0

    for char in text:
        if char in counter:
            counter[char] += 1
        else:
             counter[char] = 1

    for count in counter.values():
        sum_of_chars += count*(count-1)
    con_index = sum_of_chars/(text_len*(text_len - 1))

    return con_index


input_text = opening(input("Input file: "))
output_file = input("Output file: ")
key = input("Key: ")

encrypted_text = vigenere_encryption(input_text, key)

with open(output_file, 'w', encoding='utf8') as file:
    file.write(encrypted_text)
print("Conformity index of plain text: ", conformity_index(input_text))
print(f"Conformity index of encrypted text with keylenght of {len(key)} : ", conformity_index(encrypted_text))
