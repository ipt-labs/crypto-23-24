import re
import matplotlib.pyplot as plt

def filter_text(text):
    # Замінюємо букву "ё" на "е"
    text = text.replace('ё', 'е')
    # Вилучаємо всі символи, окрім російських літер
    text = re.sub(r'[^а-яе]', '', text)
    # Замінюємо великі літери на маленькі
    text = text.lower()
    return text

# Зчитуємо вміст файлу text_1.txt (російськомовний текст)
with open('text_1.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Фільтруємо текст і видаляємо всі пробіли
filtered_text = filter_text(text).replace(' ', '')

# Зберігаємо очищений текст без пробілів у окремому файлі
with open('filtered_text.txt', 'w', encoding='utf-8') as filtered_file:
    filtered_file.write(filtered_text)

# Ключі різної довжини
keys = ["он", "нет", "кино", "земля", "методполиалфавитного"]

def vigenere_encrypt(text, key):
    encrypted_text = ""
    key_length = len(key)

    for i in range(len(text)):
        char = text[i]
        key_char = key[i % key_length]
        shift = ord(key_char) - ord('а')
        encrypted_char = chr(((ord(char) - ord('а') + shift) % 32) + ord('а'))
        encrypted_text += encrypted_char

    return encrypted_text

# Шифруємо текст ключами різної довжини
for key in keys:
    encrypted_text = vigenere_encrypt(filtered_text, key)
    with open(f'encrypted_text_{len(key)}.txt', 'w', encoding='utf-8') as file:
        file.write(encrypted_text)


def calculate_index_of_coincidence(text):
    text_length = len(text)
    letter_frequencies = {}
    
    for letter in text:
        if letter in letter_frequencies:
            letter_frequencies[letter] += 1
        else:
            letter_frequencies[letter] = 1
    
    index_of_coincidence = 0
    for letter in letter_frequencies:
        frequency = letter_frequencies[letter]
        index_of_coincidence += (frequency / text_length) * ((frequency - 1) / (text_length - 1))
    
    return index_of_coincidence

# Розрахунок індексу відповідності для очищеного тексту
index_open_text = calculate_index_of_coincidence(filtered_text)

# Розрахунок індексу відповідності для кожного з шифртекстів
print(f"Index of the opened text: {index_open_text}")
for key_num, key in enumerate(keys, start=1):
    with open(f'encrypted_text_{len(key)}.txt', 'r', encoding='utf-8') as file:
        encrypted_text = file.read()
    index_encrypted_text = calculate_index_of_coincidence(encrypted_text)
    print(f"Index of keys position {key_num}: \t {index_encrypted_text}")

# Розрахунок індексу відповідності для кожного з шифртекстів
indices = [index_open_text]
key_labels = ["ВТ"]
for key_num, key in enumerate(keys, start=1):
    with open(f'encrypted_text_{len(key)}.txt', 'r', encoding='utf-8') as file:
        encrypted_text = file.read()
    index_encrypted_text = calculate_index_of_coincidence(encrypted_text)
    indices.append(index_encrypted_text)
    key_labels.append(f"Ключ {key_num}")

# Побудова діаграми
plt.bar(key_labels, indices, color='pink')
plt.xlabel("Номери ключів")
plt.ylabel("Індекс відповідності")
plt.title("Індекси відповідності для шифртекстів")
plt.show()