#!/usr/bin/python3
from entropy_assessment import *

def findNext(freq:dict,char:str) -> list:
    results = []
    for key in freq.keys():
        if key[0] == char:
            results.append(key[1])
    results.reverse()
    return results
def main() -> None:
    with open(TEXT_FILENAME) as f:
        text_rus_clear = f.read().replace("\n"," ").lower()
    freq_bigram = freqCalc(parseText(text_rus_clear),2)
    char = input("> Enter char to find: ")
    while len(char) > 0:
        print(findNext(freq_bigram,char))
        char = input("> Enter char to find: ")

if __name__ == "__main__":
    main()
