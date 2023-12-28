import re
import math
import collections 

SYMBOLS = ' абвгдежзийклмнопрстуфхцчшщыьэюя'



def file_read(filename):
    with open(filename, "r", encoding='utf-8') as f:
        text = f.read().lower()
    return text


text = file_read('Mertvye_dushi.txt')

def text_for_lab(text, space):
    text = text.lower()
    text = text.replace('ё', 'е').replace('ъ', 'ь')
    if space:
        text = re.sub(r'[^а-я ]', '', text)
    if not space:
        text = re.sub(r'[^а-я]', '', text)
    return text


text_no_spaces = text_for_lab(text, False)
text_spaces = text_for_lab(text, True)

def monogram(text, space=True):
    if space:
        monogram_frequency = {}
        for i in SYMBOLS:
            monogram_frequency[i] = text.count(i)
        for i in monogram_frequency:
            monogram_frequency[i] = monogram_frequency[i] / len(text)
    if not space:
        monogram_frequency = {}
        for i in SYMBOLS[1:]:
            monogram_frequency[i] = text.count(i)
        for i in monogram_frequency:
            monogram_frequency[i] = monogram_frequency[i] / len(text)
    
    return monogram_frequency


def write_file(filename, dictionary):
    with open(filename, 'w', encoding='utf-8') as f:
        for key, value in dictionary.items():
            f.write(f'{key} ~ {value}\n')


def bigram(dictionary, intersections):
    bigram_frequency = {}
    if intersections:
        bigram_list = [dictionary[i:i + 2] for i in range(len(dictionary))] 
        
    if not intersections:
        bigram_list = [dictionary[i:i + 2] for i in range(0, len(dictionary), 2)]
    
    bigram_unique_list = list(set(bigram_list))
    count_b = collections.Counter(bigram_list)
    for i in bigram_unique_list:
        bigram_frequency[i] = round(count_b[i] / len(bigram_list), 10)

    return bigram_frequency


def entropy_hn(dictionary, n):
    entropy_h = 0
    for i in dictionary.keys():
        entropy_h -= dictionary[i] * math.log2(dictionary[i])
    return entropy_h / n


def redundancy(entropy, space):
    if space:
        redundancy_r = 1 - (entropy / math.log2(32))
    else:
        redundancy_r = 1 - (entropy / math.log2(31))
    return redundancy_r


print('*** Ентропія монограми без пробілів ***')
print(entropy_hn(monogram(text_no_spaces, False), 1))
print()
print('*** Ентропія монограми з пробілами ***')
print(entropy_hn(monogram(text_spaces, True), 1))
print()
print('*** Надлишковість монограми без пробілів ***')
print(redundancy(entropy_hn(monogram(text_no_spaces, False), 1), False))
print()
print('*** Надлишковість монограми з пробілами ***')
print(redundancy(entropy_hn(monogram(text_spaces, True), 1), True))

print()
print('*** Ентропія біграми без пробілів з перетином ***')
print(entropy_hn(bigram(text_no_spaces, True), 2))
print()
print('*** Ентропія біграми без пробілів без перетину ***')
print(entropy_hn(bigram(text_no_spaces, False), 2)) 
print()
print('*** Надлишковість біграми без пробілів з перетином ***')
print(redundancy(entropy_hn(bigram(text_no_spaces, True), 2), False))
print()
print('*** Надлишковість біграми без пробілів без перетину ***')
print(redundancy(entropy_hn(bigram(text_no_spaces, False), 2), False))

print()
print('*** Ентропія біграми з пробілами з перетином ***')
print(entropy_hn(bigram(text_spaces, True), 2))
print()
print('*** Ентропія біграми з пробілами без перетину ***')
print(entropy_hn(bigram(text_spaces, False), 2))
print()
print('*** Надлишковість біграми з пробілами з перетином ***')
print(redundancy(entropy_hn(bigram(text_spaces, True), 2), True))
print()
print('*** Надлишковість біграми з пробілами без перетину ***')
print(redundancy(entropy_hn(bigram(text_spaces, False), 2), True))

write_file('monogram_no_spaces.txt', monogram(text_no_spaces, False))
write_file('monogram_spaces.txt', monogram(text_spaces, True))

write_file('bigram_no_spaces_no_intersections.txt', bigram(text_no_spaces, False))
write_file('bigram_spaces_no_intersections.txt', bigram(text_spaces, False))
write_file('bigram_no_spaces_intersections.txt', bigram(text_no_spaces, True))
write_file('bigram_spaces_intersections.txt', bigram(text_spaces, True))

