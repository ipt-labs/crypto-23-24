import matplotlib.pyplot as plt

def text_preparing():
    with open("lab2_text.txt","r",encoding="utf-8") as t:
        data = t.read()
        formatted = "".join([l if l.isalpha() and l in "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ " else " " for l in data])
        formatted = " ".join(formatted.split())
        formatted = formatted.replace('ё', 'е')
        formatted = "".join([l.lower() for l in formatted])
        formatted = "".join([x for x in formatted if x != " "])

    with open("processed_text_lab2.txt", "w", encoding="utf-8") as t:
        t.write(formatted)

    return formatted


def vigenere_encoding(txt, cipher_key):
    cipher_key_len = len(cipher_key)
    dictionary = dict(enumerate('абвгдежзийклмнопрстуфхцчшщъыьэюя'))
    dict_keys = list(dictionary.keys())
    dict_values = list(dictionary.values())
    cipher_key_nums = [dict_keys[dict_values.index(x)] for x in cipher_key]  # перетворюємо ключ на цифри
    blocks = []
    ciphered_text = ""

    # ділимо відкритий текст на блоки довжиною довжини ключа
    for i in range(0, len(txt), cipher_key_len):
        blocks.append(txt[i:i+cipher_key_len])

    # шифруємо блоки ключем
    for block in blocks:
        block_nums = [dict_keys[dict_values.index(x)] for x in block]  # перетворюємо блок на цифри
        cipher_block = [sum(i) % 32 for i in zip(block_nums, cipher_key_nums)]  # шифруємо блок
        cipher_block_text = "".join([dictionary[x] for x in cipher_block])  # перетворюємо в текст
        ciphered_text += cipher_block_text
    with open("cipher_text_with_key_len_"+str(cipher_key_len)+".txt", "w", encoding="utf-8") as file:
        file.write(ciphered_text)

    return ciphered_text


def index(txt):
    coefficient = len(txt)*(len(txt)-1)
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    count_dict = {x: txt.count(x) for x in alphabet}
    i_y = 0
    for key in count_dict.keys():
        i_y += count_dict[key] * (count_dict[key]-1)

    i_y = i_y/coefficient
    return i_y


def indexes_for_unknown_cipher(txt):
    arr_of_total_indexes = []
    for r in range(2, 32):
        i_y = 0
        for i in range(0, r):
            string = ""
            for j in range(i, len(txt) - r + 1, r):
                string += txt[j]
            i_y += index(string)
        arr_of_total_indexes.append((r,i_y/r))
    return arr_of_total_indexes


def key_len(lst):
    for i in lst:
        if (i[1] / theoretical_i) * 100 > 90:
            return i[0]


def key_bruteforce(txt, key_r):
    key_nums = []
    letter = ''
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    dictionary = dict(enumerate(alphabet))
    dict_keys = list(dictionary.keys())
    dict_values = list(dictionary.values())
    for r in range(0, key_r):
        string = ""
        for char in range(r,len(txt)-r,key_r):
            string += txt[char]
        count_dict = {x: string.count(x) for x in alphabet}
        most_frequent = max(count_dict,key=count_dict.get)
        letter += most_frequent
        key_nums.append(dict_keys[dict_values.index(most_frequent)])

    string_key = ""
    for idx in key_nums:
        string_key += dictionary[(idx - 14 + 32) % 32] # віднімаємо індекс найпопулярнішої букви ("о")
    return string_key

def create_plot(arr):

    x = []
    y = []
    for i in range(0, len(arr)):
        x.append(arr[i][0])
        y.append(arr[i][1])

    plt.scatter(x, y)
    plt.xticks(range(len(x)+ 2), range(len(y)+ 2))
    plt.xlabel("Довжина ключа")
    plt.ylabel("Індекс")
    plt.savefig('graph.png')


def vigenere_decoding(text,key):
    key_len = len(key)
    dictonary = dict(enumerate('абвгдежзийклмнопрстуфхцчшщъыьэюя'))
    dict_keys = list(dictonary.keys())
    dict_values = list(dictonary.values())
    key_nums = [dict_keys[dict_values.index(x)] for x in key]# перетворюємо ключ на цифри
    blocks = []
    ciphered_text = ""
    # ділимо відкритий текст на блоки довжиною довжини ключа
    for i in range(0,len(text),key_len):
        blocks.append(text[i:i+key_len])

    # шифруємо блоки ключем
    for block in blocks:
        block_nums = [dict_keys[dict_values.index(x)] for x in block] # перетворюємо блок на цифри
        cipher_block = [i[0]-i[1] if i[0]-i[1] >= 0 else i[0]-i[1]+32 for i in zip(block_nums, key_nums)] # шифруємо блок
        cipher_block_text = "".join([dictonary[x] for x in cipher_block])
        ciphered_text += cipher_block_text
    with open("deciphered_text.txt","w",encoding="utf-8") as file:
        file.write(ciphered_text)


keys = {
    2: "ло",
    3: "вап",
    4: "свап",
    5: "укрна",
    10: "йцукенгштр",
    15: "фчвсипкуцйвнгот"
}
for value in keys.values():
    text = text_preparing()
    cipher_text = vigenere_encoding(text, value)
    print(index(cipher_text))
theoretical_i = 0.05520961681534098
with open("personal_text_var17.txt", "r", encoding="utf-8") as f:
    personal_text = f.read()

list_of_indexes = indexes_for_unknown_cipher(personal_text)
create_plot(list_of_indexes)
key_length = key_len(list_of_indexes)

variant_key = key_bruteforce(personal_text, key_length)
deciphered_text = vigenere_decoding(personal_text,"абсолютныйигрок")

