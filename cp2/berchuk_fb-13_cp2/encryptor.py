def encrypt(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            key_char = key[i % len(key)]
            shift = ord(key_char.lower()) - ord('а')
            if char.isupper():
                encrypted_char = chr(((ord(char) - ord('А') + shift) % 32) + ord('А'))
            else:
                encrypted_char = chr(((ord(char) - ord('а') + shift) % 32) + ord('а'))
            encrypted_text += encrypted_char
    return encrypted_text


def calculate_idx(text):
    n = len(text)
    sum = 0
    for char in set(text):
        encoded_text_count = text.count(char)
        sum += (encoded_text_count * (encoded_text_count - 1))
    result = (1 / (n * (n - 1))) * sum
    return result


with open("text.txt", "r", encoding="utf-8") as file:
    original_text = file.read()

keys = {
    2: "шо",
    3: "бар",
    4: "лаба",
    5: "грива",
    10: "валентинка",
    11: "затрушенный",
    12: "колючкозубый",
    13: "макродинамика",
    14: "авиапереброска",
    15: "дезинтоксикация",
    16: "высокодисперсный",
    17: "ребристотрубчатый",
    18: "катапультироваться",
    19: "абонементодержатель",
    20: "нефтегазопереработка"
}

with open("results.txt", "w", encoding="utf-8") as results_file:
    results_file.write("Індекс для нешифрованого тексту:\n")
    original_index = calculate_idx(original_text)
    results_file.write(f"{original_index:.6f}\n\n")

    for key_length, key in keys.items():
        encrypted_text = encrypt(original_text, key)
        index_of_coincidence = calculate_idx(encrypted_text)

        results_file.write(f"Ключ {key_length}: '{key}'\n")
        results_file.write("Шифртекст:\n")
        results_file.write(f"{encrypted_text}\n")
        results_file.write("Індекс відповідності = {:.6f}\n\n".format(index_of_coincidence))