import re


def filter_text(text):
    text = re.sub(r'[a-zA-Z]', '', text)
    text = text.lower()
    text = text.replace('ё', 'е')
    text = re.sub(r'[^а-яА-Я]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(" ", "")
    return text

with open("text_cp2", "r", encoding="utf8") as input_file:
    text = input_file.read()

filtered_text = filter_text(text)

with open("text_cp2_edited.txt", "w", encoding="utf-8") as output_file:
    output_file.write(filtered_text)



def vigenere_encrypt(text, key):
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    alphabet_dict = {letter: index for index, letter in enumerate(alphabet)}
    encrypted_text = ""
    key_index = 0

    for char in text:

        if char in alphabet_dict:
            text_index = alphabet_dict[char] # получаем индекс текущей буквы в тексте
            key_char = key[key_index % len(key)] # получаем текущую букву ключа
            key_index += 1
            encrypted_index = (text_index + alphabet_dict[key_char]) % len(alphabet) # буква текста + буква ключа по модулю
            encrypted_char = alphabet[encrypted_index] # буква, соответствующая индексу encrypted_index в алфавите
            encrypted_text += encrypted_char

    return encrypted_text



def index_of_coincidence(text):
    n = len(text)
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    sum_frequencies = 0

    for letter in alphabet:
        frequency = text.count(letter)
        sum_frequencies += frequency * (frequency - 1)

    index_of_coincidence = sum_frequencies / (n * (n - 1))

    return index_of_coincidence



def find_key_length(text):
    max_ic = 0
    best_key_length = 2

    for i in range(2, 21):
        block = "".join([text[char] for char in range(i, len(text) - i + 1, i)])
        ic = index_of_coincidence(block)

        if ic > max_ic:
            max_ic = ic
            best_key_length = i

    return best_key_length



# Убираем переносы
with open('cp2_var11.txt', 'r', encoding='utf-8') as file:
    text = file.read()
text_without_newlines = text.replace('\n', '')
with open('cp2_var11_norm.txt', 'w', encoding='utf-8') as file:
    file.write(text_without_newlines)



def find_vigenere_key(txt, key_length):
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    key = ""

    for i in range(key_length):
        group = txt[i::key_length]  # разбиваем текст на фрагменты размером с ключ
        count_dict = {x: group.count(x) for x in alphabet}
        most_common_char = max(set(group), key=group.count)  # самый встречающийся символ
        shift = alphabet.index(most_common_char) - alphabet.index('о')  # вычисляем сдвиг
        key += alphabet[shift]
        count_dict.clear()

    return key



def vigenere_decrypt(text, key):
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    alphabet_dict = {letter: index for index, letter in enumerate(alphabet)}

    decrypted_text = ""
    key_index = 0

    for char in text:

        if char in alphabet_dict:
            encrypted_index = alphabet_dict[char]  # получаем индекс зашифрованной буквы
            key_char = key[key_index % len(key)]  # получаем текущую букву ключа
            key_index += 1
            decrypted_index = (encrypted_index - alphabet_dict[key_char]) % len(alphabet) # буква ключа - зашифрованная буква по модулю
            decrypted_char = alphabet[decrypted_index]  # буква, соответствующая индексу decrypted_index
            decrypted_text += decrypted_char

    return decrypted_text



# Шифруем открытый текст
# key = "жемчужинка"
# encrypted_text = vigenere_encrypt(filtered_text, key)
# print(encrypted_text)

# Ищем индекс соответствия
# coincidence_index = index_of_coincidence(encrypted_text)
# print(f"Индекс соответствия: {coincidence_index:.6f}")

# Потенциальная длинна ключа в тексте 11 варианта
# key_length = find_key_length(text_without_newlines)
# print(f"Найденная длина ключа: {key_length}")

# Поиск ключа зная длину
# key = find_vigenere_key(text_without_newlines, key_length)
# print(f"Найденный ключ: {key}")

# Расшифровуем шифрованый текст
# decrypted_text = vigenere_decrypt(text_without_newlines, "венецианскийкупец")
# print(decrypted_text)
# with open('cp2_var11_decrypted.txt', 'w', encoding='utf-8') as file:
#     file.write(decrypted_text)

