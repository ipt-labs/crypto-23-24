def index_bigram(lst):
    result = []
    alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
    for bigram in lst:
        index_1 = alphabet.index(bigram[0])
        index_2 = alphabet.index(bigram[1])
        index = index_1 * len(alphabet) + index_2
        result.append(index)
    return result

def index_to_bigram(index):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'
    letter2 = alphabet[index%len(alphabet)]
    letter1 = alphabet[int(index//len(alphabet))]
    return letter1+letter2

def euclid_invert(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = euclid_invert(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def solve(number, b, module):
    if number < 0 or number > module:
        number %= module
    answer = []
    gcd, *invert = euclid_invert(number, module)
    if gcd == 1:
        x0 = b * invert[0] % module
        return [x0]
    elif gcd == 0 or b % gcd != 0:
        return 0
    else:
        x0 = solve(int(number//gcd), int(b//gcd), int(module//gcd))[0]
        for i in range(0, gcd):
            temp = (x0 + int(i*module//gcd)) % module
            answer.append(temp)
        return answer

def search_bigram(text):
    d = {}
    for index in range(0, len(text), 2):
        if text[index:index+2] not in d:
            d[text[index:index+2]] = 1
        else:
            d[text[index:index+2]] += 1
    d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
    return list(d.keys())[:5]

def search_combination(lst, list_bigram):
    combinations = []
    lst_index = index_bigram(lst)
    list_bigram_index = index_bigram(list_bigram)
    for x1 in list_bigram_index:
        for y1 in lst_index:
            temp_x = [x for x in list_bigram_index if x != x1]
            temp_y = [y for y in lst_index if y != y1]
            for x2 in temp_x:
                for y2 in temp_y:
                    combination = [x1,y1,x2,y2]
                    combinations.append(combination)
    return combinations

def search_keys(combinations):
    keys = []
    module = 31*31
    for x1, y1, x2, y2 in combinations:
        keys_a = solve(x1-x2, y1-y2, module)
        if not keys_a:
            continue
        else:
            for key_a in keys_a:
                key_b = (y1-key_a*x1)%module
                keys.append((key_a, key_b))
    return keys

def check_bigram(bigram):
    letter = 'уеыаоэяиюь'
    if bigram[0] in letter and bigram[1] == 'ь':
        return 0
    return 1

def decrypted(key, text):
    decrypted = ''
    for index in range(0, len(text)-1, 2):
        bigram_enc = index_bigram([text[index:index+2]])[0]
        bigram_dec_index = solve(key[0], bigram_enc - key[1], 31*31)
        if bigram_dec_index:
            bigram_dec = index_to_bigram(bigram_dec_index[0])
        else: 
            return None
        if check_bigram(bigram_dec):
            decrypted += bigram_dec
        else:
            return None
    return decrypted


with open(r'Labs\Crypt_labs\Lab3\var2_edit.txt', encoding='utf-8') as file:
    text = file.read()

bigram = search_bigram(text)
list_bigram = ['ст','но','то','на','ен']
print(bigram)
comb = search_combination(bigram, list_bigram)
#print(comb)
keys = search_keys(comb)
#print(keys)
for key in keys:
    temp = decrypted(key, text)
    if temp == None:
        continue
    else:
        print(temp)
        print(key)
        print('==================================')
