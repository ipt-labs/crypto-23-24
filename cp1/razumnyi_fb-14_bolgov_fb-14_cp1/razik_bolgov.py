import math
import re
import pandas as pd
import os

allowed_letters = 'абвгдежзийклмнопрстуфхцчшщыьэюя '


def filtered(text_to_filter, spaces=True):
    """ Make the text lower-case
        Replace ё with e, Ъ with ь
        Replace non-russian symbols with a single space
        Replace any spaces, tabs, newlines etc with a single space
        Specify whether to remove spaces-only completely """

    if not spaces:
        text_to_filter = re.sub(' ', '', text_to_filter)
        return text_to_filter

    text_to_filter = text_to_filter.lower()
    text_to_filter = text_to_filter.replace('ё', 'е').replace('ъ', 'ь')
    text_to_filter = re.sub('[^а-я]', ' ', text_to_filter)
    text_to_filter = re.sub(r'\s+', ' ', text_to_filter)

    return text_to_filter


def letter_frequency(text_to_freq, spaces=True):
    """ Count the frequencies of letters and find entropy and redundancy """

    global allowed_letters

    if not spaces:
        alph = allowed_letters[:-1]
    else:
        alph = allowed_letters

    letter_freq_dict = {}

    for i in alph:
        letter_freq_dict[i] = text_to_freq.count(i)

    for i in letter_freq_dict:
        letter_freq_dict[i] = letter_freq_dict[i] / len(text_to_freq)

    d = {k: v for k, v in sorted(letter_freq_dict.items(), key=lambda item: item[1], reverse=True)}

    ########## A piece of code to create a txt file and append the found frequencies
    # if not os.path.exists('letters.txt'):
    #     f = open('letters.txt', 'w')
    #     f.close()

    # with open('letters.txt', 'a', encoding='utf8') as f:
    #     if spaces:
    #         f.write('Letter frequencies in the text with spaces\n\n')
    #     else:
    #         f.write('Letter frequencies in the text without spaces\n\n')
    #     for i in d:
    #         f.write(f' "{i}"   |   {d[i]}\n')
    #     f.write('\n\n')
    ##########

    if spaces:
        print('Letter frequencies in the text with spaces\n')
    else:
        print('Letter frequencies in the text without spaces\n')
    for i in d:
        print(f' "{i}"   |   {d[i]}')
    print('')

    entropy_h1 = 0
    for i in letter_freq_dict.values():
        entropy_h1 += -i * math.log2(i)

    print("Entropy is: ")
    print(f"H.1 = {entropy_h1}")

    print("Redundancy is: ")
    if spaces:
        print(f"R.1 = {1 - (entropy_h1 / math.log2(32))}\n\n")
    else:
        print(f"R.1 = {1 - (entropy_h1 / math.log2(31))}\n\n")


def bigram_frequency(text_to_freq, cross=True, spaces=True):
    """ Count the frequency of bigrams and find entropy and redundancy """

    global allowed_letters
    bigram_freq_dict = {}

    if cross:
        mass = []
        for i in range(0, len(text_to_freq)):
            bigram = text_to_freq[i:i + 2]
            mass.append(bigram)
        mass_unique = []
        [mass_unique.append(i) for i in mass if i not in mass_unique]
    else:
        mass = []
        for i in range(0, len(text_to_freq), 2):
            bigram = text_to_freq[i:i + 2]
            mass.append(bigram)
        mass_unique = []
        [mass_unique.append(x) for x in mass if x not in mass_unique]

    for i in mass_unique:
        bigram_freq_dict[i] = mass.count(i)

    for i in bigram_freq_dict:
        bigram_freq_dict[i] = round(bigram_freq_dict[i] / len(mass), 10)

    if not spaces:
        alphabet = list(allowed_letters[:-1])
    else:
        alphabet = list(allowed_letters)

    df = pd.DataFrame(columns=alphabet, index=alphabet)

    for bigram, freq in bigram_freq_dict.items():
        if len(bigram) == 2:
            df.loc[bigram[0], bigram[1]] = freq

    df.fillna(0, inplace=True)

    ########## Optional to display table in terminal
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)
    # print(df)

    file_name = "bigram_table"
    if cross:
        file_name += "_cross"
    elif not cross:
        file_name += "_not_cross"
    if spaces:
        file_name += "_spaces"
    elif not spaces:
        file_name += "_not_spaces"

    file_name += ".xlsx"
    df.to_excel(file_name)
    print(f'To see the entire table, please refer to *{file_name}* or uncomment code to show in the terminal')

    entropy_h2 = 0
    for i in bigram_freq_dict.values():
        entropy_h2 += -i * math.log2(i)

    print("Entropy is: ")
    entropy_h2 = entropy_h2 / 2
    print(f"H.2 = {entropy_h2}")

    print("Redundancy is: ")
    if spaces:
        print(f"R.2 = {1 - (entropy_h2 / math.log2(32))}\n\n")
    else:
        print(f"R.2 = {1 - (entropy_h2 / math.log2(31))}\n\n")


if __name__ == '__main__':

    # Open the file and filter the text with spaces
    with open('ds.txt', 'r', encoding='utf8') as f1:
        f1_read = filtered(f1.read())

    # Find letter frequencies in text with spaces
    letter_frequency(f1_read)

    # Find crossed bigram frequencies in text with spaces
    bigram_frequency(f1_read)

    # Find non-crossed frequencies in text with spaces
    bigram_frequency(f1_read, cross=False)

    #
    # Remove spaces in the filtered text
    f2_read = filtered(f1_read, spaces=False)

    # Find letter frequencies in text without spaces
    letter_frequency(f2_read, spaces=False)

    # Find crossed bigram frequencies in text without spaces
    bigram_frequency(f2_read, spaces=False)

    # Find non-crossed bigram frequencies in text without spaces
    bigram_frequency(f2_read, spaces=False, cross=False)

