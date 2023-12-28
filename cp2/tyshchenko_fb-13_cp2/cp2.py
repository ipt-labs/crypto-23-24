#!/usr/bin/python3

from collections import Counter
import sys

# Global variables
ALPHABET = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)
CHARS = {'о': 0.113, 'е': 0.085, 'а': 0.077, 'и': 0.069, 'н': 0.062, 'т': 0.06, 'с': 0.05, 'в': 0.046, 'л': 0.044, 'р': 0.042, 'к': 0.042, 'д': 0.031, 'у': 0.03, 'м': 0.03, 'п': 0.028, 'ь': 0.02, 'ы': 0.019, 'б': 0.019, 'я': 0.019, 'ч': 0.019, 'г': 0.017, 'з': 0.017, 'ж': 0.011, 'х': 0.01, 'ш': 0.01, 'й': 0.01, 'ю': 0.006, 'ц': 0.003, 'щ': 0.003, 'э': 0.002, 'ф': 0.001, 'ъ': 0.0}
KEYS = ["т", "да", "зло", "крах", "месть", "денацификация", "самоуничтожение", "сельскохозяйственный", "электрофотополупроводниковый"]

# Read n characters of file fname.
def read_file(fname: str) -> str:
    with open(fname, "r") as f:
        text = f.read()
    return text.strip()

# Calculate appearences of letters in text.
def count_letters(text: str) -> dict:
    return Counter(text)
    
# Calculate index of coincidence.
def ioc(text: str, pt=False) -> float:
    n = len(text)
    count = count_letters(text)
    ioc = 0
    if pt:
        for i in ALPHABET:
            ioc += CHARS[i] * n * (CHARS[i] * n - 1)
    else:
        for i in ALPHABET:
            ioc += count[i] * (count[i] - 1)
    return ioc / (n * (n - 1))
    
# Separate ciphered text into blocks.
def separate(text: str, period: int) -> list:
    blocks = [''] * period
    for i in range(len(text)):
        blocks[i % period] += text[i]
    return blocks

# Find period (key length).    
def find_period(text: str, show=False) -> list:
    period = 1
    acc = 0.005
    res = [0, 0]
    found = False
    if show:
        print("Period\tIoC")
    while period <= 30:
        blocks = separate(text, period)
        # Calculate union IoC for all blocks (algorithm 1).
        i = 0
        for b in blocks:
            i += ioc(b)
        i /= period
        # Visualize correlation between period and IoC values.
        if show:
            print(f"{period}\t{i}")
        if IOC_TH - i < acc and not found:
            res = [period, i]
            found = True
        period += 1
    # Case "period not found".
    if found:
        return res
    else:
        return [0, 0]
   
# Find key based on found period.    
def find_key(text: str, period: int) -> list:
    blocks = separate(text, period)
    # List of the most common letters in blocks.
    common = []
    for b in blocks:
        # Find and store the most common letter in b.
        letters = dict(sorted(count_letters(b).items(), reverse=True, key=lambda item: item[1]))
        common.append(encode(list(letters)[0]))
    # Create string of the most common russian letters.
    chars = "оеоооеооооооао"
    s = [encode(x) for x in chars]
    # Create key based on the most common letters of CT and russian.
    key = ''.join([decode(x-y) for x, y in zip(common, s)])
    return [key, chars]
    
# Swap letters with their corresponding numbers.
def encode(text: str):
    encoded = [ALPHABET.index(x) for x in text]
    if len(encoded) == 1:
        return encoded[0]
    else:
        return encoded

# Swap numbers with their corresponding letters.
def decode(nums) -> str:
    if isinstance(nums, int):
        return ALPHABET[nums]
    else:
        return ''.join([ALPHABET[x] for x in nums])
   
# Encrypt text with Vigenere cipher.
def encrypt(text: str, key: str) -> str:
    ct = encode(text)
    r = encode(key)
    if isinstance(r, list):
        sz = len(r)
        for i in range(len(text)):
            ct[i] = (ct[i] + r[i % sz]) % M
    else:
        for i in range(len(text)):
            ct[i] = (ct[i] + r) % M
    return decode(ct)

# Decrypt text encrypted with Vigenere cipher.  
def decrypt(text: str, key: str):
    pt = encode(text)
    r = encode(key)
    if isinstance(r, list):
        sz = len(r)
        for i in range(len(text)):
            pt[i] = (pt[i] - r[i % sz]) % M
    else:
        for i in range(len(text)):
            pt[i] = (pt[i] - r) % M
    return decode(pt)

# Support function for visualize.
def split_text(text: str, size=30) -> list:
    res = []
    i = 0
    n = len(text)
    while i < n:
        res.append(text[i:i+size])
        i += size
    return res
   
# Visualize encryption.
def visualize(text: str, key: str, act='e') -> None:
    ksize = len(key)
    parts = split_text(text)
    for p in parts:
        psize = len(p)
        if act == 'e':
            print(f"""M:\t{p}
r:\t{key * (psize//ksize) + key[:psize%ksize]}
C:\t{encrypt(p, key)}""")
        elif act == 'd':
            print(f"""C:\t{p}
r:\t{key * (psize//ksize) + key[:psize%ksize]}
M:\t{decrypt(p, key)}""")
        else:
            print("Incorrect act value. Choose between \'e\' and \'d\'")
            
def show_decryption(text: str, key: str) -> None:
    ksize = len(key)
    print(f"{key}\n{'-' * ksize}")
    parts = split_text(text, ksize)
    for p in parts:
        print(decrypt(p, key))

def solve(f1: str, f2: str) -> None:
    global IOC_TH
    # Read files.
    var = read_file(f1)
    custom = read_file(f2)
    '''
    Task 1. Processing custom text.
    - Calculate plaintext IoC.
    - Encrypt custom text with different keys.
    - Calculate ciphertext IoC and period (key length) in table.
    - Decrypt custom text.
    - Compare PT and CT IoCs.
    '''
    print(f"Custom text:\t{custom[:30]}...")
    IOC_TH = ioc(custom, pt=True)
    print(f"IoC:\t{IOC_TH}\n")
    for r in KEYS:
        print(f"Using key \"{r}\"\nEncrypting...")
        ct = encrypt(custom, r)
        visualize(custom[:30], r, "e")
        print("Searching period (key length)...")
        period, i = find_period(ct, show=True)
        print(f"Found:\n\tPeriod:\t{period}\n\tIoC:\t{i}\nDecrypting...")
        visualize(ct[:30], r, "d")
        print()
    '''
    Task 2. Decipher var3 text.
    - Find period (key length)
    - Find most the common characters blocks of CT.
    - Find key.
    - Get PT.
    '''
    print(f"Var3 text:\t{var[:30]}...")
    print("Searching period...")
    period, i = find_period(var, show=True)
    print(f"Found:\n\tPeriod:\t{period}\n\tIoC:\t{i}\nSearching key...")
    key, chars = find_key(var, period)
    print(f"Chars:\t{chars}\nKey:\t{key}\nDecrypting...")
    show_decryption(var[:period*5], key)
    #print(decrypt(var, key))

if __name__ == "__main__":
    num_args = len(sys.argv)
    if num_args < 3:
        print(f"""USAGE: {sys.argv[0]} VAR3FILE CUSTOMFILE
[*] VAR3FILE\t- path to var3 text file.
[*] CUSTOMFILE\t- path to file with custom plaintext.""")
    else:
        f1 = sys.argv[1]
        f2 = sys.argv[2]
        solve(f1, f2)
