#!/usr/bin/python3
from pprint import pp 
import string
from math import log2
from decimal import *

e_,a_,q_ = "[!]","[*]","[?]"
TEXT_FILENAME = 'text2'
RUS_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
getcontext().prec = 100

def clearText(text:str) -> str:
    text_ = list(text)
    permitted = RUS_ALPHABET
    result = [char for char in text_ if char in permitted]
    return ''.join(result)

def parseText(text:str) -> str:
    text_ = list(text)
    permitted = RUS_ALPHABET + ' ' #+ string.punctuation + string.digits 
    result = [char for char in text_ if char in permitted]
    return ''.join(result)

def printFreq(freq:dict) -> None:
    res_str = " ".join(["| {}:{:.12f}".format(item,freq[item]) for item in freq.keys()]) + " |"
    res_str = "".join([char + "\n" if (c + 1) % ((res_str.find(".")+14) * 5) == 0 else char for c,char in enumerate(res_str)])
    print(res_str)

def printMatrix(freq:dict) -> None:
    ALPH = list(set([char[0] for char in freq.keys()] + [char[1] for char in freq.keys()]))
    ALPH.sort()
    start_row = [' '] + ['  '+i+'  ' for i in list(ALPH)]
    rows = [[i]+[' '*5]*len(ALPH) for i in ALPH]
    rows = [start_row] + rows
    for cross in freq:
        a = ALPH.index(cross[0]) + 1 
        b = ALPH.index(cross[1]) + 1
        v = freq[cross]
        rows[a][b] = "{:.3f}".format(v*100)
    for row in rows:
        print(' | '.join(row))

def freqCalc(text:str,ch_len:int=1,step:int=1) -> dict:
    frequencies = {}
    text_len = len(text)
    for pos in range(0,text_len-ch_len+1,step):
        ch = text[pos:pos+ch_len]
        frequencies[ch] = frequencies.get(ch, 0) + 1
    frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1]))
    sm_elems = sum(frequencies.values())
    for item in frequencies: frequencies[item] = Decimal.from_float(frequencies[item] / sm_elems)
    return frequencies

def getEntropy(freq:dict) -> Decimal:
    entropy = Decimal(0.0)
    for f in freq.values(): entropy -= f * Decimal.from_float(log2(f))
    return entropy / len(list(freq.keys())[0])

def getRedundancy(h:Decimal,alphabet:list=RUS_ALPHABET) -> Decimal:
    h0 = Decimal(log2(len(alphabet)))
    r = Decimal(1 - (h / h0))
    return r



def main() -> None:
    with open(TEXT_FILENAME) as f:
        text_rus_clear = f.read().replace("\n"," ").lower()

    print(f"{a_} Counting the frequency for characters one by one...")
    freq_single = freqCalc(parseText(text_rus_clear))
    print(f"{e_} Frequency for each char:")
    printFreq(freq_single)
    entr1 = getEntropy(freq_single)
    print(f"{e_} Entropy H1: {entr1}")
    print(f"{e_} Redundancy R1: {getRedundancy(entr1,RUS_ALPHABET+' ')}")
    print(f"|\n{a_} Same text without spaces and special chars...")
    freq_single_WoSpaces = freqCalc(clearText(text_rus_clear))
    printFreq(freq_single_WoSpaces)
    entr1_ = getEntropy(freq_single_WoSpaces)
    print(f"{e_} H1 w/o spaces: {entr1_}")
    print(f"{e_} R1 w/o spaces: {getRedundancy(entr1_)}")


    
    #bigram_alphabet = [i+j for i in RUS_ALPHABET for j in RUS_ALPHABET]
    #works fine if we skip division by 2 for H2 entropy, and work with bigram alphabet without RUS_ALPHABET when defining R2

    print(f"|\n{a_} Counting frequency for bigrams with overlay...")
    freq_bigram = freqCalc(parseText(text_rus_clear),2)
    print(f"{e_} Frequency for bigrams:")
    if input("> Show bigram frequencies table? [y/n] ").lower() == "y": printFreq(freq_bigram)
    entr2 = getEntropy(freq_bigram)
    print(f"{e_} Entropy H2: {entr2}")
    print(f"{e_} Redundancy R2: {getRedundancy(entr2, RUS_ALPHABET+' ')}")
    freq_wOL = freqCalc(parseText(text_rus_clear),2,2)
    entr2_wOL = getEntropy(freq_wOL)
    print(f"{e_} Entropy H2` for text without overlapping: {entr2_wOL}")
    print(f"{e_} Redundancy H2` for text without overlapping: {getRedundancy(entr2_wOL, RUS_ALPHABET+' ')}")

    print(f"|\n{a_} Counting frequency for bigrams without spaces...")
    freq_bigram_WoSpaces = freqCalc(clearText(text_rus_clear),2)
    print(f"{e_} Frequency for bigrams:")
    if input("> Show bigram frequencies table? [y/n] ").lower() == "y": printFreq(freq_bigram_WoSpaces)
    entr2_ = getEntropy(freq_bigram_WoSpaces)
    print(f"{e_} H2 w/o spaces: {entr2_}")
    print(f"{e_} R2 w/o spaces: {getRedundancy(entr2_)}")
    freq_wOL_WoSpaces = freqCalc(clearText(text_rus_clear),2,2)
    entr2_wOL_WoSpaces = getEntropy(freq_wOL_WoSpaces)
    print(f"{e_} H2` w/o spaces, w/o overpalling: {entr2_wOL_WoSpaces}")
    print(f"{e_} R2` w/o spaces, w/o overlapping: {getRedundancy(entr2_wOL_WoSpaces)}")


    if input("> Show bigram frequencies matrix? [y/n] ").lower() == "y": printMatrix(freq_bigram_WoSpaces)
    

if __name__ == "__main__":
    main()
