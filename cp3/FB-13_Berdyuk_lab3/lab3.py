import string
import collections
import re
import math

def text_transf(text, spec_chars):
    text = text.lower()
    text = "".join([char for char in text if char not in spec_chars])
    text = re.sub(r'[a-z]', '', text)
    text = re.sub(r'[0-9]', '', text)
    return text

def count_Hn(n, diction):
    length = 0
    for key, value in diction.items():
        length = length + value
    H_n = 0
    for key, value in diction.items():
        H_n = H_n - (value / length) * math.log(value / length, 2)
    return H_n/n

def evclid(a, b):
    u, u_temp, v, v_temp = 1, 0, 0, 1
    while (b!=0):
        q = a // b
        a, b = b, a % b
        u, u_temp = u_temp, u - u_temp*q
        v, v_temp = v_temp, v - v_temp*q
    return (u, v, a)

def rivnyanya(a, b, n):
    all_x = []
    gcd = evclid(a, n)[2]
    if (gcd==1):
        all_x.append((evclid(a, n)[0])*b%n)
        return all_x
    if (b%gcd!=0):
        return None
    x = (evclid(a//gcd, n//gcd)[0])*(b//gcd)%(n//gcd)
    for i in range(gcd):
        x_temp = x + (n//gcd)*i
        all_x.append(x_temp)
    return all_x



file = open('examp.txt', "r", encoding="utf-8")
file_2 = open('19.txt', "r", encoding="utf-8")
text = file.read()
text_2 = file_2.read()
spec_chars = string.punctuation + '\n\xa0«»\t—…' + ' ' + '`' + "'" + '’' + '¹²³⁴⁵⁶⁷⁸⁹⁰–”' + '\xad' + 'á“ó½'
text_n_sp = text_transf(text, spec_chars)
text_2 = text_transf(text_2, spec_chars)
bigrams = [text_n_sp[i:i+2] for i in range(len(text_n_sp)-1)]
bigram_counts = collections.Counter(bigrams)
print(bigram_counts)
bigrams_2 = [text_2[i:i+2] for i in range(0,len(text_2)-1,2)]
bigram_counts_2 = collections.Counter(bigrams_2)
print(bigram_counts_2)
print(evclid(51, 89))
print(rivnyanya(39,30,111))
alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
print(bigrams_2)
pop_b = ['то', 'ст', 'но', 'ен', 'на']
pop_b_19 = ['уф', "иж", "ьи", "хф", "щф"]
key = []
for i in range(5):
    x1 = alphabet.index(pop_b[i][0])*31+alphabet.index(pop_b[i][1])
    for j in range(5):
        if (i!=j):
            x2 = alphabet.index(pop_b[j][0])*31+alphabet.index(pop_b[j][1])
            for k in range(5):
                y1 = alphabet.index(pop_b_19[k][0])*31+alphabet.index(pop_b_19[k][1])
                for p in range(5):
                    if (k!=p):
                        y2 = alphabet.index(pop_b_19[p][0])*31+alphabet.index(pop_b_19[p][1])
                        a = rivnyanya(x1 - x2, y1 - y2, 31 * 31)
                        b = []
                        if (a != None):
                            for h in range(len(a)):
                                b.append((y1 - a[h] * x1) % (31 * 31))
                            print(a, b)
                            de_text = ''
                            for g in range(len(bigrams_2)):
                                b_temp = bigrams_2[g]
                                y = len(alphabet) * alphabet.index(b_temp[0]) + alphabet.index(b_temp[1])
                                x = evclid(a[0], 31 * 31)[0] * (y - b[0]) % (31 * 31)
                                de_text = de_text + alphabet[x // 31]
                                de_text = de_text + alphabet[x % 31]
                            if "аь" in de_text or "оь" in de_text or "еь" in de_text or "эь" in de_text or "иь" in de_text or "ыь" in de_text:
                                print("Bad case")
                            else:
                                if (i < 5 and j < 5 and (i!=j) and k < 5 and p < 5 and (k!=p)):
                                    print(pop_b[i], end=' ')
                                    print(pop_b[j])
                                    print(pop_b_19[k], end=' ')
                                    print(pop_b_19[p])
                                    print(de_text[:100])
                                    key.append(a)
                                    key.append(b)
                    else:
                        continue
        else:
            continue

print("key: ",key[0], key[1])
de_text = ''
for g in range(len(bigrams_2)):
    b_temp = bigrams_2[g]
    y = len(alphabet) * alphabet.index(b_temp[0]) + alphabet.index(b_temp[1])
    x = evclid(key[0][0], 31 * 31)[0] * (y - key[1][0]) % (31 * 31)
    de_text = de_text + alphabet[x // 31]
    de_text = de_text + alphabet[x % 31]
print(de_text[:200])

with open("decrypt19.txt", "w") as file:
    file.write(de_text)

