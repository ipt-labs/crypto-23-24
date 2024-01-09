import re
from collections import Counter
import pandas as pd
import math


def clearing_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        original = infile.read()

    edited = re.sub(r'[^а-яА-Я\s\n]', '', original)
    edited = edited.replace("\n", " ").replace("ъ", "ь").replace("ё", "е")
    edited = re.sub(" +", " ", edited)
    edited = edited.lower()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(edited)


def clearing_spaces(input_file, output_file):
    with_spaces = open(input_file, 'r', encoding='utf-8').read()
    without_spaces = with_spaces.replace(" ", "")
    open(output_file, 'w', encoding='utf-8').write(without_spaces)


alphabet_spaces = {'а', 'б', 'в', 'г', 'д', 'е', 'ж',
                   'з', 'и', 'й', 'к', 'л', 'м', 'н',
                   'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                   'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь',
                   'э', 'ю', 'я', ' '}

alphabet_no_spaces = {'а', 'б', 'в', 'г', 'д', 'е', 'ж',
                      'з', 'и', 'й', 'к', 'л', 'м', 'н',
                      'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                      'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'ь',
                      'э', 'ю', 'я'}


def monograms_freq(the_text):
    with open(the_text, 'r', encoding='utf-8') as file:
        text = file.read()

    all_letters = len(text)
    frequency_dict = dict()

    if " " in text:
        alph = alphabet_spaces
    else:
        alph = alphabet_no_spaces

    for letter in alph:
        count = text.count(letter)
        frequency = round(count / all_letters, 4)
        frequency_dict[letter] = frequency

    full_entropy = 0
    entropy_list = []

    for value in frequency_dict.keys():
        entropy = -(frequency_dict[value] * math.log2(frequency_dict[value]))
        full_entropy += -(frequency_dict[value] * math.log2(frequency_dict[value]))
        entropy_list.append(entropy)

    r = 1 - (full_entropy / math.log2(len(alph)))

    mdf = pd.DataFrame(list(frequency_dict.items()), columns=['Monogram', 'Frequency'])
    mdf = mdf.sort_values(by='Frequency', ascending=False)
    mdf['Entropy'] = entropy_list

    if " " in text:
        mdf.to_excel(writer, sheet_name='MonoSpaces', index=False)
        ws = writer.sheets['MonoSpaces']
    else:
        mdf.to_excel(writer, sheet_name='MonoNoSpaces', index=False)
        ws = writer.sheets['MonoNoSpaces']

    ws['D1'] = 'Full entropy'
    ws['D2'] = full_entropy
    ws['E1'] = 'R'
    ws['E2'] = r


def bigram_cross_freq(the_text):
    with open(the_text, 'r', encoding='utf-8') as file:
        text = file.read()

    all_b = len(text)
    bigrams = []

    for i in range(all_b):
        bigram = text[i:i+2]
        if len(bigram) == 2:
            bigrams.append(bigram)

    bigram_dict = Counter(bigrams)

    full_entropy = 0
    entropy_list = []

    for j in bigram_dict.keys():
        bigram_dict[j] = round(bigram_dict[j] / all_b, 6)
        entropy = -(bigram_dict[j] * math.log2(bigram_dict[j]))
        full_entropy += -((bigram_dict[j] * math.log2(bigram_dict[j]))/2)
        entropy_list.append(entropy)

    df = pd.DataFrame(list(bigram_dict.items()), columns=['Bigram', 'Frequency'])
    df = df.sort_values(by='Frequency', ascending=False)
    df['Entropy'] = entropy_list

    if " " in text:
        df.to_excel(writer, sheet_name='BigramCrossSpaces', index=False)
        ws = writer.sheets['BigramCrossSpaces']
        r = 1 - (full_entropy / math.log2(len(alphabet_spaces)))
    else:
        df.to_excel(writer, sheet_name='BigramCrossNoSpaces', index=False)
        ws = writer.sheets['BigramCrossNoSpaces']
        r = 1 - (full_entropy / math.log2(len(alphabet_no_spaces)))

    ws['D1'] = 'Full entropy'
    ws['D2'] = full_entropy
    ws['E1'] = 'R'
    ws['E2'] = r


def bigram_uncross_freq(the_text):
    with open(the_text, 'r', encoding='utf-8') as file:
        text = file.read()

    all_b = len(text)
    bigrams = []

    for i in range(0, all_b, 2):
        bigram = text[i:i+2]
        if len(bigram) == 2:
            bigrams.append(bigram)

    bigram_dict = Counter(bigrams)

    big_sum = 0
    for value in bigram_dict.values():
        big_sum += value

    full_entropy = 0
    entropy_list = []

    for j in bigram_dict.keys():
        bigram_dict[j] = round(bigram_dict[j] / big_sum, 6)
        entropy = -(bigram_dict[j] * math.log2(bigram_dict[j]))
        full_entropy += -((bigram_dict[j] * math.log2(bigram_dict[j])) / 2)
        entropy_list.append(entropy)

    df2 = pd.DataFrame(list(bigram_dict.items()), columns=['Bigram', 'Frequency'])
    df2 = df2.sort_values(by='Frequency', ascending=False)
    df2['Entropy'] = entropy_list

    if " " in text:
        df2.to_excel(writer, sheet_name='BigramUncrossSpaces', index=False)
        ws = writer.sheets['BigramUncrossSpaces']
        r = 1 - (full_entropy / math.log2(len(alphabet_spaces)))
    else:
        df2.to_excel(writer, sheet_name='BigramUncrossNoSpaces', index=False)
        ws = writer.sheets['BigramUncrossNoSpaces']
        r = 1 - (full_entropy / math.log2(len(alphabet_no_spaces)))

    ws['D1'] = 'Full entropy'
    ws['D2'] = full_entropy
    ws['E1'] = 'R'
    ws['E2'] = r


clearing_text('gonegirl.txt', 'edited.txt')
clearing_spaces('edited.txt', 'edited_no_spaces.txt')

with pd.ExcelWriter('output_file.xlsx', engine='openpyxl') as writer:
    monograms_freq('edited.txt')
    monograms_freq('edited_no_spaces.txt')
    bigram_cross_freq('edited.txt')
    bigram_cross_freq('edited_no_spaces.txt')
    bigram_uncross_freq('edited.txt')
    bigram_uncross_freq('edited_no_spaces.txt')
