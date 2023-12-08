import openpyxl
import math

def calculate_frequencies(text, space = 0, cross_bigram = 0):
    if space:
        text = ''.join(filter(lambda char: (char.isalpha() and char >= 'а' and char <= 'я') or char.isspace(), text.lower()))
    else:
        text = ''.join(filter(lambda char: char.isalpha() and char >= 'а' and char <= 'я', text.lower()))
    letter_freq = {}
    for letter in text:
        if letter in letter_freq:
            letter_freq[letter] += 1
        else:
            letter_freq[letter] = 1

    if cross_bigram == 1:
        step = 1
    else:
        step = 2
    bigram_freq = {}
    for i in range(0, len(text) - 1, step):
        bigram = text[i:i+2]
        if bigram in bigram_freq:
            bigram_freq[bigram] += 1
        else:
            bigram_freq[bigram] = 1

    text_length = len(text)
    letter_freq = {letter: freq / text_length for letter, freq in letter_freq.items()}
    if cross_bigram:
        bigram_freq = {bigram: freq / (text_length - 1) for bigram, freq in bigram_freq.items()}
    else:
        bigram_freq = {bigram: freq / (text_length // 2) for bigram, freq in bigram_freq.items()}

    return letter_freq, bigram_freq

def calculate_entropy_let(freq):
    entropy = 0.0
    for probability in freq.values():
        entropy -= probability * math.log2(probability)
    return entropy

def calculate_entropy_bigr(freq):
    entropy = 0.0
    for probability in freq.values():
        if probability > 0:
            entropy -= probability * math.log2(probability)
    return entropy / 2
    
def calculate_redundancy(entropy, space):
    if space:
        return 1 - (entropy / math.log2(32))
    else:
        return 1 - (entropy / math.log2(31))

def xlsx_save(filename, letters = 1, bigrams = 1):
    wb = openpyxl.Workbook()
    ws = wb.active
    if letters:
        for letter, freq in letter_freq.items():
            ws.append([letter, freq])
    if bigrams:
        for bigram, freq in bigram_freq.items():
            ws.append([bigram, freq])

    wb.save(f'C:/Users/artem/Desktop/КРИПТА/{filename}.xlsx')


with open('C:/Users/artem/Desktop/КРИПТА/text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

print('Letters and not cross bigrams without space:')
letter_freq, bigram_freq = calculate_frequencies(text, 0, 0)
xlsx_save('letters_not_cross_bigr_without_space')
print(f'Letters entropy: {calculate_entropy_let(letter_freq)}')
print(f'Bigrams entropy: {calculate_entropy_bigr(bigram_freq)}')
print(f'Letter redundancy: {calculate_redundancy(calculate_entropy_let(letter_freq), 0)}')
print(f'Bigrams redundancy: {calculate_redundancy(calculate_entropy_bigr(bigram_freq), 0)}\n')

print('Letters and not cross bigrams with space:')
letter_freq, bigram_freq = calculate_frequencies(text, 1, 0)
xlsx_save('letters_not_cross_bigr_with_space')
print(f'Letters entropy: {calculate_entropy_let(letter_freq)}')
print(f'Bigrams entropy: {calculate_entropy_bigr(bigram_freq)}')
print(f'Letter redundancy: {calculate_redundancy(calculate_entropy_let(letter_freq), 1)}')
print(f'Bigrams redundancy: {calculate_redundancy(calculate_entropy_bigr(bigram_freq), 1)}\n')

print('Cross bigrams with space:')
letter_freq, bigram_freq = calculate_frequencies(text, 1, 1)
xlsx_save('Cross_bigr_with_space', 0)
print(f'Bigrams entropy: {calculate_entropy_bigr(bigram_freq)}')
print(f'Bigrams redundancy: {calculate_redundancy(calculate_entropy_bigr(bigram_freq), 1)}\n')

print('Cross bigrams without space:')
letter_freq, bigram_freq = calculate_frequencies(text, 0, 1)
xlsx_save('Cross_bigr_without_space', 0)
print(f'Bigrams entropy: {calculate_entropy_bigr(bigram_freq)}')
print(f'Bigrams redundancy: {calculate_redundancy(calculate_entropy_bigr(bigram_freq), 0)}\n')
