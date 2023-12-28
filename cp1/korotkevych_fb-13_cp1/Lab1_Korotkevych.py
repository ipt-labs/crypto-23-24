import math
from collections import defaultdict

def count_letters(text):
    
    letter_count = 0
    letter_pair = defaultdict(float)

    for c in text:
        letter_pair[c] += 1
        letter_count += 1

    for key, value in letter_pair.items():
        letter_pair[key] /= letter_count

    return letter_pair

def count_bigram(text):
    bigram_count = 0
    bigram_pair = defaultdict(float)

    for i in range(len(text) - 1):
        bigram = text[i:i + 2]
        bigram_pair[bigram] += 1
        bigram_count += 1

    for key, value in bigram_pair.items():
        bigram_pair[key] /= bigram_count

    return dict(bigram_pair)

def count_bigram_2(text):
    bigram_count = 0
    bigram_pair = defaultdict(float)

    for i in range(0, len(text) - 1, 2):
        non_overlapping_bigram = text[i:i + 2]
        bigram_pair[non_overlapping_bigram] += 1
        bigram_count += 1

    for key, value in bigram_pair.items():
        bigram_pair[key] /= bigram_count

    return dict(bigram_pair)

def letter_entropy(pair):
    entropy = 0.0
    for value in pair.values():
        entropy -= value * math.log2(value)

    return entropy

def bigram_entropy(pair):
    entropy = 0.0
    for value in pair.values():
        entropy -= value * math.log2(value)

    return entropy/2

with open("/home/kali/Desktop/cryptolab1/scripts2_with_no_space.txt", "r") as file_input, open("/home/kali/Desktop/cryptolab1/outputfile.txt", "w") as file_output:
    text = "abcdef"

    for line in file_input:
        text2 = line.lower()

    letters = count_letters(text2)
    bigrams = count_bigram(text2)
    bigrams_with_step = count_bigram_2(text2)

    for key, value in letters.items():
        file_output.write("\n")
        file_output.write(f"{key}:{value}")

    for key, value in bigrams.items():
        file_output.write("\n")
        file_output.write(f"{key}:{value}")

    for key, value in bigrams_with_step.items():
        file_output.write("\n")
        file_output.write(f"{key}:{value}")


    file_output.write(f"\nLetter entropy: {letter_entropy(letters)}")
    file_output.write(f"\nBigram entropy: {bigram_entropy(bigrams)}")
    file_output.write(f"\nBigram entropy with step 2: {bigram_entropy(bigrams_with_step)}")