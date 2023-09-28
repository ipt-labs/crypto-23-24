import re
import numpy
import pandas
import openpyxl

ALPHABET = "йцукенгшщзхфывапролджэячсмитьбю "
TRANSFORMS = {x: x for x in ALPHABET} | {'ё': 'е', 'ъ': 'ь'}
H0 = numpy.log2(len(ALPHABET))


def prettifier(text, with_spaces=True):
    text = re.findall(r'[а-яА-Я]+', text)
    if with_spaces:
        text = ' '.join(text)
    else:
        text = ''.join(text)
    return text.lower()


def get_frequency(text):
    frequency = {x: 0 for x in ALPHABET}

    for letter in text:
        frequency[TRANSFORMS[letter]] += 1
    return frequency


def get_bigram_frequency(text, without_intersection=True):
    frequency = {x: {y: 0 for y in ALPHABET} for x in ALPHABET}
    step = int(without_intersection)+1

    for idx, letter in enumerate(text[:-1:step]):
        frequency[TRANSFORMS[letter]][TRANSFORMS[text[idx*step+1]]] += 1

    return frequency


def calc_h1(frequency):
    frequency_array = [x for x in frequency.values()]
    probabilities = numpy.divide(frequency_array, numpy.sum(frequency_array))
    probabilities = probabilities[probabilities != 0]
    h1 = -numpy.dot(probabilities, numpy.log2(probabilities))
    return h1


def calc_h2(bigram_frequency):
    frequency_array = [x for y in bigram_frequency.values() for x in y.values() ]
    probabilities = numpy.divide(frequency_array, numpy.sum(frequency_array))
    probabilities = probabilities[probabilities != 0]
    h2 = -numpy.dot(probabilities, numpy.log2(probabilities)) * 0.5
    return h2


def stringify_frequency(frequency):
    ans = ""
    for k,v in frequency.items():
        if type(v) == dict:
            for k2,v2 in v.items():
                ans += f"'{k}{k2}' : {v2} \n"
        else:
            ans += f"'{k}' : {v} \n"

    return ans

def parse_b_frequency(b_frequency):
    f = {}
    for k, v in b_frequency.items():
            for k2, v2 in v.items():
                f[f'{k}{k2}']= v2

    return f


with open('text1.txt', 'r', encoding='UTF-8') as file:
    raw = file.read()
    for x in range(2):
        with_spaces = bool(x)
        text = prettifier(raw, with_spaces)
        frequency = get_frequency(text)
        h1 = calc_h1(frequency)
        df = pandas.DataFrame(data=frequency, index=[0])
        df =df.T
        df["H1"] = h1
        df["R1"] = 1-h1/H0
        df.to_excel(f'1-gram Spaces={with_spaces}.xlsx', header=f"1-gram Spaces={with_spaces}")

        for y in range(2):
            without_intersection = bool(y)
            bigram_frequency = get_bigram_frequency(text, without_intersection)
            h2 = calc_h2(bigram_frequency)
            df = pandas.DataFrame(data=parse_b_frequency(bigram_frequency), index=[0])
            df = df.T
            df["H2"] = h2
            df["R2"] = 1 - h2 / H0
            df.to_excel(f'2-gram Spaces={with_spaces} Intersection={not without_intersection}.xlsx', header=f"2-gram Spaces={with_spaces} Intersection={not without_intersection}")




