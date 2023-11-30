def index_spivp(filtered_text):
    total_chars = len(filtered_text)
    char_count = {}

    for char in filtered_text:
        char_count[char] = char_count.get(char, 0) + 1

    ispivp = sum(count * (count - 1) for count in char_count.values()) / (total_chars * (total_chars - 1))
    return ispivp

def key_length(ciphertext, max_key_length=30):
    n = len(ciphertext)
    index_spivp_list = []

    for i in range(1, max_key_length + 1):
        matches = 0
        for j in range(n - i):
            if ciphertext[j] == ciphertext[j + i]:
                matches += 1
        index_spivp = matches / (n - i)
        index_spivp_list.append(index_spivp)

    possible_key_lengths = [i + 1 for i, val in enumerate(index_spivp_list) if val > 0.055]

    return possible_key_lengths, index_spivp_list
def common_char(text):
    char_count = {}
    for char in text:
        char_count[char] = char_count.get(char, 0) + 1

    most_common_char = max(char_count, key=char_count.get)
    return most_common_char
def vig_dec(ciphertext, key):
    decrypted_text = ""
    key_length = len(key)
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        key_char = key[i % key_length]
        decrypted_char = chr((ord(char) - ord(key_char)) % 32 + ord('а'))
        decrypted_text += decrypted_char
    return decrypted_text
def restore_key(ciphertext, key_length):
    key = ""
    for i in range(key_length):
        ith_block = ciphertext[i::key_length]
        most_common_char = common_char(ith_block)
        key_char = chr((ord(most_common_char) - ord('о')) % 32 + ord('а'))
        key += key_char
    return key

with open('D:\Навчання\СР\cp_lab2_enc.txt', 'r', encoding='utf-8') as file:
    ciphertext = file.read()

possible_key_lengths, index_spivp_list = key_length(ciphertext)
for i, val in enumerate(index_spivp_list):
    print(f"Значення індексу співпадіння при довжині ключа {i + 1}: {val}")
print("Ймовірна довжина ключа:", possible_key_lengths)

selected_key_length = possible_key_lengths[0]
estimated_key = restore_key(ciphertext, selected_key_length)
print("Можливий ключ:", estimated_key)
# print("Фактичний ключ: сонвлентююночь")

decrypted_text = vig_dec(ciphertext, 'сонвлентююночь')
file_path = r'D:\Навчання\СР\cp_lab2_dec.txt'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(decrypted_text)

