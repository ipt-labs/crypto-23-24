import matplotlib.pyplot as plt

def encrypted(text, key):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    encrypted_text = ''
    for i in range(len(text)):
        char = text[i]
        key_char = key[i%len(key)]
        encrypt_char_index = (alphabet.index(char) + alphabet.index(key_char)) % len(alphabet)
        encrypted_text += alphabet[encrypt_char_index]
    return encrypted_text

def decrypted(encrypt_text, key):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    decrypted_text = ''
    l = []
    for i in range(len(encrypt_text)):
        char = encrypt_text[i]
        key_char = key[i%len(key)]
        decrypted_char_index = (alphabet.index(char) - alphabet.index(key_char)) % len(alphabet)
        decrypted_text += alphabet[decrypted_char_index]
    l = [decrypted_text[i:i+len(key)] for i in range(0, len(decrypted_text) - len(key) + 1, len(key))]
    return l

def index_vidpovidnosti(text):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    count = 0
    for i in alphabet:
        temp = text.count(i)
        count += temp * (temp - 1)
    return count/(len(text)*(len(text)-1))

def search_len_key(text):
    d = {}
    for r in range(2,32):
        d[r] = 0
        sum = 0
        blocks = [text[i::r] for i in range(r)]
        for block in blocks:
            sum += index_vidpovidnosti(block)
        d[r] = sum/r
    return d

def search_key(text, len_key, char):
    for i in char:
        alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        result = ''
        blocks = [text[i::len_key] for i in range(len_key)]
        for block in blocks:
            letter_count = {}
            for letter in block:
                if letter in letter_count:
                    letter_count[letter] += 1
                else:
                    letter_count[letter] = 1
            max_letter = max(letter_count, key=letter_count.get)
            result += alphabet[(alphabet.index(max_letter)-alphabet.index(i))%len(alphabet)]
        return result
        


with open('Labs\Crypt_labs\Lab2\edited.txt', encoding='utf-8') as file:
    text = file.read()
text = text.replace(" ", '')
keys = ['ку', 'рад', 'пять', 'пресф', 'большойвзлом', 'урокикриптоанализа']
t = []
t.append(index_vidpovidnosti(text))
for key in keys:
    temp = encrypted(text, key)
    with open(f'Labs\Crypt_labs\Lab2\encrypt_{len(key)}.txt', 'w', encoding='utf-8') as file:
        file.write(temp)
    t.append(index_vidpovidnosti(temp))
len_key = [0]+[len(i) for i in keys]
#plt.bar(len_key, t, color='g')
#plt.title('Значення індексів відповідності', fontsize=14)
#plt.xticks(range(0,21))
#plt.xlabel('Період', fontsize=12)
#plt.ylabel('Індекс відповідності', fontsize=12)
#plt.show()
with open(r'Labs\Crypt_labs\Lab2\variant2_1.txt', encoding='utf-8') as file:
    text_1 = file.read()
d = search_len_key(text_1.replace(' ', ''))
print(d)
#plt.bar(d.keys(), d.values(), color='g')
#plt.title('Значення індексів відповідності', fontsize=14)
#plt.xticks(range(2,32))
#plt.xlabel('Період', fontsize=12)
#plt.ylabel('Індекс відповідності', fontsize=12)
#plt.show()
key_1 = search_key(text_1.replace(' ', ''), 14, 'е')
with open(r'Labs\Crypt_labs\Lab2\variant2_enc.txt','w', encoding='utf-8') as file:
    file.write(''.join(decrypted(text_1.replace(' ', ''), 'последнийдозор')))