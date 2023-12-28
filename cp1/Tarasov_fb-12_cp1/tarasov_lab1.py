import re
import math
import collections

#prepare text
file = "text.txt"
with open(file, "r", encoding="utf-8") as file:
    text = file.read().replace(' ', '_')
text = text.lower()
text = text.replace('-', '_')
text = re.sub(r'\n+', '_', text)
text = re.sub(r'_+', '_', text)

def text_without_spaces(text):
    return text.replace('_', '')
text_without_spaces = text_without_spaces(text)

def get_chars(text):
    length = 0
    chars = set()
    for char in text:
        chars.add(char)
    return chars

def count_chars(text, chars):
    counter = collections.Counter(text)
    counter = dict(sorted(counter.items(), key=lambda x: x[1], reverse=True))
    return counter

def count_freq_chars(tupple, all):
    freqs = []
    for key, value in tupple.items():
        print(key, ": Amount:", value, "[+] Frequency:", round(value/all, 6))
        freqs.append(value/all)
	    #print("Entropy:", count_entropy(length, freqs, amount))
    return freqs

#def count_freq_bgrams()

def count_entropy(n, freqs, amount):
    entropy = 0
    for i in range (0, n):
        #print(freqs[i])
        entropy +=  (-1) * (freqs[i] * math.log2(freqs[i]))
    print("\nEntropy:", entropy/amount, "\n")
    print("\n[+]"+"-"*40+"[+]\n")
    return entropy/amount


def bgram_freq(text, n):
    bgrams = collections.Counter((text[i:i+2]) for i in range(0, len(text)-1, n))
    total_count = sum(bgrams.values())
    freqs = {}
    for key, value in bgrams.items():
        freqs[key] = value
    freqs = dict(sorted(freqs.items(), key=lambda x: x[1], reverse=True))
    #print(total_count, freqs)
    return total_count, freqs


count_entropy(34, count_freq_chars(count_chars(text, get_chars(text)), len(text)), 1)
count_entropy(33, count_freq_chars(count_chars(text_without_spaces, get_chars(text)), len(text_without_spaces)), 1)

#CROSSED BIGRAMS
count_entropy(len(bgram_freq(text, 1)[1]), count_freq_chars(bgram_freq(text, 1)[1], bgram_freq(text, 1)[0]), 2) 
count_entropy(len(bgram_freq(text_without_spaces, 1)[1]), count_freq_chars(bgram_freq(text_without_spaces, 1)[1], bgram_freq(text_without_spaces, 1)[0]), 2)

#NON-CROSSED BIGRAMS
count_entropy(len(bgram_freq(text, 2)[1]), count_freq_chars(bgram_freq(text, 2)[1], bgram_freq(text, 2)[0]), 2)
count_entropy(len(bgram_freq(text_without_spaces, 2)[1]), count_freq_chars(bgram_freq(text_without_spaces, 2)[1], bgram_freq(text_without_spaces, 2)[0]), 2)