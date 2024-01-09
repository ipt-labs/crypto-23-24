import re
import matplotlib.pyplot as plt
from collections import Counter
def repeat_items(l, c):
    return l * (c // len(l)) + l[:(c % len(l))]

def encrypt(plain_text, key):
    encrypted = ""
    split_plain_text = [
        plain_text[i : i + len(key)] for i in range(0, len(plain_text), len(key))
    ]

    for each_split in split_plain_text:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1

    return encrypted


def filtrate(ini_text,  write_file):
    with open(ini_text, 'r', encoding='utf-8') as file:
          text = file.read()
    text = text.lower()
    text_i = re.sub('[^а-я]+', '', text)
    with open (write_file, 'w', encoding='utf-8') as file_2:
         file_2.write(text_i)
    file.close()
    file_2.close()


def calculate_letter_frequencies(text):
    letter_frequencies = {}
    for char in text:
        #if char.isalpha():
            if char in letter_frequencies:
                letter_frequencies[char] += 1
            else:
                letter_frequencies[char] = 1
    return letter_frequencies

def find_complience_index(text):
    text_l = len(text)
    freq_dict = calculate_letter_frequencies(text)
    ic = sum(freq_dict * (freq_dict - 1) for freq_dict in freq_dict.values()) / (text_l * (text_l - 1))
    return ic

def key_length(text):
    text = text.lower()
    key_length = {}
    for i in range(2, 40):
        blocks = [text[n::i] for n in range(i)]
        block_ics = [find_complience_index(block) for block in blocks]
        avg_ic = sum(block_ics) / len(block_ics)
        key_length[i] = avg_ic

    return key_length


def find_vigenere_key(ciphertext, key_length):

    groups = [[] for _ in range(key_length)]
    for i, char in enumerate(ciphertext):
        group_index = i % key_length
        groups[group_index].append(char)

    probable_key = ''
    for group in groups:
        letter_frequencies = {}
        for char in group:
        # if char.isalpha():
            if char in letter_frequencies:
                letter_frequencies[char] += 1
            else:
                letter_frequencies[char] = 1
        most_common_char = max(letter_frequencies, key=letter_frequencies.get)
        key_letter = chr(((ord(most_common_char) - ord('о')) % 32) + ord('а'))
        probable_key += key_letter

    return probable_key

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
print(letter_to_index)
index_to_letter = dict(zip(range(len(alphabet)), alphabet))
print(index_to_letter)

def decrypt(cipher, key):
    decrypted = ""
    split_encrypted = [
        cipher[i : i + len(key)] for i in range(0, len(cipher), len(key))
    ]

    for each_split in split_encrypted:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted





l = 'variant4text.txt'
l_filt = 'variant4text_filtrated.txt'
filtrate(l, l_filt)
filtrate('lab2CP_originaltext.txt', 'lab2CP_filtrated.txt')
with open('variant4text_filtrated.txt', 'r', encoding='utf-8') as file:
    encrypted_text = file.read()
with open('lab2CP_filtrated.txt', 'r', encoding='utf-8') as file:
    text = file.read()
key_list = ['да', 'нет', 'кора', 'мутка', 'силиконовый', 'авиаконструктор', 'богостроительство', 'межправительственный']
b_text = find_complience_index(text)
print("індекс відповідності для оригінального відфільтрованого тексту: ", b_text)
for i in key_list:
    a = encrypt(text, i)
    index = find_complience_index(a)
    #print(f"закодований текст з ключем {i}: ", a)
    print(f"індекс відповідності для шифртексту з ключем {i}", index)
    #z = decrypt(a, i)
    #print(f"розкодований текст з ключем {i}: ", z)


freq_dict = calculate_letter_frequencies(text)
#print(freq_dict)
#print(freq_dict.values())
c = key_length(encrypted_text)
for i_i in c:
    print(f"Індекс відповідності для ключа довжини :",i_i, c[i_i])
plt.bar(c.keys(), c.values())
plt.xlabel('length of key')
plt.ylabel('IC')
plt.show()
b = find_complience_index(encrypted_text)
print('Ключ:', find_vigenere_key(encrypted_text, 13))
got_key = 'громыковедьма'
decrypted_text = decrypt(encrypted_text, got_key)
write_file_decrypted = 'Variant4_decrypted.txt'
with open(write_file_decrypted, 'w', encoding='utf-8') as file_2:
    file_2.write(decrypted_text)


