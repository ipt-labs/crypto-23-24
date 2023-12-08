from main import Lab2CipherText
from matplotlib import pyplot

if __name__ == '__main__':
    with open('task.txt', 'r', encoding='utf8') as f:
        inputText = Lab2CipherText(f.read())

    while True:
        maxLength = input('Enter the maximum key length to check for \x1B[3m(0 to check all possibilities, \'q\' to exit)\x1B[0m: ')
        if maxLength == 'q':
            exit(1)
        while True:
            if not maxLength.isdigit():
                maxLength = input('Invalid input! Please try again: ')
                continue
            break
        maxLength = int(maxLength)

        approximationByIndex = inputText.approximate_key_length_by_index(maxLength=maxLength)
        approximationByIndex = sorted(approximationByIndex.items(), key=lambda x: x[0])
        approximationByCoincidences = inputText.approximate_key_length_by_coincidences(maxLength=maxLength)
        approximationByCoincidences = sorted(approximationByCoincidences.items(), key=lambda x: x[0])

        figure, (plotLeft, plotRight) = pyplot.subplots(1, 2)
        plotLeft.set_title('Key length approximation by coincidence index')
        plotLeft.bar([coincidence[0] for coincidence in approximationByIndex], [coincidence[1] for coincidence in approximationByIndex])

        plotRight.set_title('Key length approximation by coincidences number')
        plotRight.bar([coincidence[0] for coincidence in approximationByCoincidences], [coincidence[1] for coincidence in approximationByCoincidences])
        pyplot.setp(plotLeft, xlabel='Key length', ylabel='Coincidence index')
        pyplot.setp(plotRight, xlabel='Key length', ylabel='Coincidences')
        pyplot.show()