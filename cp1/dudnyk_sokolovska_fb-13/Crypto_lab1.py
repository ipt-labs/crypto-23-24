import numpy 
import re
from collections import defaultdict
import pandas as pd

alphabet = list('абвгдежзийклмнопрёъыстуфхцчшщьэюя ')

def process_text(file_name):     
    file = open(file_name, "rt", encoding='UTF-8')
    text = file.read()
    text = text.lower()
    text = text.replace("\n", "")
    text = text.replace("ё", "е")
    text = text.replace("ъ", "ь")
    text = text.replace("ы", "ь")
    symbols = "? , . … ; “ „ : -  ! ( ) * « » \ / — 1 2 3 4 5 6 7 8 9 0 №" 
    for i in symbols.split():
        text = text.replace(i, " ")
    return text

text = process_text("text.txt")
text_no_spaces = text.replace(" ", "")


def frequency(text, symbols_list):
    freq_dict = {}
    for i in symbols_list:
        matches = re.findall(rf'{i}', text)
        freq_dict[i] = len(matches)
    return freq_dict

def frequency_bigrams(text, stepUse = True):
    step = 2 if stepUse else 1
    bigrams = defaultdict(int)
    for i in range(0, len(text)-1, step):
        bigram = text[i:i+2]
        bigrams[bigram] += 1
    return bigrams


def get_H(frequency):
    probability_sum = sum(frequency.values())
    general_sum = 0
    for i in frequency:
        if frequency[i] != 0:
            p = frequency[i] / probability_sum
            general_sum -= p * numpy.log2(p)
    return general_sum

def get_R(h, h0 = numpy.log2(len(alphabet))):    
    return 1 - (h/h0)

my_data = { "h1" : get_H(frequency(text, alphabet)), "r1" : get_R(get_H(frequency(text, alphabet))), 
            "h2-crossed":get_H(frequency_bigrams(text)), "h2-uncrossed": get_H(frequency_bigrams(text, False)),
            "r2-crossed":get_R(get_H(frequency_bigrams(text))), "r2-uncrossed":get_R(get_H(frequency_bigrams(text, False)))}


my_data2 = { "h1" : get_H(frequency(text_no_spaces, alphabet)), "r1" : get_R(get_H(frequency(text_no_spaces, alphabet))), 
            "h2-crossed":get_H(frequency_bigrams(text_no_spaces)), "h2-uncrossed": get_H(frequency_bigrams(text_no_spaces, False)),
            "r2-crossed":get_R(get_H(frequency_bigrams(text_no_spaces))), "r2-uncrossed":get_R(get_H(frequency_bigrams(text_no_spaces, False)))}

df = pd.DataFrame(data=my_data, index=[0])

# my_data = frequency_bigrams(text_no_spaces, False)
# df = pd.DataFrame(data=my_data, index=[0])
# df.to_excel('entropy-and-redundancy.xlsx')

# print("R2 from h2:")
# print(get_R(get_H(frequency_bigrams(text))))