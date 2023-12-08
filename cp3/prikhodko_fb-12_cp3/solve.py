#!/usr/bin/python3
import random
import sys
sys.path.append('../../cp1/prikhodko_fb-12_cp1')
from entropy_assessment import freqCalc
CHARSET = ''.join([chr(char) for char in range(ord('а'),ord('я')+1,1) if char != ord('ъ')])
CHARSET = "абвгдежзийклмнопрстуфхцчшщьыэюя"
MOD = len(CHARSET)
BANNED = [i for i in "аь, еь, иь, оь, уь, ыь, ьь, эь, юь, яь, аы, еы, иы, оы, уы, ыы, эы, юы, яы".split(", ")]


def tests() -> None:
    """
    Function for POC
    """
    pt_ru = "Криптография это весело, правда?"
    ct = affineBigramEncrypt(1,2,pt_ru)
    pt_d = affineBigramDecrypt(1,2,ct)
    pt = parseText(pt_ru)
    if len(pt) % 2 != 0: pt += pt[-1]
    assert pt == pt_d


def xgcd(a:int,b:int) -> list:
    """
    Function extended GCD, used for finding unit in a ring
    input:
        a,b - integers for gcd(a,b)
    output:
        g   - gcd(a,b)
        x,y from x*a + y*b = g
    """
    if a == 0 : 
        return b,0,1
    g,xr,yr = xgcd(b%a, a) 
    x,y = yr - (b//a) * xr, xr
    return [g,x,y] 

def fermatPT(n:int, k:int) -> bool:
    """
    Function to test number for primality
    input:
        n   - number
        k   - number of iteration, aka "strength of test"
    output:
        1/0 - number is prime / number is composite
    """
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(k):
        a = random.randint(1, n-1)
        if pow(a, n-1) % n != 1:
            return False
    return True

def parseText(pt:str) -> str:
    """
    Function for text parsing, remove all characters that are not in CHARSET
    input:
        pt  - plain text 
    output:
        ptc - plain text cleared
    """
    ptc = ''.join([char for char in pt.lower() if char in CHARSET])
    if len(ptc) % 2 != 0: ptc += ptc[-1]
    return ptc

def parseBigrams(text:str) -> list:
    """
    Function to create bigrams of form x0*m + x1
    input:
        text    - text to parse 
    output:
        res     - list of bigrams
    """
    bigrams = [text[i:i+2] for i in range(0,len(text),2)]
    res = []
    for bg in bigrams:
        x0 = CHARSET.index(bg[0])
        x1 = CHARSET.index(bg[1])
        X = x0 * MOD + x1
        res += [X]
    return res

def getText(bigrams:list) -> str:
    """
    Function to convert list of bigrams in form x0*m + x1 to text 
    input:
        bigrams - list of bigrams 
    output:
        text    - created text
    """
    text = "" 
    for bg in bigrams:
        x1 = CHARSET[bg%MOD]
        x0 = CHARSET[bg//MOD]
        text += x0 + x1 
    return text

def affineBigramEncrypt(a:int,b:int,pt:str) -> str:
    """
    Basic function for text encryption using bigram version of Affine Cipher
    input:
        a,b - cipher key (a - factor, b - addend)
        pt  - plain text 
    output:
        ct  - cipher text
    """
    pt = parseText(pt)
    if len(pt) % 2 != 0: pt += pt[-1]
    bigrams_intConv = parseBigrams(pt)
    ct_intConv = [(bg*a + b)%MOD**2 for bg in bigrams_intConv]
    ct = getText(ct_intConv)
    return ct

def affineBigramDecrypt(a:int,b:int,ct:str) -> str:
    """
    Basic function for text decryption using bigram version of Affine Cipher
    input:
        a,b - cipher key (a - factor, b - addend)
        ct  - cipher text 
    output:
        pt  - plain text
    """
    _,a_inv,_ = xgcd(a,MOD**2)
    bigrams_intConv = parseBigrams(ct)
    pt_intConv = [((bg - b) * a_inv)%MOD**2 for bg in bigrams_intConv]
    pt = getText(pt_intConv)
    return pt

def getBannedBigrams(text:str) -> list:
    """
    Function for finding bigrams that cannot appear in text
    input:
        text    - big plain text, example
    output:
        banned  - list of banned bigrams
    """
    all_bg = set()
    for a in CHARSET:
        for b in CHARSET:
            all_bg.add(a+b)
    text_bg = set()
    for i in range(0,len(text),2):
        text_bg.add(text[i:i+2])
    banned = list(all_bg.difference(text_bg))
    return banned

def solveEq(x:list,y:list) -> list:
    """
    Function for solving system of Affine Cipher equations in field
    input:
        x,y - lists of 2 values for ct and pt
    output:
        key - a,b parameters of possible key
    """
    assert fermatPT(MOD,10)
    x0,x1 = x 
    y0,y1 = y 
    y_sub = (y0-y1)%MOD**2
    x_sub = (x0-x1)%MOD**2
    g,x_sub_inv,_ = xgcd(x_sub,MOD**2)
    a = (y_sub * x_sub_inv)%MOD**2
    b = (y0 - a*x0)%MOD**2
    return [a,b] 

def solveCongr(x:list,y:list) -> list:
    """
    Function for solving system of Affine Cipher equations in ring
    input:
        x,y - lists of 2 values for ct and pt
    output:
        key - a,b parameters of possible key
    """
    x0,x1 = x 
    y0,y1 = y 
    y_sub = (y0-y1)%MOD**2
    x_sub = (x0-x1)%MOD**2
    g,x_sub_inv,_ = xgcd(x_sub,MOD**2)
    if g == 1:
        a = (y_sub * x_sub_inv)%MOD**2
        b = (y0 - a*x0)%MOD**2
        return [[a,b]]
    elif y_sub % g != 0:
        return [None]
    else:
        y_sub //= g
        x_sub //= g
        mod = (MOD**2)//g
        _,x_sub_inv,_ = xgcd(x_sub,mod)
        a = (y_sub * x_sub_inv)%MOD**2
        res = []
        for i in range(g):
            tmpa = a + i*mod
            b = (y0 - tmpa*x0)%MOD**2
            res.append([tmpa,b])
        return res
    

def attack(ex:str,ct:str) -> list:
    """
    Function for cracking bigram Affine cipher based on freq analysis
    input:
        ex_text - example text for analysis, must be big
        ct      - cipher text 
    output:
        pt      - decrypted plain text
    """
    res = findKeys(ex,ct)
    pts = []
    for key in res:
        a,b = key
        pt = affineBigramDecrypt(a,b,ct)
        print("key for",pt[:10]+"...",[a,b])
        pts.append(pt)
    return pts

def getComb(c:list) -> list:
    """
    Function for creating all posible combinations of 2 different elements from list
    input:
        c       - list with elements
    output:
        result  - list of combinations
    """
    result = []
    n = len(c)
    for i in range(n):
        for j in range(i+1,n):
            if c[i] != c[j]:
                result.append([c[i],c[j]])
    return result

def checkText(text:str) -> bool:
    tmp = [text[i:i+2] for i in range(0,len(text),2)]
    for b in BANNED:
        if b in tmp:
            return False 
    return True

def findKeys(ex:str,ct:str) -> list:
    """
    Function for finding list of possible keys
    input:
        ex_text - example text for analysis, must be big
        ct      - cipher text 
    output:
        res     - list of possible keys
    """
    ex_freq = list(freqCalc(ex,2,2).keys())[::-1][:MAX_CHECK]
    ct_freq = list(freqCalc(ct,2,2).keys())[::-1][:MAX_CHECK]
    ex_p = parseBigrams("".join(ex_freq))
    ct_p = parseBigrams("".join(ct_freq))
    ex_c = getComb(ex_p)
    ct_c = getComb(ct_p)
    res = []
    for i in ex_c:
        for j in ct_c:
            a,b = solveEq(i,j)
            tmp = affineBigramDecrypt(a,b,ct)
            if checkText(tmp):
                if [a,b] not in res:
                    res.append([a,b])
    return res


def main() -> None:
    tests()
    global MAX_CHECK
    MAX_CHECK = 7
    # paths = ["text"]
    # ex_text = ""
    # for file in paths:
    #    with open(file) as f:
    #        ex_text += parseText(f.read())
    # print(getBannedBigrams(ex_text))
    ex_text = "еннатоност"
    with open("13.txt") as f:
        test_text = parseText(f.read())
    #print(freqCalc(test_text,2,2))
    pts = attack(ex_text,test_text)
    for pt in pts:
        print("|",pt)
if __name__ == "__main__":
    main()
