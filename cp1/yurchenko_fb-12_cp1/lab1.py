import re
from math import log2

Alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def clear(f):
    full = list(f)
    start_with = [i for i in full if i in Alph+' ']
    finish = [i for i in full if i in Alph]
    finish_with = [i for i in re.sub(r'\s+', ' ',''.join(start_with))]
    return finish, finish_with

def count_ch_freq(lst):
    char_freq = {}
    for char in lst:
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1
    return char_freq

def count_bigr_freq(lst, step=1):
    string = ''.join(lst)
    bigr_freq = {}
    for i in range(0, len(lst)-1, step):
        bigr = string[i:i+2]
        if bigr in bigr_freq:
            bigr_freq[bigr] += 1
        else:
            bigr_freq[bigr] = 1
    return bigr_freq

def cal_H(freq):
    entr = 0.0
    total = sum(freq.values())
    for val in freq.values():
        q = val/total
        entr -= q*log2(q)
    return entr

def cal_R(entr, len=34):
    R = 1-(entr/log2(len))
    return R

def print_table(freq):
    hor = '-'*38
    print(hor)
    print("|  Символ  |  Кількість  |  Частота  |")
    print(hor)
    total = sum(freq.values())
    for char, val in sorted(freq.items(), key=lambda i: i[1], reverse=True):
        q = val/total
        print(f"|{char:^10}|{val:^13}| {q:.7f} |")
    print(hor)

with open("text1.txt", encoding="utf-8") as f:
    text = f.read().lower()

finish, finish_with = clear(text)
print("Частота букв у тексті:")
print_table(count_ch_freq(finish_with))
print("\n")
print("Частота біграм у тексті з перетинами:")
print_table(count_bigr_freq(finish_with))
print("\n")
print("Частота біграм у тексті без перетинів:")
print_table(count_bigr_freq(finish_with, 2))
print("\n")
print("H1 з пробілами: ", cal_H(count_ch_freq(finish_with)))
print("H1 без пробілів: ", cal_H(count_ch_freq(finish)))
print("H2 з пробілами та перетинами: ", 0.5*cal_H(count_bigr_freq(finish_with)))
print("H2 з пробілами та без перетинів: ", 0.5*cal_H(count_bigr_freq(finish_with, 2)))
print("H2 без пробілів та з перетинами: ", 0.5*cal_H(count_bigr_freq(finish)))
print("H2 без пробілів та перетинів: ", 0.5*cal_H(count_bigr_freq(finish, 2)),"\n")
print("R для букв з пробілами: ", cal_R(cal_H(count_ch_freq(finish_with))))
print("R для букв без пробілів: ", cal_R(cal_H(count_ch_freq(finish)),33))
print("R для біграм з пробілами та перетинами: ", cal_R(0.5*cal_H(count_bigr_freq(finish_with))))
print("R для біграм з пробілами та без перетинів: ", cal_R(0.5*cal_H(count_bigr_freq(finish_with, 2))))
print("R для біграм без пробілів та з перетинами: ", cal_R(0.5*cal_H(count_bigr_freq(finish)), 33))
print("R для біграм без пробілів та перетинів: ", cal_R(0.5*cal_H(count_bigr_freq(finish, 2)), 33))
