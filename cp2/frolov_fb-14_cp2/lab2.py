import re

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"


def filter_read(filename: str) -> str:
    with open(filename, "r") as f:
        text = f.read().strip().lower()
    text = re.sub('[^а-я]+', '', text)
    return text


def encrypt(text: str, key: str) -> str:
    encrypted = ""
    chunks = [text[chunk_start_pos: chunk_start_pos + len(key)] for chunk_start_pos in range(0, len(text), len(key))]
    for chunk in chunks:
        pos_in_chunk = 0
        for letter in chunk:
            number = ((ord(letter) - 1071) + (ord(key[pos_in_chunk]) - 1071)) % 32  # 32 is alphabet length
            encrypted += chr(number + 1071)
            pos_in_chunk += 1
    return encrypted.lower()


def decrypt(text: str, key: str) -> str:
    decrypted = ""
    chunks = [text[chunk_start_pos: chunk_start_pos + len(key)] for chunk_start_pos in range(0, len(text), len(key))]
    for chunk in chunks:
        pos_in_chunk = 0
        for letter in chunk:
            number = ((ord(letter) - 1071) - (ord(key[pos_in_chunk]) - 1071)) % 32  # 32 is alphabet length
            decrypted += chr(number + 1072)
            pos_in_chunk += 1
    return decrypted.lower()


def get_index(text: str) -> float:
    frequency_dict = {}
    for letter in text:
        if letter in frequency_dict:
            frequency_dict[letter] += 1
        else:
            frequency_dict[letter] = 1

    index = (1 / (len(text) * (len(text) - 1))) * sum(letter_value * (letter_value - 1) for letter_value in frequency_dict.values())
    return index


def key_length(text) -> int:
    index_by_key = {}
    for i in range(2, 30):
        chunks = [text[n::i] for n in range(i)]
        block_index = [get_index(chunk) for chunk in chunks]
        average_index = sum(block_index) / len(block_index)
        index_by_key[i] = average_index

    min_key_prob = 0
    result_key = 0
    for key in index_by_key:
        if index_by_key[key] > min_key_prob:
            min_key_prob = index_by_key[key]
            result_key = key
    return result_key


def find_vigenere_key(txt, key_length) -> str:
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    key = ""

    for i in range(key_length):
        chunk = txt[i::key_length]
        count_dict = {x: chunk.count(x) for x in alphabet}
        most_common_char = max(set(chunk), key=chunk.count)
        shift = alphabet.index(most_common_char) - alphabet.index('о')
        key += alphabet[shift]
        count_dict.clear()

    return key


keys = ["он", "два", "пять", "полет", "самолетнебовысоко"]
text_to_encrypt = filter_read("toencrypt.txt")

print(f"Індекс відповідності для відкритого тексту: {get_index(text_to_encrypt)}")

for key in keys:
    encrypted_text = (encrypt(text_to_encrypt, key))
    print(f"{get_index(encrypted_text)} - Індекс відповідності для тексту зашифровакого ключем \"{key}\"")

text_to_decrypt = filter_read("todecrypt_11.txt")
key_len = key_length(text_to_decrypt)
print(f"\nВірогідна довжина ключа: {key_len}")
print(f"Вірогідний ключ: {find_vigenere_key(text_to_decrypt, key_len)}")

with open("todecrypt_11_decrypted.txt", "w") as f:
    f.write(decrypt(text_to_decrypt, "венецианскийкупец"))