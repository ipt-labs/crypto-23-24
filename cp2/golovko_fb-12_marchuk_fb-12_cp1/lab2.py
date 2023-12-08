# Function to encrypt plaintext with Vigenère cipher
def clean_text(text):

    text = ' '.join(text.split())
    text = text.lower()
    text = ''.join(char for char in text if (char.isalpha() and ord(char)>1071 and ord(char)<1106))
    return text
def vigenere_cipher(plaintext, key):
    encrypted_text = []
    repeat_count = len(plaintext) // len(key)
    key_repeated = key * repeat_count
    key_repeated += key[:len(plaintext) - len(key_repeated)]
    # print(key_repeated)
    # print(plaintext)
    plaintext=[*plaintext]
    key_repeated=[*key_repeated]
    for i in range(0,len(plaintext)):
        encrypted_text.append(chr((ord(plaintext[i])-1071+ord(key_repeated[i])-1071)%32 +1070))
    return "".join(encrypted_text)
def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.lower()
    key = key.lower()
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    decrypted_text = ''

    for i in range(len(ciphertext)):
        if ciphertext[i] in alphabet:
            shift = (alphabet.index(ciphertext[i]) - alphabet.index(key[i % len(key)])) % 32
            decrypted_text += alphabet[shift]
        else:
            decrypted_text += ciphertext[i]

    return decrypted_text

def find_freq(formated_text):
    letter_frequency = {}
    for litera in formated_text:
        if litera in letter_frequency:
            letter_frequency[litera] += 1
        else:
            letter_frequency.update({litera: 1})
    return letter_frequency
def print_freq(let_freq,formated_text):
    print("загальна "," відсоток від ")
    print("кількість"," загального")
    for letter, frequency in sorted(let_freq.items(), key=lambda x:x[1], reverse=True):
        print(f"{letter}: {frequency},    %= {round(int(frequency)/len(formated_text)*100,3)}")
    return None
def calc_IC(letter_freq,total_length):
    ic = 0.0
    for count in letter_freq.values():
        ic += (count * (count - 1)) / (total_length * (total_length - 1))
    return ic
def calc_IC_block(text,r):
    temp_ic=0
    for j in range(0,r):
        new_block=[]
        for i in range(0,len(text)+1,r):
            try:
                new_block.append(text[i+j])
            except:
                break
        temp_freq=find_freq(new_block)
        temp_ic+=calc_IC(temp_freq,len(new_block))
    return temp_ic/r

def get_key(text,r):
    for j in range(0,r):
        new_block=[]
        for i in range(0,len(text)+1,r):
            try:
                new_block.append(text[i+j])
            except:
                break
        temp_freq=find_freq(new_block)
        # print_freq(temp_freq,new_block)
        o_enc=max(temp_freq, key=temp_freq.get)
        # print(o_enc)
        if ord(o_enc)-1086>0:
            print(chr(ord(o_enc)-14),end="")
        else:
            print(chr((ord(o_enc)-1070+16)%32+1072),end="")
    return "."
def get_key2(text,r):
    for j in range(0,r):
        new_block=[]
        for i in range(0,len(text)+1,r):
            try:
                new_block.append(text[i+j])
            except:
                break
        temp_freq=find_freq(new_block)
        o_enc=max(temp_freq, key=temp_freq.get)
        # print(o_enc)
        if ord(o_enc)-1077>0:
            print(chr(ord(o_enc)-5),end="")
        else:
            print(chr((ord(o_enc)-1070+7)%32+1072),end="")
    return "."
def theoretical_ic(letter_freq,text_length):
    result=float()
    for i in letter_freq.values():
        result+=(float(i)/text_length)**2
    return result

input_file_path = 'D:\\uni year 3\\crypto labs\\crypto-23-24\\cp2\\Igor_Marchuk_Maria_holovko_FB-12\\test.txt'
with open(input_file_path, 'r', encoding='utf-8') as file:

    text = file.read()
text=clean_text(text)
text1_freq=find_freq(text)

# print_freq(text1_freq,text)
# print(calc_IC(text1_freq,len(text)))

# Read input text from a file
input_file = "D:\\uni year 3\\crypto labs\\crypto-23-24\\cp2\\Igor_Marchuk_Maria_holovko_FB-12\\input_to_cipher.txt"
with open(input_file, "r",encoding='utf-8') as file:
    plaintext = file.read()
# Specify the key
key = "лимон"

# Encrypt the plaintext using the Vigenère cipher
encrypted_text = vigenere_cipher(plaintext, key)
text2_freq=find_freq(encrypted_text)
# print(calc_IC(text2_freq,len(encrypted_text)))

# print(calc_IC_avg(encrypted_text,3))
# print(calc_IC_avg(text,3))
# print(calc_IC_avg(text,20))
# print(theoretical_ic(32))
# print(encrypted_text)

# print(plaintext)
# plain_freq=find_freq(plaintext)
# print(calc_IC(plain_freq,len(encrypted_text)))
# print('**')
# crypto1=vigenere_cipher(plaintext,"ма")
# crypto1_freq=find_freq(crypto1)
# print(calc_IC(crypto1_freq,len(encrypted_text)))
# print(theoretical_ic(crypto1_freq,len(encrypted_text)))
# print("******")
crypto2=vigenere_cipher(plaintext,"мяу")
# crypto2_freq=find_freq(crypto2)
# print(calc_IC(crypto2_freq,len(encrypted_text)))
# print(theoretical_ic(crypto2_freq,len(encrypted_text)))
# print("******")
# crypto3=vigenere_cipher(plaintext,"котя")
# crypto3_freq=find_freq(crypto3)
# print(calc_IC(crypto3_freq,len(encrypted_text)))
# print(theoretical_ic(crypto2_freq,len(encrypted_text)))
# print("******")
crypto4=vigenere_cipher(plaintext,"рябина")
# print(calc_IC_block(crypto4,2))
# print(calc_IC_block(crypto4,3))
# print(calc_IC_block(crypto4,4))
# print(calc_IC_block(crypto4,5))
# print(calc_IC_block(crypto4,6))

# crypto4_freq=find_freq(crypto4)
# print(calc_IC(crypto4_freq,len(encrypted_text)))
# print(theoretical_ic(crypto4_freq,len(encrypted_text)))
# print("******")
crypto5=vigenere_cipher(plaintext,"арбуз")
# crypto5_freq=find_freq(crypto5)
# print(calc_IC(crypto5_freq,len(encrypted_text)))
# print(theoretical_ic(crypto5_freq,len(encrypted_text)))
# print("******")


task_freq=find_freq(text)
for i in range (1,32):
    print(i,"=",calc_IC_block(text,i))
# print_freq(task_freq,text)
# print(theoretical_ic(task_freq,len(text)))
# for i in range (1,32):
#     print(i,"=",calc_IC_block(text,i))
print(get_key(text,12))
print(get_key2(text,12))
print(vigenere_decrypt(text,"вшекспирбуря"))
# word1='вшебспирбуря'
# word2='лбокъшсщккщи'
# for i in range(len(word1)):
#     for j in range(len(word2)):
#         combined_word = word1[:i] + word2[j] + word1[i+1:]
#         print(combined_word)