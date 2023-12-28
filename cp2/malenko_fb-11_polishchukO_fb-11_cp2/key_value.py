from main import Lab2CipherText, ALPHABET
from math import ceil, sqrt
from matplotlib import pyplot

if __name__ == '__main__':
    with open('task.txt', 'r', encoding='utf8') as f:
        inputText = Lab2CipherText(f.read())

    while True:
        keyLength = input('Enter the key length to check for letter frequencies \x1B[3m(\'q\' to exit)\x1B[0m: ')
        if keyLength == 'q':
            exit(1)
        while True:
            if not keyLength.isdigit():
                keyLength = input('Invalid input! Please try again: ')
                continue
            break
        keyLength = int(keyLength)

        frequenciesList = inputText.get_letter_frequencies(key='*'*keyLength)
        canvasSize = ceil(sqrt(len(frequenciesList)))
        figure, axis = pyplot.subplots(canvasSize, canvasSize)

        xCoordinate = 0
        yCoordinate = 0
        topLetters = ''
        for frequencies in frequenciesList:
            frequenciesSorted = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
            topLetters += frequenciesSorted[0][0]
            xAxisData = [frequency[0] for frequency in frequenciesSorted]
            yAxisData = [frequency[1] for frequency in frequenciesSorted]
            axis[xCoordinate, yCoordinate].bar(xAxisData, yAxisData)
            yCoordinate += 1
            if yCoordinate >= canvasSize:
                xCoordinate += 1
                yCoordinate = 0

        result = ''.join([ALPHABET[(ALPHABET.find(letter)-ALPHABET.find('е')) % (len(ALPHABET))] for letter in topLetters])
        print(f'The most likely key of length {keyLength} - "{result}"')
        pyplot.show()