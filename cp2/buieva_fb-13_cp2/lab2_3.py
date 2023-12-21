from collections import Counter

abc = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
         'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

def normalized_text(alphabet, file_name):
    with open(file_name, "r", encoding='UTF-8') as file:
        text = file.read().lower().replace("ё", "е")
        for char in text[:]:
            if char not in alphabet and char != " ":
                text = text.replace(char, "")
        return "".join(text.split())

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

def split_to_blocks(text, length):
    blocks = []
    for i in range(length):
        blocks.append(text[i::length])
    return blocks


def find_key_length(encoded_text):
    index_length_dict = {}
    for i in range(2, 31):
        blocks = split_to_blocks(encoded_text, i)
        index = 0
        for block in blocks:
            index += match_index(block)
        index /= len(blocks)
        index_length_dict[i] = index
        key_length_index = dict(sorted(index_length_dict.items(), key=lambda x: x[1], reverse=True))
    return key_length_index

probabilities_of_symbol={}
def letter_frequencies(some_text):
    number_of_each_letter = Counter(some_text)
    total_number = len(some_text)
    for letter, k in number_of_each_letter.items():
        probabilities_of_symbol[letter] = k / total_number
    sorted_probabilities_of_symbol = dict(sorted(probabilities_of_symbol.items(), key=lambda x: x[1], reverse=True))
    return sorted_probabilities_of_symbol

def find_key(encoded_text, key_length):
    blocks = split_to_blocks(encoded_text, key_length)
    most_used_letters = "оаеин"
    possible_keys = []
    for letter in most_used_letters:
        key = ""
        for block in blocks:
            most_used_letter_encoded_text = list(letter_frequencies(block).keys())[0]
            key_part = abc[(abc.index(most_used_letter_encoded_text) - abc.index(letter)) % len(abc)]
            key += key_part
        possible_keys.append(key)
    return possible_keys

def vigenere_decrypt(plain_text, key):
    decrypted_text = ""
    for i in range(len(plain_text)):
        char = plain_text[i]

        if char in abc:
            text_i = abc.index(char)
            key_i = abc.index(key[i % len(key)])
            d_char = abc[(text_i - key_i) % len(abc)]
            decrypted_text += d_char
        else:
            decrypted_text += char

    return decrypted_text

text_to_decode = normalized_text(abc, "lab2_3_encrypted_text.txt")
keys_length = find_key_length(text_to_decode)
possible_key_length = list(keys_length.keys())[0]
print(keys_length)
print(find_key(text_to_decode, possible_key_length))
key = "конкистадорыгермеса"
print(vigenere_decrypt(text_to_decode, key))
