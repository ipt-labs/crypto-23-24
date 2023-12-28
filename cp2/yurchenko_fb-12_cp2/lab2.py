from random import choice

Alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
l = [i for i in range(2,6)]+[i for i in range(10,21)]

def vig_enc(plain, key):
    enc_text = ""
    key_len = len(key)
    for i in range(len(plain)):
        char = plain[i]
        key_char = key[i % key_len]
        enc_char = chr((ord(char) + ord(key_char)) % 32 + ord('а'))
        enc_text += enc_char
    return enc_text

def gen_key(length):
    key = ''.join(choice(Alph) for _ in range(length))
    return key

def index_vidpov(text):
    char_freq = {}
    text_len = len(text)
    for char in list(text):
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1
    s = 0
    for i in char_freq.keys():
        s += char_freq[i] * (char_freq[i] - 1)
    s = s/(text_len*(text_len-1))
    return s

def find_key(r, text):
    res = ""
    blocks = ['']*r
    for i in range(len(text)):
        blocks[i%r] += text[i]
    for block in blocks:
        a = max(block, key=block.count)
        res += chr(((ord(a) - ord('о')) % 32) + ord('а'))
    return res

def vig_dec(enc_text, key):
    plain = ""
    key_len = len(key)
    for i in range(len(enc_text)):
        char = enc_text[i]
        key_char = key[i % key_len]
        dec_char = chr((ord(char) - ord(key_char)) % 32 + ord('а'))
        plain += dec_char
    return plain 

with open("text2.txt", encoding="utf-8") as f:
    text = list(f.read().lower())
plain = ''.join([i for i in text if i in Alph])

print("Індекс відповідності для відкритого тексту:", index_vidpov(plain))
for key_len in l:
    key = gen_key(key_len)
    enc_text = vig_enc(plain, key)
    #print(key, enc_text[:20])
    print(f"Індекс відповідності для шифртексту з ключем довжини {key_len}: {index_vidpov(enc_text)}")
print("\n")
with open("variant10.txt", encoding="utf-8") as f:
    variant = f.read()
for r in range(2, 31):
    indeces = 0
    for i in range(0, r):
        block = "".join([variant[i] for i in range(i,len(variant)-r+1,r)])
        indeces += index_vidpov(block)
    index_value = indeces / r
    print(f"Індекс відповідності для блоків довжини {r}: {index_value}")

print("\nМожливий ключ:", find_key(15, variant))
right_key = 'крадущийсявтени'
plain_variant = vig_dec(variant, right_key)
print(f"\nПравильний ключ: {right_key}\n\n{plain_variant}")

with open('plain_variant.txt', 'w', encoding="utf-8") as f:
        f.write(plain_variant)
