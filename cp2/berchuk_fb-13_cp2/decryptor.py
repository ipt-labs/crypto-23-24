def decrypt(text, key):
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    decrypted = []
    key_len = len(key)

    for i, char in enumerate(text):
        char_index = alphabet.index(char)
        key_char_index = alphabet.index(key[i % key_len])
        decrypted_idx = (char_index - key_char_index) % len(alphabet)
        decrypted_char = alphabet[decrypted_idx]
        decrypted.append(decrypted_char)

    return "".join(decrypted)


with open("9var.txt", "r", encoding="utf-8") as f:
    text = f.read()

key = "войнамагаэндшпиль"
decrypted = decrypt(text, key)

with open("decrypted_9var.txt", "w", encoding="utf-8") as f:
    f.write(decrypted)