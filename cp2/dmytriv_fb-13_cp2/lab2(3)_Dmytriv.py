import matplotlib.pyplot as plt

ciphered = 'var13.txt'
all = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
result = 'result_var13.txt'

def blocks(data, len_key):
    all_blocks = []
    for i in range(len_key):
        b = data[i:: len_key]
        all_blocks.append(b)
    return all_blocks

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

def index_for_key(list_of_blocks):
    sum_of = 0
    for block in list_of_blocks:
        indx = find_index(block)
        sum_of += indx

    index_key = sum_of/len(list_of_blocks)
    return index_key

def key_len_by_index(text):
    key_index = {}
    for k  in range(2,31):
        bl = blocks(text, k)
        indx_= index_for_key(bl)
        key_index.update({k: indx_})
    return key_index

def decryption(data, key):
    deciphered_data = ''
    for i, el in enumerate(data):
        d_indx = all.index(el) 
        k_indx = all.index(key[i % len(key)])
        new_i_indx = ((d_indx - k_indx) % len(all)) 
        new_i = all[new_i_indx]
        deciphered_data += new_i
    return deciphered_data

with open(ciphered, 'r', encoding='utf-8') as t:
        cphrd_text = t.read()

res = key_len_by_index(cphrd_text) 
for k, i in res.items():
    print(f"Індекс для ключа довжиною {k}: {i}")

len_of_our_key = max(res, key=res.get)
print('Довжина нашого ключа: ', len_of_our_key)

for_x = list(res.keys())
for_y = list(res.values())
plt.scatter(for_x, for_y)
plt.xticks(range(len(for_x)+ 2), range(len(for_x)+ 2))
plt.xlabel("Довжина ключа")
plt.ylabel("Індекс")
plt.show()

def what_key(data, len_key):
    blcks = blocks(data, len_key)
    most_often = {}
    for b in blcks:
        num = {}
        for ltr in b:
            if ltr in num:
                num[ltr] += 1
            else:
                num[ltr] = 1
        num_sorted = dict(sorted(num.items(), key=lambda item: item[1], reverse=True))
        kkeys = list(num_sorted.keys())
        number_ = 0
        oftn_l = kkeys[number_]
        most_often.update({ (blcks.index(b) + 1): oftn_l})
    letter_key = ''
    for v in most_often.values():
        o_indx = all.index('р') 
        v_indx = all.index(v)
        k_ind = (v_indx - o_indx) % 32
        k_ltr = all[k_ind]        
        letter_key += k_ltr

    print(letter_key)

what_key(cphrd_text, len_of_our_key)

key = 'родинабезразличия'
res_13 = decryption(cphrd_text, key)
print("Ключ: ", key, ' ', res_13)
with open(result, 'w', encoding='utf-8') as ws:
    ws.write(res_13)
