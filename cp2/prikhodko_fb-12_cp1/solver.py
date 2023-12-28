#!/usr/bin/python3
from random import choice
from kasisky import *
from save import *

PLAINTEXT_FILE = 'text'
CIPHERTEXT_FILE = 'ct'
REQ_LEN = 3
KEY_LEN = [2,3,4,5]+[i for i in range(10,21,1)]
e_,a_,q_ = "[!]","[*]","[?]"
RUS_ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
OFFSET = ord(RUS_ALPHABET[0])
I0 = 1 / len(RUS_ALPHABET)
FREQ_MONO = 'оеанитсвлркмдпуяьчгзыбжйшхюэщцфъ' #taken from results of analysis in lab1

def clearText(text:str) -> str:
    text_ = list(text)
    permitted = RUS_ALPHABET
    result = [char for char in text_ if char in permitted]
    return ''.join(result)

def vigenereEncrypt(pt:str, key:str) -> str:
    n = len(RUS_ALPHABET)
    d,r = len(pt)//len(key), len(pt)%len(key)
    keystream = d*key + key[:r]
    ct = ""
    for t,k in zip(pt,keystream):
        t = ord(t) - OFFSET
        k = ord(k) - OFFSET 
        ct += chr(((t + k) % n) + OFFSET) 
    return ct

def vigenereDecrypt(ct:str, key:str) -> str:
    n = len(RUS_ALPHABET)
    d,r = len(ct)//len(key), len(ct)%len(key)
    keystream = d*key + key[:r]
    pt = ""
    for c,k in zip(ct,keystream):
        c = ord(c) - OFFSET
        k = ord(k) - OFFSET
        pt += chr(((c - k) % n) + OFFSET)
    return pt

def calcIndex(text:str):
    n = len(text)
    apdx = (n * (n - 1))
    N = calcFreqChar
    s = sum([N(text,t)*(N(text,t) - 1) for t in RUS_ALPHABET])
    I = s / apdx 
    return I

def calcFreqChar(text:str,char:str) -> int:
    return text.count(char)

def calcFreq(text:str,ch_len:int=1,step:int=1) -> dict:
    frequencies = {}
    text_len = len(text)
    for pos in range(0,text_len-ch_len+1,step):
        ch = text[pos:pos+ch_len]
        frequencies[ch] = frequencies.get(ch, 0) + 1
    frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1]))
    return list(frequencies.keys())[::-1]

def getCaesarKey(text:str):
    freq = calcFreq(text)
    keys = []
    for i in range(len(freq)):
        a = ord(FREQ_MONO[i]) - OFFSET
        b = ord(freq[i]) - OFFSET
        tmp = b - a
        keys.append(tmp%len(RUS_ALPHABET)) 
    return  keys

def genkey(keys:list) -> str:
    res = []
    for i in keys:
        res.append(i[0])
    res = ''.join([chr(i+OFFSET) for i in res])
    return res

def main() -> None:
    with open(PLAINTEXT_FILE) as f:
        pt = f.read()
    with open(CIPHERTEXT_FILE) as f:
        ct = f.read()
    ct = clearText(ct)
    print(f"{a_} Length of file is {len(pt)//1000} kb, while required length is {REQ_LEN} kb")
    pt = clearText(pt)[:REQ_LEN*1000]
    if input(f"{q_} Redacted to required length, show text? [y/N] ").lower() == 'y':
        print(pt)
    print(f"{a_} Generating keys of length: " +', '.join([str(i) for i in KEY_LEN]))
    keys = []
    for l in KEY_LEN:
        key = ''.join(choice(RUS_ALPHABET) for _ in range(l))
        keys.append(key)
    if input(f"{q_} Show keys? [Y/n] ").lower() != 'n':
        print(keys)
    print(f"{a_} Encrypting plaintext for each key...")
    ctd = {}
    for key in keys:
        ctd[key] = vigenereEncrypt(pt,key)
    pt_i = calcIndex(pt)
    print(f"{e_} Coincidence index for plaintext is {pt_i}")
    print(f"{e_} For ciphertexts with length of key N:")
    indexes = {}
    for key in ctd:
        print("{:2s}".format(str(len(key))),end=" | ")
        tmp_i = calcIndex(ctd[key])
        print(tmp_i)
        indexes[ctd[key]] = tmp_i
    ct_i = calcIndex(ct)
    print(f"{a_} For task ciphertext: {ct_i}")
    print("|")
    print(f"{a_} Splitting for key range 1-30")
    results = []
    for l in range(1,31):
        parts = ['']*l 
        for i in range(0,len(ct),l):
            for c,elem in enumerate(ct[i:i+l]):
                parts[c] += elem
        tmp = []
        for part in parts:
            tmp.append(calcIndex(part))
        results.append(sum(tmp)/len(tmp))
    for i in range(len(results)):
        print(i+1,'|',results[i])
    keylen = 0
    sub = 10
    for c,i in enumerate(results):
        tmp = pt_i - i
        if sub > tmp:
            sub = tmp
            keylen = c+1
    print(f"{e_} Key length by result of 'Index of coincidence' analysis: {keylen}")
    kasisky_keylen = kasiskyExamination(ct)
    print(f"{e_} Kasisky examination result, key length: {kasisky_keylen}")
    
    poskey = findKey(ct)
    if poskey:
        if input(f"{e_} Found saved key for this ciphertext, use it to decrypt? [Y/n] ").lower() == 'n':
            pass 
        else:
            print(f"{e_} Decrypted text with key {poskey}:")
            print(vigenereDecrypt(ct,poskey))
            exit()


    parts = ['']*keylen
    for i in range(0,len(ct),keylen):
        for c,elem in enumerate(ct[i:i+keylen]):
            parts[c] += elem
    keychars = []
    for c,i in enumerate(parts):
        pos_chars = getCaesarKey(i)
        pos_chars_d = {}
        for i in pos_chars:
            pos_chars_d[pos_chars.count(i)] = i
        pos_chars = list(dict(sorted(pos_chars_d.items(), reverse=True)).values())
        keychars.append(pos_chars)
    poskey = genkey(keychars)
    print(f"{e_} The most likely key is {poskey}")
    print(f"Decrypted plaintext example:")
    print(vigenereDecrypt(ct,poskey)[:100])
    if input(f"{q_} Do you want to change any letters of the key? [y/N] ").lower() == 'y':
        print(f"{a_} Write only positional index of number to change using results of analysis, 'number letter' to change manually or leave blank to exit")
        inp = input("> ")
        while inp:
            try:
                args = inp.split(" ")
                if len(args) == 1:
                    ind = int(args[0])
                    if len(keychars[ind]) != 1:
                        keychars[ind].pop(0)
                    poskey = genkey(keychars)
                elif len(args) == 2:
                    ind = int(args[0])
                    c = args[1]
                    poskey = list(poskey)
                    poskey[ind] = c
                    poskey = ''.join(poskey)
                print(poskey,vigenereDecrypt(ct,poskey)[:100])
                inp = input("> ")
            except:
                print('Invalid index')
                inp = input("> ")
                continue

    print(f"{e_} Decrypted text with key {poskey}:")
    print(vigenereDecrypt(ct,poskey))
    if input(f"{q_} Save this key for this ciphertext? [y/N] ").lower() == 'y':
        save(ct,poskey)

if __name__ == "__main__":
    main()

