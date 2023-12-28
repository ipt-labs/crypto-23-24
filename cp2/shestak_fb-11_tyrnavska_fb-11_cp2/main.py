import text_manipulator as tm
from collections import Counter


# Getting open text
text = tm.get_text("valid_text_without_spaces.txt")
# Keys for encrypting
keys = ['да', 'нет', 'соль', 'сахар', 'синиймакар', 'светлоитеплосеогодня']


# Function for encrypting text using vigenere method
def vig_encrypt(key, text_ex):
    # Using list comprehension, ord() func and encrypting formula we are getting encrypted text
    encrypted_text = [
        chr((ord(text[i]) + ord(key[i % len(key)])) % 32 + ord('а'))
        for i in range(len(text_ex))
    ]
    return ''.join(encrypted_text)


# Function for counting compliance index for some text
def index(text_ex):
    first_part = 1 / (len(text_ex) * (len(text_ex) - 1))
    second_part = [n * (n - 1) for n in Counter(text_ex).values()]
    second_part = sum(second_part)
    return first_part * second_part


# Function for making blocks of text
def separator(text_ex, key_len):
    groups = [text_ex[i::key_len] for i in range(key_len)]

    return groups


# Function for counting comp. index for specific length of key
def indexes(groups):
    all_indexes = []

    for i in range(len(groups)):
        first_part = 1 / (len(groups[i]) * (len(groups[i]) - 1))
        second_part = [n * (n - 1) for n in Counter(groups[i]).values()]
        second_part = sum(second_part)
        all_indexes.append(first_part * second_part)

    mean_index = sum(all_indexes) / len(all_indexes)

    return mean_index


# Function for see if values approximately equal
def approx_equal(x, y, epsilon=0.001):
    return abs(x - y) < epsilon


# Encryption testing
# encrypted = vig_encrypt('да', 'привет')
# print(encrypted)

#############################
# 1, 2 tasks

print('Open text:')
print(text)
print(f"Index: {index(text)}")
print()

for k in keys:
    print(f"Encrypted text with key '{k}' (length of key is {len(k)}):")
    enc = vig_encrypt(k, text)
    print(enc)
    print(f"Index: {index(enc)}")
    print()


#############################
# 3 task

# Getting encrypted text
enc_text = tm.get_text("encrypted_var1.txt")


# Getting value of I for open text
# freqs_sqs = [float(i)**2 for i in tm.get_frequency("letters_frequency_without_spaces.csv").values()]
# MI = sum(freqs_sqs)  # 0.05593598260963655
# print(MI)

# Getting most possible length of key using value of I and comparing these values
Ind = 0
r = 1
while not approx_equal(0.0553, Ind):
    r += 1
    Ind = indexes(separator(enc_text, r))

# We got length of r. It's 12
print("r =", r)


# Making groups of letters to get most frequent ones later
enc_groups = separator(enc_text, r)

# Using table from previous lab getting list of most frequent letters in ruzzian language
most_fr_letter = [letter for letter in tm.get_frequency("letters_frequency_without_spaces.csv").keys()]


# Function for getting most possible key using groups of letters
def get_fin_keys(groups):
    fin_key = ''
    for i in groups:
        counter = Counter(i)
        most_fr_letter_in_group = counter.most_common(1)[0][0]
        pos = (ord(most_fr_letter_in_group) - ord(most_fr_letter[0])) % 32
        fin_key += chr(pos + 1072)

    return fin_key


# Function for decrypting encrypted text
def vig_decrypt(key, text_ex):
    # Using list comprehension, ord() func and decrypting formula we are getting decrypted text
    decrypted_text = [
        chr((ord(text_ex[i]) - (ord(key[i % len(key)]))) % 32 + ord('а'))
        for i in range(len(text_ex))
    ]
    return ''.join(decrypted_text)


# Getting key
print(get_fin_keys(enc_groups))

# We got key "вшебспирбуря", and it stands for "В. Шекспир - Буря"
# So key is "вшекспирбуря"

# Text decrypting
print(vig_decrypt('вшекспирбуря', enc_text))
