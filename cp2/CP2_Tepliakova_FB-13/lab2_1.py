import re
import matplotlib.pyplot as plt

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"  # mod32
keys = ["да", "нет", "иглы", "взнос", "губернаторствовавший"]  # ключі довжини 2-5 і 20

input_file_path = "D:/python/crypta/task1.txt"
output_file_path = "D:/python/crypta/task1_edited.txt"

def edit_textfile(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    text = re.sub(r'[^a-zA-Zа-яА-Я\s\n]', ' ', text)
    text = text.lower()
    text = text.replace("ё", "е")
    text = text.replace("ъ", "ь")
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(' ', '')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)
    return text

edited_text = edit_textfile(input_file_path, output_file_path)

def encrypt_vigenere(plain_text, key):
    encrypted_text = ""
    key_length = len(key)

    for i in range(len(plain_text)):
        char = plain_text[i]
        key_char = key[i % key_length]
        move = ord(key_char) - ord('а')
        encrypted_char = chr((ord(char) + move - ord('а')) % 32 + ord('а'))
        encrypted_text += encrypted_char
    return encrypted_text

def calculate_index_of_coincidence(plain_text):
    total_characters = len(plain_text)
    total_frequencies = 0
    for character in alphabet:
        frequency = plain_text.count(character)
        total_frequencies += frequency*(frequency -1)
    index_of_coincidence = total_frequencies/(total_characters*(total_characters-1))
    return index_of_coincidence


def calculate_and_print_indices(original_text, encryption_keys):
    indices = {}
    for key in encryption_keys:
        encrypted_text = encrypt_vigenere(original_text, key)
        index = calculate_index_of_coincidence(encrypted_text)
        indices[key] = index
        print(f"Індекс відповідності для зашифрованих текстів (Key = '{key}'): {index}")
    return indices

def visualize_indices(indices):
    keys = list(indices.keys())
    values = list(indices.values())
    key_lengths = [len(key) for key in keys]

    plt.bar(key_lengths, values)
    plt.xlabel('Ключі')
    plt.ylabel('Індекс відповідності')
    plt.title('Індекси відповідності для ключів')
    plt.show()

index_original = calculate_index_of_coincidence(edited_text)
print(f"Індекс відповідності для відкритого тексту: {index_original}")
indices = calculate_and_print_indices(edited_text, keys)

visualize_indices(indices)

def write_encrypted_texts_to_file(encrypted_text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(encrypted_text))
encrypted_texts = []
for key in keys:
    encrypted_text = encrypt_vigenere(edited_text, key)
    encrypted_texts.append(encrypted_text)

output_file_path_all_keys = "D:/python/crypta/encrypted_text.txt"
write_encrypted_texts_to_file(encrypted_texts, output_file_path_all_keys)



