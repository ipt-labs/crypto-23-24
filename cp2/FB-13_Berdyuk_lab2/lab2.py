import string
import collections
import re
import matplotlib.pyplot as plt
import math
import csv

def text_transf(text, spec_chars):
    text = text.lower()
    text = "".join([char for char in text if char not in spec_chars])
    text = re.sub(r'[a-z]', '', text)
    text = re.sub(r'[0-9]', '', text)
    text = re.sub('ё', 'е', text)
    return text

def encrypt_transf(text, r):
    text_ord_new = ''
    for i in range(len(text)):
        b = (ord(text[i]) - 1072 + ord(r[i % len(r)]) - 1072)%32
        text_ord_new = text_ord_new + chr(b+1072)
    return text_ord_new

def I_count(text):
    result = collections.Counter(text)
    diction = dict(result)
    sum = 0
    for key, value in diction.items():
        sum = sum + value * (value - 1)
    I = sum/(len(text) * (len(text) - 1))
    return I



file = open('examp2.txt', "r", encoding="utf-8")
text = file.read()
spec_chars = string.punctuation + '\n\xa0«»\t—…' + ' ' + '`' + "'" + '’' + '¹²³⁴⁵⁶⁷⁸⁹⁰–”' + '\xad' + 'á“ó½'
text_n_sp = text_transf(text, spec_chars)
results = collections.Counter(text_n_sp)
print(results)
res_count_d = dict(results)
"""
sum = 0
for key, value in res_count_d.items():
    sum = sum + value*(value - 1)
I = sum/(len(text_n_sp)*(len(text_n_sp)-1))
print(I)
"""
print(I_count(text_n_sp))
r2 = 'на'
text_r2 = encrypt_transf(text_n_sp, r2)
print(text_r2[0:100])
print(I_count(text_r2))
with open("encrypt2.txt", "w") as file:
    file.write(text_r2)
text_r3 = encrypt_transf(text_n_sp, 'сон')
print(text_r3[0:100])
print(I_count(text_r3))
with open("encrypt3.txt", "w") as file:
    file.write(text_r3)
text_r4 = encrypt_transf(text_n_sp, 'боль')
print(text_r4[0:100])
print(I_count(text_r4))
with open("encrypt4.txt", "w") as file:
    file.write(text_r4)
text_r5 = encrypt_transf(text_n_sp, 'проза')
print(text_r5[0:100])
print(I_count(text_r5))
with open("encrypt5.txt", "w") as file:
    file.write(text_r5)
text_r12 = encrypt_transf(text_n_sp, 'криптография')
print(text_r12[0:100])
print(I_count(text_r12))
with open("encrypt12.txt", "w") as file:
    file.write(text_r12)
text_r13 = encrypt_transf(text_n_sp, 'окукливавшись')
print(text_r13[0:100])
print(I_count(text_r13))
file2 = open('cripted.txt', "r", encoding="utf-8")
text_decr = file2.read()
spec_chars = string.punctuation + '\n\xa0«»\t—…' + ' ' + '`' + "'" + '’' + '¹²³⁴⁵⁶⁷⁸⁹⁰–”' + '\xad' + 'á“ó½'
text_decr = text_transf(text_decr, spec_chars)
print(I_count(text_decr))

print("Індекс відповідності зашифрованного текста совпадает с моим текстом зашифрованным 12-буквенным словом")

l = len(text_decr)
for r in range(2,31):
    print(r, ':')
    sum = 0
    for i in range(r):
        sum = sum + I_count(text_decr[i:l:r])
    print(sum/r)
print("key is 12")
key = 'вшекспирбуря'
new_text = ''
for i in range(0,len(text_decr)):
    new_text = new_text + chr(((ord(text_decr[i])-1072)-(ord(key[i%12])-1072))%32+1072)
print(new_text[0:100])
print(I_count(new_text))
with open("decrypt.txt", "w") as file:
    file.write(new_text)

res1 = collections.Counter(text_decr[0:l:12])
res2 = collections.Counter(text_decr[1:l:12])
res3 = collections.Counter(text_decr[2:l:12])
res4 = collections.Counter(text_decr[3:l:12])
res5 = collections.Counter(text_decr[4:l:12])
res6 = collections.Counter(text_decr[5:l:12])
res7 = collections.Counter(text_decr[6:l:12])
res8 = collections.Counter(text_decr[7:l:12])
res9 = collections.Counter(text_decr[8:l:12])
res10 = collections.Counter(text_decr[9:l:12])
res11 = collections.Counter(text_decr[10:l:12])
res12 = collections.Counter(text_decr[11:l:12])

