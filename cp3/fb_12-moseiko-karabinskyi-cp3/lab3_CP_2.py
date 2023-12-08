import re
from collections import Counter
def filtrate(ini_text,  write_file):
    with open(ini_text, 'r', encoding='Windows-1251') as file:
          text = file.read()
    text = text.lower()
    text_i = re.sub('[^а-я]+', '', text)
    with open (write_file, 'w', encoding='Windows-1251') as file_2:
         file_2.write(text_i)
    file.close()
    file_2.close()

def calculate_bigram_frequencies(text):
    bigram_frequencies = {}
    for i in range(0, len(text), 2):
        bigram = text[i:i + 2]
        #if bigram.isalpha():
        if bigram in bigram_frequencies:
            bigram_frequencies[bigram] += 1
        else:
            bigram_frequencies[bigram] = 1
    common_keys = dict(sorted(bigram_frequencies.items(), key=lambda x: x[1], reverse=True))
    common_keys = list(common_keys.keys())
    res = common_keys[:5]
    return res



def inverse(a, m):
    gcd, x, y = extended_gcd_2(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def extended_gcd_2(a, b):
    old_r, r = a, b
    x, s = 1, 0
    y, t = 0, 1
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        x, s = s, x - quotient * s
        y, t = t, y - quotient * t
    gcd = old_r
    return (gcd, x, y)


# ax = b mod m
def congurence(a, b, m):

    gcd, x, y = extended_gcd_2(a,m)
    if b % gcd !=0:
        return 0

    find_x = inverse(a//gcd, m//gcd) * (b//gcd) % (m//gcd)
    all_x = []
    for i in range(gcd):
        _x = find_x + i * m % (m * gcd)
        all_x.append(_x)
    return all_x

def bigram_to_numbers(bigram):
    return (alphabet.index(bigram[0]))*m+alphabet.index(bigram[1])

def what_key(text, most_used_bigram):
    most_common_encbigram = calculate_bigram_frequencies(text)
    var_keys = []
    for i in range(len(most_used_bigram)):
        for j in range(len(most_used_bigram)):
            for q in range(len(most_common_encbigram)):
                for w in range(len(most_common_encbigram)):
                    if i != j and q != w:
                        X1, X2 = bigram_to_numbers(most_used_bigram[i]), bigram_to_numbers(most_used_bigram[j])
                        Y1, Y2 = bigram_to_numbers(most_common_encbigram[q]), bigram_to_numbers(most_common_encbigram[w])
                        X = X1 - X2
                        Y = Y1 - Y2
                        if inverse(X, m**2) is not None:
                            a = congurence(X, Y, m**2)
                            if a is not None:
                                for c in a:
                                    if c > 0 and inverse(c, m**2) is not None and c not in [key[0] for key in var_keys]:
                                        b = (Y1 - c*X1) % m**2 
                                        if b > 0:
                                            decrypted_text = decrypt_text(text, c, b)
                                            var_keys.append((c, b))
                                            if check_text(decrypted_text) > 7:
                                                #print("Decrypted text: ", decrypted_text)
                                                return decrypted_text


def decrypt_text(text, a, b):
    decrypted_text = ""
    for i in range(0, len(text) - 1, 2):
        bigram = text[i: i + 2]
        Y = bigram_to_numbers(bigram)
        X = (congurence(a, Y - b, m**2)[0])
        bigram1 = X // 31
        bigram2 = X % 31
        decrypted_text += alphabet[int(bigram1)]
        decrypted_text += alphabet[int(bigram2)]
    return decrypted_text

def check_text(text):
    check = 0
    dict_with_res = Counter(text)
    sorted_dict = dict(sorted(dict_with_res.items(), key=lambda item: item[1], reverse=True))
    l_text = list(sorted_dict.keys())[:3]
    for i in l_text:
        if i in most_used_letters:
            check += 1
    l_text = list(sorted_dict.keys())[-3:]
    for j in l_text:
        if j in most_rare_letters:
            check += 1
    most_common_encbigram = calculate_bigram_frequencies(text)
    for b in most_common_encbigram:
        if b in most_used_bigram:
            check += 1
    return check


alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
m = 31
non_filtr = 'CP3_var04.txt'
most_used_bigram = ['ст', 'но', 'то', 'на', 'ен']
most_used_letters = ['о', 'е', 'а']
most_rare_letters = ['ф', 'щ', 'ь']
ex = 'CP3_var04_filtrated.txt'
filtrate(non_filtr, ex)
with open(ex, 'r', encoding='Windows-1251') as file:
     encoded_text = file.read()
bigram_freq = calculate_bigram_frequencies(encoded_text)
print("\nЧастота біграм:")
print(extended_gcd_2(13, 103))
print(inverse(13,103))
print(congurence(17, 86, 113))
sol = what_key(encoded_text, most_used_bigram)
#print(often_bigram(encoded_text, option))
print(bigram_freq)
file_to_write = open('decrypted_text_lab3.txt', 'w')
file_to_write.write(sol)