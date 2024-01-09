import collections
from math import gcd, log
from itertools import combinations
import numpy as np

def GetBigrams(Filename, Alphabet, Step=False):
    File = open(Filename, "r")
    RawText = File.read().lower()
    RawText = RawText.replace('ё','е')
    RawText = RawText.replace('ъ','ь')

    TextList = [i for i in RawText if i in Alphabet]
    if Step == False:
        BigramsCount = len(list(zip(TextList,TextList[1:])))
        Bigrams = collections.Counter(zip(TextList,TextList[1:]))
    else:
        BigramsCount = len(list(zip(TextList,TextList[2:])))
        Bigrams = collections.Counter(zip(TextList,TextList[2:]))


    ReportFile = open("BigramProb.txt", "w")
    for i in Bigrams.keys():
        Bigrams[i] = Bigrams[i]/BigramsCount

    return Bigrams

def get_bigrams(filename, alphabet, from_file=True):
    if from_file:
        file = open(filename, "r")
        raw = file.read().lower()
    else:
        raw = filename.lower()

    raw = raw.replace('ё','е')
    raw = raw.replace('ъ','ь')
    raw = [i for i in raw if i in alphabet]
    raw = ''.join(raw)
    raw_list = [raw[i:i+2] for i in range(0, len(raw), 2)]
    return collections.Counter(raw_list)


def find_reversed(a, b, n):
    d = gcd(a, n)
    if d == 1:
        return [ (pow(a, -1, n) * b) % n]

    if b%d:
        return []

    a1 = a / d
    b1 = b / d
    n1 = n / d
    ret = []
    a1_rev = pow(int(a1), -1, int(n1))
    x0 = (b1 * a1_rev)%n1
    for i in range(d):
        ret.append( (x0 + n1*i) )
    return ret

def from_bigram_to_value(bigram, alphabet):
    m = len(alphabet)
    return alphabet.index(bigram[0])*m + alphabet.index(bigram[1])

def from_value_to_bigram(value, alphabet):
    m = len(alphabet)
    x1 = value//m
    x2 = value%m
    x1 = alphabet[int(x1)]
    x2 = alphabet[int(x2)]
    return x1+x2


def shannon(string):
    counts = collections.Counter(string)
    frequencies = ((i / len(string)) for i in counts.values())
    return - sum(f * log(f, 2) for f in frequencies)


def get_a(x_bigrams, y_bigrams, alphabet):

    m2 = pow(len(alphabet), 2)
    y1 = from_bigram_to_value(y_bigrams[0], alphabet)
    y2 = from_bigram_to_value(y_bigrams[1], alphabet)
    x1 = from_bigram_to_value(x_bigrams[0], alphabet)
    x2 = from_bigram_to_value(x_bigrams[1], alphabet)
    a = find_reversed( (x1 - x2)%m2, (y1 - y2)%m2, m2)
    return a


def get_b(y, x, a_list, alphabet):
    b = []
    m2 = pow(len(alphabet), 2)
    for a in a_list:
        b.append( find_reversed(1, (y - x * a)%m2, m2))
    return b


def enc_bigram(bigram, a, b, alphabet):
    m2 = pow(len(alphabet), 2)
    return from_value_to_bigram( (from_bigram_to_value(bigram, alphabet) * a + b) % m2, alphabet)

def dec_bigram(bigram, a_rev, b, alphabet):
    m2 = pow(len(alphabet), 2)
    return from_value_to_bigram( (a_rev * (from_bigram_to_value(bigram, alphabet) - b)) % m2, alphabet)


def affine_bigram_dec_text(raw, a, b, alphabet):
     text = [raw[i:i+2] for i in range(0, len(raw), 2)]
     dec_text = []
     for i in text:
         dec_text.append(dec_bigram(i, a, b, alphabet))
     dec_text = "".join(dec_text)
     return dec_text

def affine_bigram_enc_text(raw, a, b, alphabet):
    text = [raw[i:i+2] for i in range(0, len(raw), 2)]
    dec_text = []
    for i in text:
        dec_text.append(enc_bigram(i, a, b, alphabet))
    dec_text = "".join(dec_text)
    return dec_text


def affine_bigram_enc(filename, a, b, alphabet):
    with open(filename, 'r') as file:
        text = file.read()
    raw = text.lower()
    raw = raw.replace('ё','е')
    raw = raw.replace('ъ','ь')
    raw = [i for i in raw if i in alphabet]
    raw = ''.join(raw)
    raw = [raw[i:i+2] for i in range(0, len(raw), 2)]
    res = []
    for i in raw:
        res.append(enc_bigram(i, a, b, alphabet))
    "".join(res)
    return res

def affine_bigram_dec(filename, alphabet, good_bigrams):
    with open(filename, 'r') as file:
        raw = file.read().lower()
    raw = raw.replace('ё','е')
    raw = raw.replace('ъ','ь')
    raw = [i for i in raw if i in alphabet]
    raw = ''.join(raw)

    m2 = pow(len(alphabet), 2)
    ideal_entropy = 4.35
    new_bigram = get_bigrams(filename, alphabet)
    new_bigram = dict(sorted(new_bigram.items(), key=lambda x: x[1], reverse=True)[:10]).keys()
    new_bigram_combinations = list(combinations(new_bigram, 2))
    good_bigram_combinations = list(combinations(good_bigrams, 2))
    used_pairs = []
    for possible_enc_pair in new_bigram_combinations:
        for possible_dec_pair in good_bigram_combinations:
            possible_a = find_reversed( from_bigram_to_value(possible_dec_pair[0], alphabet) - from_bigram_to_value(possible_dec_pair[1], alphabet), from_bigram_to_value(possible_enc_pair[0], alphabet) - from_bigram_to_value(possible_enc_pair[1], alphabet), m2)
            if len(possible_a) == 0:
                pass
            for a in possible_a:
                b = (from_bigram_to_value(possible_enc_pair[0], alphabet) - from_bigram_to_value(possible_dec_pair[0], alphabet) * a)%m2
                for i in find_reversed(int(a), 1, m2):
                    dec_text = affine_bigram_dec_text(raw, i, b, alphabet)
                    if (a, b) in used_pairs:
                        continue
                    used_pairs.append((a, b))


                    if   ideal_entropy - 0.1 <= shannon(dec_text) <= ideal_entropy + 0.1:
                        print("possible solution: a = {}, b = {}".format(a, b))
                        print(dec_text[:50])

    return

def main():

    
    alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',  'ь', 'ы', 'э', 'ю', 'я', ]
    bigr = get_bigrams("karam.txt", alphabet)
    print(bigr.most_common(5))
    good_bigrams = ['то', 'ен', 'но', 'ст', 'на']
#    good_bigrams = ['то', 'ен', 'но', 'ст', 'на', 'ка', 'ко']
#    affine_bigram_dec("test_v15.txt", alphabet, good_bigrams)
#    with open("cleartext.txt", 'r') as file:
#        raw = file.read().lower()
#    raw = raw.replace('ё','е')
#    raw = raw.replace('ъ','ь')
#    raw = [i for i in raw if i in alphabet]
#    raw = ''.join(raw)

#    enc_raw = affine_bigram_enc_text(raw, 67, 23, alphabet)
#    with open("cleartext_enc.txt", 'w') as file:
#        file.write(enc_raw)
#    print(affine_bigram_dec_text(enc_raw, 643, 3, alphabet ))
    with open("v15.txt", "r") as file:
        print("cyphertext: ", file.read()[:0x30])
    affine_bigram_dec("v15.txt", alphabet, good_bigrams)









if __name__ == '__main__':
    main()
