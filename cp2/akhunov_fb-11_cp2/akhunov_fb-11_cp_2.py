import csv

# Це ключі шифрування, довжиною 2, 3, 4, 5, 10 і 20 відповідно
KEYS: tuple = ('да', 'дуб', 'хлеб', 'туман', 'облачность', 'завтрапятницакайфуем')

# Алфавіт
ALPHABET: str = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


# Ця функція зчитує текстовий файл та поверає string з текстом цього файлу
def file_read(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        text: str = file.read()
    return text


# Ця функція отримує текст та повертає редагований текст для подальшого аналізу
def text_edit(text: str) -> str:
    text = text.replace('ё', 'е')
    text = text.lower()
    text = ''.join(char for char in text if char in ALPHABET)
    text = text.replace(' ', '')
    return text


# Ця функція зашифровує текст
def encryption(key: str, input_text: str) -> str:
    global ALPHABET
    key_index: int = 0
    encrypted_text: str = ''
    for char in input_text:
        encrypted_char_index = (ALPHABET.index(char) + ALPHABET.index(key[key_index])) % len(ALPHABET)
        encrypted_char = ALPHABET[encrypted_char_index]
        encrypted_text += encrypted_char
        key_index = (key_index + 1) % len(key)
    return encrypted_text


# Ця функція рахує індекси відповідності
def affinity_index(encrypted_text: str) -> float:
    frequency: dict = {}
    affinity: float = 0.0
    for char in encrypted_text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    for char in frequency:
        affinity += (frequency[char] * (frequency[char] - 1)) / \
                    (len(encrypted_text) * (len(encrypted_text) - 1))
    return affinity


# Ця функція створює csv файл з результатами
def create_csv_file(filename: str, affinity_dict: dict):
    with open(filename, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Довжина ключа", "Індекс"])
        for affinity in affinity_dict:
            if affinity == 'Вхідний текст':
                key_len = 'Вхідний текст'
            else:
                key_len = len(affinity)
            affinity = affinity_dict[affinity]
            affinity = str(affinity).replace('.', ',')
            writer.writerow([key_len, affinity])


def main():
    text: str = file_read('task1.txt')
    affinity_dict: dict = {}
    text: str = text_edit(text)
    affinity_dict['Вхідний текст'] = affinity_index(text)
    for key in KEYS:
        encrypted_text = encryption(key, text)
        print(encrypted_text)
        affinity_dict[key] = affinity_index(encrypted_text)
    create_csv_file('Affinities.csv', affinity_dict)


if __name__ == "__main__":
    main()
