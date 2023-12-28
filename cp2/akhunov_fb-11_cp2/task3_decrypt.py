import csv

ALPHABET: str = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'


# Ця функція зчитує текстовий файл та поверає string з текстом цього файлу
def file_read(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        text: str = file.read()
    return text


# Ця функція зчитує csv файл зі списком найчастіше вживаних літер та повертає ці літери
def read_csv(path: str) -> str:
    data_dict = {}
    with open(path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                char = row[0]
                count = row[1]
                data_dict[char] = count
    del data_dict['Символ(и)']
    for item in data_dict:
        data_dict[item] = int(data_dict[item])
    sorted_data = dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=True))
    key_string = ''.join(sorted_data.keys())
    return key_string


# Ця функція розшифровує текст
def decryption(text: str, key: str) -> str:
    global ALPHABET
    key_index: int = 0
    decrypted_text: str = ''
    for char in text:
        decrypted_char_index = (ALPHABET.index(char) - ALPHABET.index(key[key_index])) % len(ALPHABET)
        decrypted_char = ALPHABET[decrypted_char_index]
        decrypted_text += decrypted_char
        key_index = (key_index + 1) % len(key)
    return decrypted_text


most_common_chars = read_csv('Mono_no_space.csv')
# print(most_common_chars)


# Ця функція генерує потенційний ключ ШТ
def key_finder(key_len: int, guess_chars: str, text: str):
    key: str = ''
    for i in range(key_len):
        frequencies: dict = {}
        for n in range(i, len(text), key_len):
            if text[n] in frequencies:
                frequencies[text[n]] += 1
            else:
                frequencies[text[n]] = 1
        char = max(frequencies, key=(lambda x: frequencies[x]))
        key += decryption(char, guess_chars[0])
    return key


text_to_decrypt = file_read('cp2_var15.txt')
print(decryption(text_to_decrypt, "посняковандрей"))
print(key_finder(14, most_common_chars, text_to_decrypt))
