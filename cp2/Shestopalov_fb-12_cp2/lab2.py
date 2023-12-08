import pandas as pd

alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def vigenere_encrypt(text, keys):
    encrypted_text = []
    key_lengths = [len(key) for key in keys]
    num_keys = len(keys)

    for i in range(len(text)):
        char = text[i]
        if char in alphabet:
            key_char = keys[i % num_keys][i % key_lengths[i % num_keys]]
            char_index = alphabet.index(char)
            key_index = alphabet.index(key_char)
            encrypted_char = alphabet[(char_index + key_index) % len(alphabet)]
            encrypted_text.append(encrypted_char)
    return ''.join(encrypted_text)

def vigenere_decrypt(text, key):
    decrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(text):
        if char in alphabet:
            ciphertext_idx = alphabet.index(char)
            key_char = key[i % key_length]
            key_idx = alphabet.index(key_char)
            decrypted_idx = (ciphertext_idx - key_idx) % len(alphabet)
            decrypted_text += alphabet[decrypted_idx]
        else:
            decrypted_text += char
    return decrypted_text

def count_vidpovidnist(text, alphabet):
    if len(text)>1:
        vidpovidnist = 0
        for char in alphabet:
            letter_count= text.count(char)
            vidpovidnist += letter_count*(letter_count-1)
    vidpovidnist/= (len(text)*(len(text)-1))
    return vidpovidnist

def generate_possible_keys(text, key_length):
    frequent_letters = 'оеатинслвр'
    possible_keys = {}
    for frequent_letter in frequent_letters:
        block_list = break_text_into_blocks(text, key_length)
        key = ""
        for block in block_list:
            most_frequent_symbol = max(block, key=lambda symbol: block.count(symbol))
            key += alphabet[(alphabet.index(most_frequent_symbol) - alphabet.index(frequent_letter)) % len(alphabet)]
        possible_keys[frequent_letter] = key
    return possible_keys

def break_text_into_blocks(text, block_size):
    blocks = [text[i::block_size] for i in range(block_size)]
    return blocks

def find_vidpovidnist(text):
    results = []
    for key_length in range(1, 41):
        blocks_list = break_text_into_blocks(text, key_length)

        index_sum = 0
        for block in blocks_list:
            block_index = count_vidpovidnist(block, alphabet)
            index_sum += block_index

        average_index = index_sum / len(blocks_list)
        print(key_length, f":  {average_index:.8f}")
        results.append({'Довжина ключа': key_length, 'Індекс відповідності': round(average_index, 15)})

    return results

def save_vidpovidnist(encrypted_text):
    key_length_results = find_vidpovidnist(encrypted_text)
    df_key_length = pd.DataFrame(key_length_results)
    df_key_length.to_excel("key_lengths.xlsx", index=False)
    print("Індекси відповідності збережені до файлу 'key_length.xlsx'")

    key_length = int(input("Введіть довжину ключа: "))
    return key_length

def find_key(text, key_length):
    frequent_letters = 'оеиантслвр'
    possible_keys = generate_possible_keys(text, key_length)

    for frequent_letter in frequent_letters:
        print(f"Можливий ключ: {possible_keys[frequent_letter]}")

    real_key = input("Введіть ключ: ")
    return real_key

with open('lab2_1.txt', 'r', encoding='utf-8') as file:
    text = file.read()
text=text.replace(" ", "")

key_lengths = [2, 3, 4, 5] + list(range(10, 21))

keys = ["оп", "кот", "ключ", "топот", "дипломатия", "водонепроницаемый"]
print("Початковий текст:  ", text)
for key in keys:
    encrypted_text = vigenere_encrypt(text, key)
    print("Зашифрований текст, ключ", key + ":", encrypted_text)
    print(count_vidpovidnist(encrypted_text, alphabet))

with open("startText.txt", "r", encoding="utf-8") as file:
    encrypted_text = file.read()

true_key_length = save_vidpovidnist(encrypted_text)

true_key = find_key(encrypted_text, true_key_length)

decrypted_text = vigenere_decrypt(encrypted_text, true_key)
with open("endText.txt", "w", encoding="utf-8") as file:
    file.write(decrypted_text)

print("Розшифрований текст збережений в endText.txt")