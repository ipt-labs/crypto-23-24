import random

text = 'text.txt'
all = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
encrypted_text = 'encrpt_t.txt'

def create_key(len):
    key = ''.join(random.choice(all) for _ in range(len))
    return key

def encryption(data, key):
    encoded_data = ''
    for i, el in enumerate(data):
        d_indx = all.index(el) 
        k_indx = all.index(key[i % len(key)])
        new_i_indx = ((d_indx + k_indx) % len(all)) 
        new_i = all[new_i_indx]
        encoded_data += new_i
    return encoded_data

def find_index(data):
    n = len(data)
    values = {}
    for i in data:
        if i in values:
            values[i] += 1
        else:
            values[i] = 1
    sum_of = 0
    for j in values.values():
        sum_of += j*(j-1)

    i = sum_of/(n*(n-1))

    return i


len_of_key = [2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
with open(encrypted_text, 'w', encoding='utf-8') as ws:
    all_keys = []
    for i in len_of_key:
        x = create_key(i)
        all_keys.append(x)
        with open(text, 'r', encoding='utf-8') as t:
            text_for_encrpt = t.read()
            print("\nІндекс відповідності відкритого тексту: ", find_index(text_for_encrpt))
        encrypted_text = 'encrpt_t.txt'
        done = encryption(text_for_encrpt, x)
        print(f"Індекс відповідності шифртексту ключ {i} : ", find_index(done))
        ws.write(f"\n\n Використання ключа довжиною {i}: \n")
        ws.write(done)
    print(all_keys)


