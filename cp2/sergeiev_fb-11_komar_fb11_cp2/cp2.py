import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

def encrypt(text, key):
    encrypted_text = [alphabet[(alphabet.find(text[i]) + alphabet.find(key[i % len(key)])) % len(alphabet)]
                      for i in range(len(text))]
    return ''.join(encrypted_text)

def compliance_index(text):
    letters_count = Counter(text)
    text_len = len(text)
    index = sum(count * (count - 1) for count in letters_count.values()) / (text_len * (text_len - 1))
    return index

def break_into_blocks(text, r):
    return [text[i::r] for i in range(r)]

def mean_blocks(text):
    mean_num = {}
    for r in range(2, 31):
        blocks = break_into_blocks(text, r)
        index = sum(compliance_index(block) for block in blocks) / r
        mean_num[r] = index
    return mean_num
    
def find_key(text, r):
    blocks = break_into_blocks(text, r)
    letters = ['о', 'е', 'а', 'и', 'т', 'н', 'с', 'р', 'л', 'в', 'к', 'п', 'м', 'д', 'з', 'я',
               'у', 'г', 'ь', 'б', 'ы', 'й', 'ч', 'ю', 'ж', 'х', 'ш', 'щ', 'ц', 'э', 'ф']
    for letter in letters:
        key = []
        for block in blocks:
            blocks_num = Counter(list(block))
            max_num = max(blocks_num, key=blocks_num.get)
            key_letter = alphabet[(alphabet.index(max_num) - alphabet.index(letter)) % len(alphabet)]
            key.append(key_letter)
        print(''.join(key))

def decrypt(text, key):
    decrypted_text = [alphabet[(alphabet.find(text[i]) - alphabet.find(key[i % len(key)])) % len(alphabet)]
                      for i in range(len(text))]
    return ''.join(decrypted_text)

def table_plot(col1, col2, filename):
    df = pd.DataFrame({'Довжина': col1, 'Індекс': col2})
    df.to_csv(filename)
    plt.figure(figsize=(10,5))
    plt.bar(df['Довжина'], df['Індекс'], color='c')
    plt.xticks(df['Довжина'])
    plt.show()

#------- завдання 1 та 2 -------#
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

keys = {'k2': 'да', 'k3': 'жах', 'k4': 'який', 'k5': 'йолка', 'k11': 'вающенкотак', 'k14': 'жидобандеровцы'}

with open('text_to_encrypt.txt', 'r', encoding='utf-8') as file:
    text_to_encrypt = file.read()

k = ['text']
indices = [compliance_index(text_to_encrypt)]

for key, value in keys.items():
    encrypted = encrypt(text_to_encrypt, value)
    with open(f'encrypted_{key}.txt', 'w', encoding='utf-8') as file:
        file.write(encrypted)
        
    k.append(key)
    indices.append(compliance_index(encrypted))
    
table_plot(k, indices, 'indices_task_2.csv')

#------- завдання 3 -------#
    
with open('text_to_decrypt.txt', 'r', encoding='utf-8') as file:
    text_to_decrypt = file.read()
    
count = mean_blocks(text_to_decrypt)
table_plot(count.keys(), count.values(), 'indices_task_3.csv')
find_key(text_to_decrypt, 15)

key = 'арудазовархимаг'
res = decrypt(text_to_decrypt, key)
with open('decrypted_text.txt', 'w', encoding='utf-8') as file:
    file.write(res)
