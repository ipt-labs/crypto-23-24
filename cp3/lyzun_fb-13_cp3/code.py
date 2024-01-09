with open('16_utf8.txt', 'r', encoding = 'utf-8') as file:
    encrypted_text = file.read()
encrypted_text = encrypted_text.replace('\n', '')
alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
m = 31
most_freq_real = ["ст", "но", "то", "на", "ен"]

def euclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = euclid(b, a % b)
        return (g, y, x - y * (a // b))

def inverted(a, mod):
    g, x, y = euclid(a, mod)
    if g != 1:
        return None
    return x

def solve_eq(a, b, mod):
    g, x, y = euclid(a, mod)
    if b%g != 0:
        return None
    if g == 1:
        return [(inverted(a, mod) * b) % mod]
    a = a // g
    b = b // g
    mod1 = mod // g
    x = []
    xx = (inverted(a, mod1) * b) % mod1
    while xx < mod:
        x.append(xx)
        xx += mod1
    return x

def bigram_count(text, step):
    bigrams = [text[i]+text[i+1] for i in range(0, len(text) - 1, step)]
    #total = len(bigrams)
    dictt = {}
    for bigram in bigrams:
        if bigram in dictt:
            dictt[bigram] += 1
        else:
            dictt[bigram] = 1
    dictt = dict(sorted(dictt.items(), key=lambda item: item[1], reverse=True))
    return dictt

def letter_count(text):
    dictt = {}
    for charr in text:
        if charr in dictt:
            dictt[charr] += 1
        else:
            dictt[charr] = 1
    dictt = dict(sorted(dictt.items(), key=lambda item: item[1], reverse=True))
    return dictt

def most_freq_bi(text, n):
    most_frequent = []
    dictt = bigram_count(text, 2)
    for i in range(n):
        most_frequent.append(list(dictt.items())[i][0])
    return(most_frequent)

def decrypt(etext, key):
    dtext = ""
    bigrams = [etext[i]+etext[i+1] for i in range(0, len(etext) - 1, 2)]
    for bigram in bigrams:
        Y = bi_to_num(bigram)
        X = solve_eq(key[0], Y-key[1], m**2)
        if X is None:
            return None
        dtext += num_to_bi(X[0])
    return dtext

def bi_to_num(bi):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    return(alphabet.index(bi[0])*len(alphabet) + alphabet.index(bi[1]))

def num_to_bi(num):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
    x2 = num % len(alphabet)
    x1 = (num - x2) // len(alphabet)
    return(alphabet[x1] + alphabet[x2])

def text_check(text):
    impossible_bigrams = ["уь", "еь", "оь", "аь", "яь", "иь", "ыь", "ьь", "юь", "шы", "жы"]
    for bigram in impossible_bigrams:
        if bigram in text:
            print("Wrong text! " + bigram + " found!")
            return False
    return True

def find_key(etext):
    combinations = []
    keys = []
    most_freq_real = ["ст", "но", "то", "на", "ен"]
    most_freq_encrypted = most_freq_bi(etext, 5)
    for y1 in range(len(most_freq_encrypted)):
        for x1 in range(len(most_freq_real)):
            for y2 in range(len(most_freq_encrypted)):
                for x2 in range(len(most_freq_real)):
                    if x1 != x2 and y1 != y2:
                        combinations.append([bi_to_num(most_freq_real[x1]), bi_to_num(most_freq_encrypted[y1]), bi_to_num(most_freq_real[x2]), bi_to_num(most_freq_encrypted[y2])])
    for comb in combinations:
        aa = solve_eq(comb[0]-comb[2], comb[1]-comb[3], m**2)    #comb => [X1, Y1, X2, Y2]
        if aa is None:
            continue
        for a in aa:
            if a == 0:
                continue
            b = (comb[1] - a * comb[0]) % m**2
            if b == 0:
                continue
            if [a, b] not in keys:
                keys.append([a, b])
    print (keys)
    possible_keys = []
    for key in keys:
        print("Key: " + str(key))
        dtext = decrypt(etext, key)
        if dtext is None:
            print("Failed to decrypt!")
            continue
        if text_check(dtext):
            print("Text checked successfully!")
            possible_keys.append(key)
            #print(dtext)
            return dtext
    #print(possible_keys)

print("Most frequent bigrams in encrypted text: " + str(most_freq_bi(encrypted_text, 5)))
#find_key(encrypted_text)

with open('16_decrypted.txt', 'w', encoding = 'utf-8') as file:
    file.write(find_key(encrypted_text))

#a, b = 370, 312