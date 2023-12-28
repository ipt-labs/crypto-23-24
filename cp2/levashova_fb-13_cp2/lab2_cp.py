import re
def edited_text(text):
    text = text.replace("ъ", "ь")
    text = text.replace("ё", "е")
    text = re.sub(r'[^а-яА-Я]', ' ', text)
    text = re.sub(r'[a-zA-Z]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.replace(" ", "")
    return text
def vig_enc(filtered_text, key):
    encrypted_text = ""
    key_length = len(key)

    for i in range(len(filtered_text)):
        char = filtered_text[i]
        key_char = key[i % key_length]
        shift = ord(key_char) - ord('а')
        encrypted_char = chr((ord(char) - ord('а') + shift) % 32 + ord('а'))
        encrypted_text += encrypted_char
    return encrypted_text
def index_spivp(filtered_text):
    total_chars = len(filtered_text)
    char_count = {}
    for char in filtered_text:
        char_count[char] = char_count.get(char, 0) + 1
    ispivp = sum(count * (count - 1) for count in char_count.values()) / (total_chars * (total_chars - 1))
    return ispivp

with open('D:\Навчання\СР\kafka-na-plyazhe.txt', 'r', encoding='utf-8') as file:
    text = file.read()
new_text = edited_text(text)

with open('D:\Навчання\СР\kafka-na-plyazhe-lab2.txt', 'w', encoding='utf-8') as file:
    file.write(new_text)

open_text_file_path = r'D:\Навчання\СР\kafka-na-plyazhe-lab2.txt'
with open(open_text_file_path, 'r', encoding='utf-8') as file:
    open_text = file.read()

keys_to_try = ["еж", "кум", "шара", "роман", "параллельно", "незнаюнестикався", "криптографическийкод"]

encrypted_texts = []
for key in keys_to_try:
    encrypted_text = vig_enc(open_text, key)
    encrypted_texts.append(encrypted_text)
    # print(f"Зашифрований текст для ключа '{key}': {encrypted_text}")

open_text_ispivp = index_spivp(open_text)
print(f"Індекс співпадіння для відкритого тексту: {open_text_ispivp}")

encrypted_texts_ispivp = [index_spivp(text) for text in encrypted_texts]
for i, ispivp in enumerate(encrypted_texts_ispivp):
    key = keys_to_try[i]
    print(f"Індекс співпадіння для зашифрованого тексту з ключем '{key}': {ispivp}")

