with open('filtered.txt', 'r', encoding = 'utf-8') as file:
    text = file.read()
with open('variant16.txt', 'r', encoding = 'utf-8') as file:
    crypted_text = file.read()

def encrypt(text, key):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    encrypted_text = ''
    for i in range(len(text)):
        char = alphabet[(alphabet.index(text[i]) + alphabet.index(key[i % len(key)])) % 32]
        encrypted_text += char
    return encrypted_text

def decrypt(text, key):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    decrypted_text = ''
    for i in range(len(text)):
        decrypted_text += alphabet[(alphabet.index(text[i]) - alphabet.index(key[i % len(key)])) % 32]
    return decrypted_text

def letter_count(text):
    dictt = {}
    for charr in text:
        if charr in dictt:
            dictt[charr] += 1
        else:
            dictt[charr] = 1
    return dictt

def comp_index(text):
    n = len(text)
    dictt = letter_count(text)
    summ = 0
    for key in dictt.keys():
        summ += dictt[key] * (dictt[key] - 1)
    return summ / (n * (n - 1))

def task1(text):
    keys = ["ви", "жен", "шифр", "текст", "шифротекст", "ходлабораторной", "методовкриптоанализа"]
    cases = ["r2", "r3", "r4", "r5", "r10", "r15", "r20"]
    for n in range(len(cases)):
        encrypted_text = encrypt(text, keys[n])
        print(cases[n] + ": " + str(comp_index(encrypted_text)))
        with open(cases[n]+".txt", 'w', encoding = "utf-8") as file:
            file.write(encrypted_text)

def divide_to_blocks(text, r):
    blocks=[]
    for _ in range(r):
        blocks.append("")
    for i in range(len(text)):
        blocks[i % r] += text[i]
    return blocks

def comp_index_for_blocks(text, r):
    blocks=divide_to_blocks(text, r)
    summ = 0
    for block in blocks:
        summ += comp_index(block)
    return summ / r

def find_key(text, r):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    blocks=divide_to_blocks(text, r)
    key = ""
    for i in range(r):
        dictt = letter_count(blocks[i])
        dictt = dict(sorted(dictt.items(), key=lambda item: item[1], reverse=True))
        #print(dictt)
        most_freq_letter = list(dictt.items())[0][0]
        key += str(alphabet[(alphabet.index(most_freq_letter) - 14) % 32])  #о №14 в списке начиная с нуля
    return(key)


"""
print("plain: " + str(comp_index(text)))
task1(text)

print("Finding key length for crypted text:")
for r in range(1, 26, 1):
    print("r" + str(r) + ": " + str(comp_index_for_blocks(crypted_text, r)))
"""

print("Finding key for crypted text:")
#key = find_key(crypted_text, 21)
key='башняяростичерныемаки'
print("Possible key: " + key)

decrypted_text = decrypt(crypted_text, key)
with open('variant16_decrypted_for_real.txt', 'w', encoding = 'utf-8') as file:
    file.write(decrypted_text)