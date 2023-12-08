import re
from collections import Counter
import math
import pandas as pd

with open("text.txt", encoding='utf8') as file:
    text = file.read()

alphabet_without_spaces = 'абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'
alph = []
for i in alphabet_without_spaces:
    alph.append(i)
alphsp = []
alphabet_with_spaces = ' абвгдеёэжзиыйклмнопрстуфхцчшщъьюя'
for i in alphabet_with_spaces:
    alphsp.append(i)

def letters_frequency1(txt):
    c = Counter()
    frequency = {}
    total = 0

    for line in txt:
        c += Counter(line)

    for letter in alphabet_without_spaces:
        frequency[letter] = c[letter] / len(txt)

    for i in frequency.values():
        total += i * math.log2(i)
    h1 = -total
    print('H1:', h1)

    R = 1 - (h1 / math.log2(len(alphabet_without_spaces)))
    print('R:', R)

def letters_frequency(txt, alphabet, excel_filename):
    c = Counter()
    frequency = {}
    total = 0

    for line in txt:
        c += Counter(line)

    for letter in alphabet:
        frequency[letter] = c[letter] / len(txt)

    for i in frequency.values():
        total += i * math.log2(i)
    h1 = -total
    print('H1:', h1)

    R = 1 - (h1 / math.log2(len(alphabet)))
    print('R:', R)

    letters_data = pd.DataFrame(data=frequency, index=['частота'])
    letters_data.to_excel(excel_filename)

with open("text.txt", encoding='utf8') as file:
    text = file.read()

splited = re.compile('[^а-яёА-ЯЁ ]').sub('', text).rstrip('.,').lower().split(' ')

cleansp = ' '.join(splited)
clean = ''.join(splited)

with open('clean_text_with_spaces.txt', 'w', encoding='utf8') as clean_textsp:
    clean_textsp.write(cleansp)

with open('clean_text.txt', 'w', encoding='utf8') as clean_text:
    clean_text.write(clean)

letters_frequency(cleansp, alphabet_with_spaces, 'frequency_of_letters_with_spaces.xlsx')
letters_frequency(clean, alphabet_without_spaces, 'frequency_of_letters_without_spaces.xlsx')



def frequency_of_bigrams(txt, intersection=True):
    c = Counter()
    frequency = {}
    index = 0

    if txt == clean:
        alph = alphabet_without_spaces
    else:
        alph = alphabet_with_spaces

    for letter_first in alph:
        for letter_second in alph:
            bgrm = letter_first + letter_second
            c[bgrm] = 0

    if intersection is True:
        for i in range(len(txt) - 1):
            bgrm = txt[i] + txt[i + 1]
            c[bgrm] += 1

        for bgrm in c.keys():
            frequency[bgrm] = c[bgrm] / sum(c.values())

    else:
        for i in range(0, len(txt) - 1, 2):
            bgrm = txt[i] + txt[i + 1]
            c[bgrm] += 1

        for bgrm in c.keys():
            frequency[bgrm] = c[bgrm] / sum(c.values())

    total = 0
    for i in frequency.values():
        if i > 0:
            total += i * math.log2(i)
    h2 = -total / 2
    print('H2:', h2)

    R = 1 - (h2 / math.log2(len(alph)))
    print('R:', R)

    bgrm_frqnc = list(frequency.values())
    bigrams_data = pd.DataFrame(data=frequency, index=alph, columns=alph)

    for i in range(0, len(alph)):
        bigrams_data[alph[i]] = bgrm_frqnc[index:len(alph) + index]
        index = len(alph) + index

    bigrams_data.to_excel('frequency_of_bigrams.xlsx')

letters_frequency1(clean)
frequency_of_bigrams(clean, intersection=False)

info = pd.DataFrame(index=alphabet_without_spaces.split(), columns=alphabet_without_spaces.split())