"""print(res1)
print(res2)
print(res3)
print(res4)
print(res5)
print(res6)
print(res7)
print(res8)
print(res9)
print(res10)
print(res11)
print(res12)"""

osn_list = ['о','е','а','н','т','и','л','с','р','в','к','д','у','м','п','г','ы','з','ч','я','ь','б','й','х','ж','ш','ц','э','щ','ф','ю','ъ']
list1 = ['р','з','ф','п','к','у','в','т','о','н','ж','ю','с','е','д','б','х','э','л','г','м','щ','я','и','ч','ъ','й','ц','ш','а','ы','']
list2 = ['ж','э','е','ш','и','к','в','а','д','ъ','й','ы','г','ф','з','л','ь','б','у','щ','ч','я','ю','п','х','р','о','ц','н','м','с','']
list3 = ['у','к','н','е','ч','ц','х','т','з','с','й','р','ш','ф','а','о','б','д','м','п','ж','и','ы','л','ь','ъ','ю','г','э','щ','в','']
list4 = ['п','ш','к','ч','ь','ы','х','т','ъ','м','щ','о','е','ц','л','ф','э','ж','й','с','у','н','я','б','а','з','и','в','р','г','']
list5 = ['я','с','ц','щ','в','г','у','б','ю','э','ь','а','ы','х','т','д','ф','ш','р','й','н','з','м','п','ъ','ж','ч','и','о','е','л','']
list6 = ['э','ф','ь','п','ъ','ч','б','я','а','ы','у','с','о','л','р','ю','к','т','ж','в','щ','ц','ш','з','д','е','н','м','х','г','']
list7 = ['ц','ъ','и','х','н','р','щ','ш','ч','ф','к','у','ы','д','м','т','г','л','с','з','й','я','п','ю','а','о','ь','ж','э','б','е','']
list8 = ['ю','х','р','э','б','в','ы','а','т','ш','ь','с','м','л','г','ъ','ф','я','щ','у','п','ч','з','е','о','ц','и','й','ж','н','д','']
list9 = ['п','б','о','ж','у','й','т','с','м','г','л','а','е','н','р','в','ь','э','к','ф','и','ц','щ','ш','д','ъ','з','я','х','ч','']
list10 = ['б','у','ш','а','ы','е','д','х','г','ч','э','в','я','ю','т','ж','ф','ъ','п','ц','ь','щ','к','и','л','о','й','с','м','р','']
list11 = ['ю','х','р','в','ш','б','э','а','ь','т','ф','ъ','ы','я','г','л','с','п','ч','у','м','щ','и','о','ц','е','й','н','з','ж','']
list12 = ['н','д','с','п','к','р','я','з','м','б','л','о','ъ','т','г','в','ы','ю','и','й','а','ф','ч','х','е','ж','у','ц','ь','э','']
text1 = text_decr[0:l:12]
text2 = text_decr[1:l:12]
text3 = text_decr[2:l:12]
text4 = text_decr[3:l:12]
text5 = text_decr[4:l:12]
text6 = text_decr[5:l:12]
text7 = text_decr[6:l:12]
text8 = text_decr[7:l:12]
text9 = text_decr[8:l:12]
text10 = text_decr[9:l:12]
text11 = text_decr[10:l:12]
text12 = text_decr[11:l:12]
text_all = text_decr
for i in range(len(text_decr)):
    if (i%12==0):
        k = list1.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==1):
        k = list2.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==2):
        k = list3.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==3):
        k = list4.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==4):
        if text_decr[i] in list5:
            k = list5.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==5):
        k = list6.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==6):
        k = list7.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==7):
        k = list8.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==8):
        k = list9.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==9):
        k = list10.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==10):
        k = list11.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
    if (i%12==11):
        k = list12.index(text_decr[i])
        text_all = text_all[:i] + osn_list[k] + text_all[i + 1:]
print(text_all)
print("Попытка расшифровать с помощью частотного анализа каждого блока")
for i in range(204):
    if (i%12==0):
        print('')
    print(chr(((ord(text_decr[i])-1072)-(ord(text_all[i])-1072))%32+1072), sep='', end='')
print('')
print("Берем самые частые буквы в предпологаемых ключах: получили вшекспирбуря")