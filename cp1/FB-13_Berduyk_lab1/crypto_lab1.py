import string
import collections
import re
import math
import csv

def text_transf(text, spec_chars):
    text = text.lower()
    text = "".join([char for char in text if char not in spec_chars])
    text = re.sub(r'[a-z]', '', text)
    text = re.sub(r'[0-9]', '', text)
    return text

def csv_write(file_name, diction):
    """with open(f'{file_name}.csv', 'a', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for key, value in diction:
            writer.writerow({key, value})"""
    length = 0
    for key, value in diction.items():
        length = length + value
    with open(file_name, 'a', encoding='cp1251', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for key, value in diction.most_common():
            writer.writerow((key, value/length))


def count_Hn(n, diction):
    length = 0
    for key, value in diction.items():
        length = length + value
    H_n = 0
    for key, value in diction.items():
        H_n = H_n - (value / length) * math.log(value / length, 2)
    return H_n/n

def count_R(Hn):
    return (1-Hn/5)*100

file = open('examp.txt', "r", encoding="utf-8")
text = file.read()
spec_chars_sp = string.punctuation + '\n\xa0«»\t—…' + '`' + "'" + '’' + '¹²³⁴⁵⁶⁷⁸⁹⁰–”' + '\xad' + 'á“ó½'
spec_chars = string.punctuation + '\n\xa0«»\t—…' + ' ' + '`' + "'" + '’' + '¹²³⁴⁵⁶⁷⁸⁹⁰–”' + '\xad' + 'á“ó½'
text_sp = text_transf(text, spec_chars_sp)
text_n_sp = text_transf(text, spec_chars)
results = collections.Counter(text_n_sp)
print(results)
results_sp = collections.Counter(text_sp)
print("With space: ", results_sp)
bigrams = [text_n_sp[i:i+2] for i in range(len(text_n_sp)-1)]
bigram_counts = collections.Counter(bigrams)
print(bigram_counts)
bigrams_sp = [text_sp[i:i+2] for i in range(len(text_sp)-1)]
bigram_sp_counts = collections.Counter(bigrams_sp)
print("With space: ", bigram_sp_counts)

csv_write('res.csv',results)
csv_write('res_sp.csv',results_sp)
csv_write('bigr_count.csv',bigram_counts)
csv_write('bigr_sp_count.csv',bigram_sp_counts)

res_count_d = dict(results)
bigr_count_d = dict(bigram_counts)
H_1 = count_Hn(1, res_count_d)
H_2 = count_Hn(2, bigr_count_d)
print("H1 ",H_1)
print("H2 ",H_2)

print("For case with space: ")

res_count_d_sp = dict(results_sp)
bigr_count_d_sp = dict(bigram_sp_counts)
H_1_sp = count_Hn(1, res_count_d_sp)
H_2_sp = count_Hn(2, bigr_count_d_sp)
print("H1 ",H_1_sp)
print("H2 ",H_2_sp)
print("Надлишковість")
print(count_R(H_1),"%")
print(count_R(H_2),"%")
print(count_R(H_1_sp),"%")
print(count_R(H_2_sp),"%")


