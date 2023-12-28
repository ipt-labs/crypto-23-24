import math
from openpyxl import Workbook

with open('filtered.txt', 'r', encoding='utf-8') as file:
    text = file.read()

with open('filtered_no_space.txt', 'r', encoding='utf-8') as file2:
    text_no_space = file2.read()

total_no_space = len(text_no_space)
total = len(text)

def letter_count(text):
    dictt = {}
    for charr in text:
        if charr in dictt:
            dictt[charr] += 1
        else:
            dictt[charr] = 1
    return dictt

def bigram_count(text, step):
    bigrams = [text[i]+text[i+1] for i in range(0, len(text) - 1, step)]
    total = len(bigrams)
    dictt = {}
    for bigram in bigrams:
        if bigram in dictt:
            dictt[bigram] += 1
        else:
            dictt[bigram] = 1
    
    return dictt, total

def find_h1(dictt, total, space = True):
    h1 = 0
    for key in dictt.keys():
        p = dictt[key] / total
        h1 += p*math.log(p, 2)
    h1 = -h1
    if space:
        N = 1 - h1/math.log(32, 2)
    else:
        N = 1 - h1/math.log(31, 2)
    return h1, N

def find_h2(dictt, total, space = True):
    h2 = 0
    for key in dictt.keys():
        p = dictt[key] / total
        h2 += p*math.log(p, 2)
    h2 = -h2/2
    if space:
        N = 1 - h2/math.log(32, 2)
    else:
        N = 1 - h2/math.log(31, 2)
    return h2, N

def bigrams_to_file(text, text_no_space):
    cases=["cross_space", "no_cross_space", "cross_no_space", "no_cross_no_space"]
    for n in range(4):
        if n < 2:
            txt = text
        else:
            txt = text_no_space
        if n % 2 == 0:
            step = 1
        else:
            step = 2
        dictt, total = bigram_count(txt, step)
        if n == 0:
            a = 'w'
        else:
            a = 'a'
        with open("Bigram_probability.txt", a, encoding='utf-8') as file:
            file.write(f'{cases[n]}\n')
            for bigram, count in dictt.items():
                frequency = count / total
                file.write(f'{bigram}: {count}, {frequency}\n')

def letters_to_file(dictt, total, total_no_space):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Character Count'
    sheet['A1'] = 'Символ'
    sheet['B1'] = 'кількість'
    sheet['C1'] = 'Частота з пробілами'
    sheet['D1'] = 'Частота без пробілів'
    row = 2
    for letter, count in dictt.items():
        sheet[f'A{row}'] = letter
        sheet[f'B{row}'] = count
        sheet[f'C{row}'] = count / total
        if letter != " ":
            sheet[f'D{row}'] = count / total_no_space
        row += 1
    workbook.save('character_count.xlsx')

letters_to_file(letter_count(text), total, total_no_space)
bigrams_to_file(text, text_no_space)

print("H1, R with space:", find_h1(letter_count(text), total))
print("H1, R without space:", find_h1(letter_count(text_no_space), total_no_space, False))
print("H2, R with space with cross:", find_h2(*bigram_count(text, 1)))
print("H2, R with space without cross:", find_h2(*bigram_count(text, 2)))
print("H2, R without space with cross:", find_h2(*bigram_count(text_no_space, 1), False))
print("H2, R without space without cross:", find_h2(*bigram_count(text_no_space, 2), False))
