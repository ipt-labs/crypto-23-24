import re
from collections import Counter
import numpy as np
import pandas as pd
import math

H0_WITH_SPACES = math.log2(34)
H0_WITHOUT_SPACES = math.log2(33)

def text_transform(text, w_s=True):
    content = text.lower()
    content = content.replace("ё", "е").replace("ъ","ь")
    content = re.findall(r'[а-яА-Я]+', content)
    if w_s:
        content = ' '.join(content)
    else:
        content = ''.join(content)
    return content

def letter_freq(text):
    letter_count = {}
    for letter in text:
        if letter in letter_count:
            letter_count[letter] +=1
        else:
            letter_count[letter] = 1
    return letter_count

def bigram_freq(text, with_space=True):
    if with_space:
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
    else:
        text = text.replace(' ', '')
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_count = Counter(bigrams)
    return dict(bigram_count)

def overlap(text, with_space=True):
    if with_space:
        bigrams = [text[i:i+2] for i in range(0,len(text)-1,2)]
    else:
        text = text.replace(' ', '')
        bigrams = [text[i:i+2] for i in range(0,len(text)-1,2)]
    bigram_count = Counter(bigrams)
    return dict(bigram_count)

def h1(freq):
    freq_arr = [i for i in freq.values()]
    probs = np.divide(freq_arr, np.sum(freq_arr))
    probs = probs[probs!=0]
    h1 = -np.dot(probs, np.log2(probs))
    return h1

def h2(freq):
    freq_arr = list(freq.values())
    probs = np.divide(freq_arr, np.sum(freq_arr))
    probs = probs[probs!=0]
    h2 = -np.dot(probs, np.log2(probs))/2
    return h2

if __name__ == "__main__":
    input_file = "/home/mhranik/kpi-labs/crypto-23-24/cp1/Hranik_FB-13_cp1/sample.txt"
    with open(input_file, 'r', encoding='utf-8') as input_file:
        extract = input_file.read()
    letter_freq_table_with_spaces = pd.DataFrame(list(letter_freq(text_transform(extract)).items()), columns=['Letter','Frequency'])
    print(letter_freq_table_with_spaces)
    letter_freq_table_without_spaces = pd.DataFrame(list(letter_freq(text_transform(extract, False)).items()), columns=['Letter','Frequency'])
    print(letter_freq_table_without_spaces)
    #print('Letter frequency with spaces: ', letter_freq(text_transform(extract)))
    #print('Letter frequency without spaces: ', letter_freq(text_transform(extract, False)))
    bigram_freq_table_with_spaces = pd.DataFrame(list(bigram_freq(text_transform(extract, False)).items()), columns=['Bigram','Frequency'])
    bigram_freq_table_without_spaces = pd.DataFrame(list(bigram_freq(text_transform(extract, False)).items()), columns=['Bigram','Frequency'])
    print(bigram_freq_table_with_spaces)
    print(bigram_freq_table_without_spaces)
    # print('Bigram frequency with spaces: ', bigram_freq(text_transform(extract)))
    # print('Bigram frequency without spaces: ', bigram_freq(text_transform(extract, False)))
    print('Letter entropy with spaces: ', h1(letter_freq(text_transform(extract))))
    print('Letter entropy without spaces: ', h1(letter_freq(text_transform(extract, False))))
    print('Bigram entropy with spaces: ', h2(bigram_freq(text_transform(extract))))
    print('Bigram entropy without spaces: ', h2(bigram_freq(text_transform(extract, False))))
    print('Bigram entropy with spaces and with intersections: ', h2(overlap(text_transform(extract))))
    print('Bigram entropy without spaces and with intersections: ', h2(overlap(text_transform(extract, False))))
    print('Letter redundancy with spaces: ', 1-(h1(letter_freq(text_transform(extract)))/H0_WITH_SPACES))
    print('Letter redundancy without spaces: ',1-(h1(letter_freq(text_transform(extract, False)))/H0_WITHOUT_SPACES))
    print('Bigram redundancy with spaces: ', 1-(h2(bigram_freq(text_transform(extract)))/H0_WITH_SPACES))
    print('Bigram redundancy without spaces: ', 1-(h2(bigram_freq(text_transform(extract, False)))/H0_WITHOUT_SPACES))
    print('Bigram redundancy with spaces and with intersections: ', 1-(h2(overlap(text_transform(extract)))/H0_WITH_SPACES))
    print('Bigram redundancy without spaces and with intersections: ', 1-(h2(overlap(text_transform(extract, False)))/H0_WITHOUT_SPACES))
    

