abc = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
         'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

#завдання 1-2
keys = ["бу", "хри", "шлкв", "фдубо", "кзжапрушвиют", "кактотакполучается"]

file = open('text_lab2.txt', 'r', encoding="UTF-8")
text = file.read()
plain_text = text.lower().replace('ё', 'е')

#шифрування
def vigenere_encrypt(plain_text, key):
    encrypted_text = ""
    for i in range(len(plain_text)):
        char = plain_text[i]

        if char in abc:
            text_i = abc.index(char)
            key_i = abc.index(key[i % len(key)])
            e_char = abc[(text_i + key_i) % len(abc)]
            encrypted_text += e_char
        else:
            encrypted_text += char

    return encrypted_text

for key in keys:
    encrypted_text = vigenere_encrypt(plain_text, key)
    print(f"Key: {key}\nEncrypted text: {encrypted_text}\n")

#індекси відповідності для відкритого та шифрованих текстів
def match_index(text):
    total_chars = len(text)
    frequencies = {}
    for char in text:
        if char.isalpha():
            char = char.lower()
            if char in frequencies:
                frequencies[char] += 1
            else:
                frequencies[char] = 1
    index_of_coincidence = sum(freq*(freq-1) for freq in frequencies.values()) / (total_chars*(total_chars-1))
    return index_of_coincidence

encrypted_texts = []
for key in keys:
    encrypted_text = vigenere_encrypt(plain_text, key)
    encrypted_texts.append(encrypted_text)

match_index_plain_text = match_index(plain_text)
match_index_encrypted_texts = [match_index(text) for text in encrypted_texts]

print(f"Індекс відповідності для відкритого тексту: {match_index_plain_text}")
for i, index in enumerate(match_index_encrypted_texts):
    print(f"Індекс відповідності для шифртексту з ключем {keys[i]}: {index}")







