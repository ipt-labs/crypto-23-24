#max_key_lenghts_guess = 30
encrypted_text = "D:\python\crypta\lab2var15.txt"
alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
decrypted_text = "D:\python\crypta\decrypted_text.txt"

with open(encrypted_text, 'r', encoding='utf-8') as file:
    text = file.read()
text = text.replace('\n', '')
with open(encrypted_text, 'w', encoding='utf-8') as file:
    file.write(text)

def calculate_index_of_coincidence(plain_text):
    total_characters = len(plain_text)
    total_frequencies = 0
    for character in alphabet:
        frequency = plain_text.count(character)
        total_frequencies += frequency*(frequency -1)
    index_of_coincidence = total_frequencies/(total_characters*(total_characters-1))
    return index_of_coincidence


def find_key_length(text):
    max_index = 0.053
    best_l = 2 #з попереднього завдання 2 - найкраща довжина
    for i in range (2, 30):
        block = ''
        for character in range(i, len(text)-i+1, i):
            block += text[character]
        block = ''.join(block)
        index = calculate_index_of_coincidence(block)
        if index>max_index:
            max_index = index
            best_l = i
    return best_l


key_length = find_key_length(text)
print(f"Довжина ключа: {key_length}")



def find_key(text, key_length):
    key = ""
    for i in range(key_length):
        fragments = text[i::key_length]
        charachter = max(set(fragments), key=fragments.count) #пошук найуживанішого символа - літера о
        #move = (ord(charachter) - ord('о')) % 32 #чомусь такий спосіб видає незрозумілі символи
        #key += chr((ord('o') + move) % 32)
        move = alphabet.index(charachter) - alphabet.index('о')
        key += alphabet[move]
    return key

key = find_key(text, key_length)
print(f"Ключ: {key}")

def decryption(text, key):
    plaintext = ''
    for i in range (len(text)):
        p = alphabet.index(text[i])
        k = alphabet.index(key[i%key_length])
        c = (p-k)%32
        plaintext += alphabet[c]
    return plaintext

decrypted = decryption(text, key)
print (decrypted)



