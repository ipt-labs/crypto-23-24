from csv import writer
from math import log2

def ClearText(text):
    """Deletes all non-alphabetic or non-space
    characters from given string"""
    alphabet = " абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    text = " ".join("".join(filter(alphabet.__contains__,text)).split())
    return text

def ReadFile(filename):
    """Reads file from given filename or path
    Returns one string in lower case"""
    with open(filename, encoding = "utf-8", mode = "r") as file:
        text = file.read().lower()
    return text

def CountLetters(text,spaces = False):
    """Counts letters frequency in given string
    Calculate entropy and redundancy of given string
    spaces = True - include space into count
    Generates .csv file with results"""
    result = []
    total = 0
    entropy = 0
    csvfilename = "LettersWithSpace.csv"
    alphabet = " абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    if not spaces:
        alphabet = alphabet.replace(" ","")
        csvfilename = "OnlyLetters.csv"
    for char in alphabet:
        number = text.count(char)
        total += number
        result.append([char,number])
    for i in result:
        frequency = i[1]/total
        i.append(frequency)
        if frequency != 0:
            entropy += -1 * frequency * log2(frequency)
    redundancy = 1 - (entropy/log2(len(alphabet)))
    with open(csvfilename,"w",newline="") as file:
        csvwriter = writer(file)
        csvwriter.writerow(["Character","Number of characters","Frequency"])
        csvwriter.writerows(result)
        csvwriter.writerow(["Total",total])
        csvwriter.writerow(["Entropy",entropy])
        csvwriter.writerow(["Redundancy",redundancy])

def CountBigrams(text,spaces = False,crossing = False):
    """Counts bigram frequency in given string
    Calculate entropy and redundancy of given string
    spaces = True - include space into count
    crossing = True - allow bigrams to cross
    Generate .csv file with results"""
    alphabet_len = 34
    if not spaces:
        text = text.replace(" ","")
        alphabet_len = 33
    bigram_TempResult = {}
    bigram_result = []
    total = 0
    entropy = 0
    if not crossing:
        for i in range(1,len(text),2):
            bigram = text[i-1:i+1]
            if bigram in bigram_TempResult:
                bigram_TempResult[bigram] += 1
                total += 1
            else:
                bigram_TempResult[bigram] = 1
                total += 1
    else:
        for i in range(1,len(text)):
            bigram = text[i-1:i+1]
            if bigram in bigram_TempResult:
                bigram_TempResult[bigram] += 1
                total += 1
            else:
                bigram_TempResult[bigram] = 1
                total += 1
    for key,val in bigram_TempResult.items():
        bigram_result.append([key,val])
    for i in bigram_result:
        frequency = i[1]/total
        i.append(frequency)
        if frequency != 0:
            entropy += (-1 * frequency * log2(frequency))/2
    redundancy = 1 - (entropy/log2(alphabet_len))
    if spaces == False and crossing == False:
        csvfilename = "BigramsWithoutSpaceAndCrossing.csv"
    elif spaces == True and crossing == False:
        csvfilename = "BigramsWithSpace.csv"
    elif spaces == False and crossing == True:
        csvfilename = "BigramsWithCrossing.csv"
    else:
        csvfilename = "BigramsWithSpaceAndCrossing.csv"
    with open(csvfilename,"w",newline="") as file:
        csvwriter = writer(file)
        csvwriter.writerow(["Bigram","Number of bigrams","Frequency"])
        csvwriter.writerows(bigram_result)
        csvwriter.writerow(["Total",total])
        csvwriter.writerow(["Entropy",entropy])
        csvwriter.writerow(["Redundancy",redundancy])

if __name__ == "__main__":
    text = ReadFile("Prestuplenie-i-nakazanie.txt")
    text = ClearText(text)
    CountLetters(text)
    CountLetters(text ,True)
    CountBigrams(text,spaces=True,crossing=True)
    CountBigrams(text,crossing=True)
    CountBigrams(text,spaces=True)
    CountBigrams(text)