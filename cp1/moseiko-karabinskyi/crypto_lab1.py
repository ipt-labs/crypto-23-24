def calculate_letter_frequencies(text):
    letter_frequencies = {}
    text = text.lower()
    for char in text:
        if char.isalpha():
            if char in letter_frequencies:
                letter_frequencies[char] += 1
            else:
                letter_frequencies[char] = 1  
    return letter_frequencies

def calculate_bigram_frequencies(text):
    bigram_frequencies = {}
    text = text.lower()
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram.isalpha():
            if bigram in bigram_frequencies:
                bigram_frequencies[bigram] += 1
            else:
                bigram_frequencies[bigram] = 1   
    return bigram_frequencies


