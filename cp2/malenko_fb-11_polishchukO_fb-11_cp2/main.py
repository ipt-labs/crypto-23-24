import random
from matplotlib import pyplot
from itertools import cycle

ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
LETTER_TO_INDEX = {letter: index for index, letter in enumerate(ALPHABET)}
SAMPLE_SIZE = 50

class Lab2Text:

    def __init__(self, text, clean=False):
        self.text = text
        if clean:
            self.text = self.__clean_text()

    def __clean_text(self):
        text = self.text.lower()
        text = ''.join([char for char in text if char in ALPHABET])
        return text

    def cipher(self, key=None):
        if not key:
            return Lab2CipherText(self.text)
        cipher = ''
        for textLetter, keyLetter in zip(self.text, cycle(key)):
            textLetterIndex = LETTER_TO_INDEX[textLetter]
            keyLetterIndex = LETTER_TO_INDEX[keyLetter]
            cipherLetterIndex = (textLetterIndex + keyLetterIndex) % len(ALPHABET)
            cipher += ALPHABET[cipherLetterIndex]
        return Lab2CipherText(cipher)

class Lab2CipherText:

    def __init__(self, text, clean=False):
        self.text = text
        if clean:
            self.text = self.__clean_text()

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.text)

    def __getitem__(self, item):
        return self.text[item]

    def __clean_text(self):
        text = self.text.lower()
        text = ''.join([char for char in text if char in ALPHABET])
        return text

    def calculate_coincidence_index(self):
        frequencies = {}
        for letter in self.text:
            if letter in frequencies:
                frequencies[letter] += 1
            else:
                frequencies[letter] = 1
        coincidenceIndex = sum(frequency * (frequency - 1) for frequency in frequencies.values()) / (len(self.text) * (len(self.text) - 1))
        return coincidenceIndex

    def approximate_key_length_by_index(self, maxLength=None):
        if not maxLength or maxLength > len(self.text):
            maxLength = len(self.text) // 3
        coincidences = {}
        for keyLength in range(1, maxLength + 1):
            sumCoincidences = 0
            for offset in range(0, keyLength):
                chunkText = ''.join([self.text[i] for i in range(offset, len(self.text) - keyLength + 1, keyLength)])
                chunk = Lab2CipherText(chunkText)
                coincidenceIndex = chunk.calculate_coincidence_index()
                sumCoincidences += coincidenceIndex
            averageCoincidence = sumCoincidences / keyLength
            coincidences.update({keyLength: averageCoincidence})
        return coincidences

    def approximate_key_length_by_coincidences(self, maxLength=None):
        if not maxLength or maxLength > len(self.text):
            maxLength = len(self.text)
        coincidences = {}
        for offset in range(1, maxLength + 1):
            coincidences[offset] = 0
            for letterIndex, letter in enumerate(self.text[:-offset]):
                if self.text[letterIndex + offset] == letter:
                    coincidences[offset] += 1
        return coincidences

    def get_letter_frequencies(self, key=None):
        if not key:
            return [{}]
        frequenciesList = []
        for letterIndex, letter in enumerate(key):
            frequencies = {}
            chunkText = ''.join([self.text[i] for i in range(letterIndex, len(self.text) - len(key) + 1, len(key))])
            for letter in chunkText:
                if letter in frequencies:
                    frequencies[letter] += 1
                else:
                    frequencies[letter] = 1
            frequenciesList.append(frequencies)
        return frequenciesList

    def decipher(self, key=None):
        if not key:
            return Lab2Text(self.text)
        deciphered = ''
        for textLetter, keyLetter in zip(self.text, cycle(key)):
            textLetterIndex = LETTER_TO_INDEX[textLetter]
            keyLetterIndex = LETTER_TO_INDEX[keyLetter]
            decipheredLetterIndex = (textLetterIndex - keyLetterIndex) % len(ALPHABET)
            deciphered += ALPHABET[decipheredLetterIndex]
        return Lab2CipherText(deciphered)

if __name__ == '__main__':
    with open('input.txt', 'r', encoding='utf8') as f:
        inputText = f.read()
    formattedText = Lab2Text(inputText, clean=True)

    coincidences = []
    for keyLength in range(1, SAMPLE_SIZE):
        key = ''.join([random.choice(ALPHABET) for letter in range(keyLength)])
        cipherText = formattedText.cipher(key=key)
        coincidenceIndex = cipherText.calculate_coincidence_index()
        coincidences.append(coincidenceIndex)

    pyplot.xlabel('Key length')
    pyplot.ylabel('Coincidence index')
    pyplot.plot(coincidences)
    pyplot.show()