from linear import euclid, linear
from matplotlib import pyplot

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
SAMPLE_SIZE = 10
BIGRAMS_FREQUENCY_OPEN_TEXT = {'ст': 0.01811,
                               'ни': 0.01727,
                               'то': 0.01631,
                               'пр': 0.01376,
                               'ос': 0.01336,
                               'ра': 0.01295,
                               'но': 0.01255,
                               'ко': 0.01168,
                               'по': 0.01102,
                               'ен': 0.01075}
IMPOSSIBLE_BIGRAMS = ['аы', 'оы', 'иы', 'ыы', 'уы', 'еы', 'аь', 'оь', 'иь', 'ыь', 'уь', 'еь', 'юы', 'яы', 'эы', 'юь', 'яь', 'эь', 'ць', 'хь', 'кь']

class Lab3Text:

    def __init__(self, text, clean=False):
        self.text = text
        if clean:
            self.text = self.__clean_text()

    def __clean_text(self):
        text = self.text.lower()
        text = ''.join([char for char in text if char in ALPHABET])
        return text

    def get_frequencies(self, length, distance=1):
        frequencies = {}
        ngrams_count = 0
        for i in range(0, len(self.text)-length+1, distance):
            ngram = self.text[i:i+length]
            ngrams_count += 1
            if ngram in frequencies:
                frequencies[ngram] += 1
            else:
                frequencies[ngram] = 1
        normalized_frequencies = {ngram: frequency/ngrams_count for ngram, frequency in frequencies.items()}
        return normalized_frequencies

    def decipher(self, a=None, b=None):
        if a is None or b is None:
            return self.text
        decypheredText = ''
        for i in range(0, len(self.text)-1, 2):
            y = get_bigram_id(self.text[i:i+2])
            x = (euclid(a, len(ALPHABET)**2)[1] * (y - b)) % (len(ALPHABET)**2)
            decypheredText += ALPHABET[x // len(ALPHABET)] + ALPHABET[x % len(ALPHABET)]
        return decypheredText

def addlabels(x, y, color):
    for i in range(len(x)):
        pyplot.text(i, y[i], y[i], ha='center', color=color)

def get_bigram_id(bigram):
    return ALPHABET.index(bigram[0]) * len(ALPHABET) + ALPHABET.index(bigram[1])

def generate_key(bigram1, bigram2):
    x1, y1 = get_bigram_id(bigram1[0]), get_bigram_id(bigram1[1])
    x2, y2 = get_bigram_id(bigram2[0]), get_bigram_id(bigram2[1])
    roots = linear(x1 - x2, y1 - y2, len(ALPHABET)**2)
    if not roots:
        return
    keys = []
    for root in roots:
        a = root
        b = (y1 - a * x1) % (len(ALPHABET)**2)
        keys.append((a,b))
    return keys

def generate_keys(open_bigrams, cyphered_bigrams):
    pairs = []
    for openBigram in open_bigrams:
        for cypheredBigram in cyphered_bigrams:
            pairs.append((openBigram, cypheredBigram))
    keys = []
    test = []
    for i in pairs:
        for j in pairs:
            if i == j or i[1] == j[1]:
                continue
            test.append((i, j))
            roots = generate_key(i, j)
            if roots:
                for root in roots:
                    keys.append(root)
    return set(keys)

if __name__ == '__main__':
    with open('input.txt', 'r', encoding='utf8') as f:
        inputText = f.read()
    formattedText = Lab3Text(inputText)
    frequencies = formattedText.get_frequencies(2, distance=2)

    frequenciesLists = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)[:SAMPLE_SIZE]
    frequenciesKeys, frequenciesValues = zip(*frequenciesLists)
    frequenciesValues = [round(value, 5) for value in frequenciesValues]
    openTextList = sorted(BIGRAMS_FREQUENCY_OPEN_TEXT.items(), key=lambda x: x[1], reverse=True)[:SAMPLE_SIZE]
    openTextKeys, openTextValues = zip(*openTextList)

    ax1 = pyplot.subplot(1, 1, 1)
    ax1.set_xlabel('Bigram (Cyphered text)', color='Blue')
    ax1.set_ylabel('Frequency')
    ax1.tick_params(axis='x', color='Blue')
    ax1.bar(frequenciesKeys, frequenciesValues, color='Blue')
    addlabels(frequenciesKeys, frequenciesValues, 'Blue')

    ax2 = ax1.twiny()
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.spines['bottom'].set_position(('outward', 36))
    ax2.set_xlabel('Bigram (Open text)', color='Orange')
    ax2.tick_params(axis='x', color='Orange')
    ax2.bar(openTextKeys, openTextValues, edgecolor='Orange', fill=False)
    addlabels(openTextKeys, openTextValues, 'Orange')

    pyplot.show()

    possibleKeys = generate_keys(openTextKeys, frequenciesKeys)
    for a1, b1 in possibleKeys:
        decypheredText = formattedText.decipher(a=a1, b=b1)
        if all(impossibleBigram not in decypheredText for impossibleBigram in IMPOSSIBLE_BIGRAMS):
            print(f'Found possible solution: a = {a1}, b = {b1}, decypheredText = {decypheredText[:100]}...')
