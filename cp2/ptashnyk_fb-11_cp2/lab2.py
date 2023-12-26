from csv import reader,writer
from math import inf

def ReadFile(filename):
    with open(filename, encoding = "utf-8", mode = "r") as file:
        text = file.read().lower()
    return text

def ClearText(text,alphabet):
    text = "".join(filter(alphabet.__contains__,text))
    return text

def VigenereEncrypt(text,key,alphabet):
    keyCharIndex = 0
    encryptedText = ""
    for char in text:
        encryptedCharIndex = (alphabet.find(char) + alphabet.find(key[keyCharIndex])) % len(alphabet)
        keyCharIndex = (keyCharIndex + 1) % len(key)
        encryptedText += alphabet[encryptedCharIndex]
    return encryptedText

def SplitTextIntoBlocks(text,numberOfBlocks = 0,numberOfChars = 0):
    blocks = []
    if numberOfBlocks:
        for i in range(0,numberOfBlocks):
            blocks.append(text[i::numberOfBlocks])
    elif numberOfChars:
        for i in range(0,len(text),numberOfChars):
            blocks.append(text[i:i + numberOfChars])
    return blocks

def CountLettersEntries(text,alphabet):
    entries = {}
    for char in alphabet:
        number = text.count(char)
        entries.update({char:number})
    return entries

def ConformityIndex(text,alphabet):
    entries = CountLettersEntries(text,alphabet)
    conformityIndex = 0
    entriesSum = 0
    for char in alphabet:
            entriesSum += entries.get(char) * (entries.get(char) - 1)
    conformityIndex = entriesSum / (len(text) * (len(text) - 1))
    return conformityIndex

def BlocksConformityIndex(blocks,alphabet):
    index = 0
    for block in blocks:
        index += ConformityIndex(block,alphabet)
    return index / len(blocks)

def TheoreticalConformityIndex(filename):
    with open(filename) as file:
        data = list(reader(file,delimiter=","))
    data = data[1:-3]
    theoreticalConformityIndex = 0
    for letterData in data:
        theoreticalConformityIndex += float(letterData[2]) ** 2
    return theoreticalConformityIndex

def GenerateCSV(filename,data,header):
    with open(f"{filename}.csv", "w", newline = "") as file:
        csvwriter = writer(file)
        csvwriter.writerow(header)
        csvwriter.writerows(data)

def DecryptionIndex(textToDecrypt,alphabet):
    decryptionIndex = []
    for r in range(2,31):
        blocks = SplitTextIntoBlocks(textToDecrypt,numberOfBlocks = r)
        decryptionIndex.append([r,BlocksConformityIndex(blocks,alphabet)])
    return decryptionIndex

def FindPossibleKeys(decryptionIndex,fileWithData):
    possibleKeys = []
    Keys = []
    theoreticalIndex = TheoreticalConformityIndex(fileWithData)
    for i in decryptionIndex:
        if abs(theoreticalIndex - i[1]) <= 0.01:
            possibleKeys.append(i[0])
    for i in range(0,len(possibleKeys)):
        for j in range(i + 1,len(possibleKeys)):
            if (possibleKeys[j] % possibleKeys[i] == 0) and (possibleKeys[i] not in Keys):
                Keys.append(possibleKeys[i])
    return Keys

def BlocksOfCeasar(encryptedText,key):
    blocksOfCeasar = []
    block = ''
    blocks = SplitTextIntoBlocks(encryptedText,numberOfChars = key)
    for i in range(0,key):
        for j in blocks:
            block += j[i]
        blocksOfCeasar.append(block)
        block = ''
    return blocksOfCeasar

def CeasarDecrypt(text, key, alphabet):
    decrypted = ''
    for char in text:
        decrypted += alphabet[(alphabet.find(char) - key) % len(alphabet)]
    return decrypted

def CompareCeasarKeys(text, keys, alphabet):
    letterFrequency = {'а':0.07966000154221213, 'б':0.017389034871788788, 'в':0.0462616184923097, 'г':0.016890781723599996, 'д':0.032017510039207775, 'е':0.08708990503532259 + 7.711060626731281e-05, 'ж':0.011408810776503806, 'з':0.015397208596053123, 'и':0.06484764723677108,
                       'й':0.010013701961575193, 'к':0.03302706582279983, 'л':0.04596148028637693, 'м':0.03143977365071268, 'н':0.06508609695769, 'о':0.114725160004508, 'п':0.027441885295007386, 'р':0.04183191074150745, 'с':0.05293109277592251, 'т':0.06475155555819181,
                       'у':0.02965199390233052, 'ф':0.0012444465534524791, 'х':0.008508265663833347, 'ц':0.00277242287456477, 'ч':0.018103197717526054, 'ш':0.00823066748127102, 'щ':0.00299070520615224, 'ъ':0.00024200867197741253, 'ы':0.016513532911399915,
                       'ь':0.022984892252756704, 'э':0.0035269204989649386, 'ю':0.005617211087318864, 'я':0.02136438320412364}
    lowestDifference = inf
    differenceSum = 0
    encryptionKey = 0
    for key in keys:
        decryptedText = CeasarDecrypt(text, key, alphabet)
        entries = CountLettersEntries(decryptedText, alphabet)
        for char in alphabet:
            differenceSum += abs(letterFrequency.get(char) - (entries.get(char) / len(decryptedText)))
        if differenceSum < lowestDifference:
            lowestDifference = differenceSum
            encryptionKey = key
        #print("key {}({}) - DifferenceSum {}".format(key, alphabet[key], differenceSum))
    #print()
    return encryptionKey

def FindCeasarKey(text,alphabet):
    possibleCeasarKeys = []
    entries = CountLettersEntries(text,alphabet)
    mostFrequentLetter = max(entries, key = entries.get)
    possibleCeasarKeys.append((alphabet.find(mostFrequentLetter) - alphabet.find('о')) % len(alphabet))
    possibleCeasarKeys.append((alphabet.find(mostFrequentLetter) - alphabet.find('е')) % len(alphabet))
    possibleCeasarKeys.append((alphabet.find(mostFrequentLetter) - alphabet.find('а')) % len(alphabet))
    encryptionKey = CompareCeasarKeys(text, possibleCeasarKeys, alphabet)
    return encryptionKey

def VigenereDecrypt(text,key,alphabet):
    keyCharIndex = 0
    decryptedText = ''
    for char in text:
        decryptedCharIndex = (alphabet.find(char) - alphabet.find(key[keyCharIndex])) % len(alphabet)
        keyCharIndex = (keyCharIndex + 1) % len(key)
        decryptedText += alphabet[decryptedCharIndex]
    return decryptedText

if __name__ == "__main__":

    #Task1 and Task2

    keys = ["об","нам","круг","мышка","ассоциация","антикоммунистический"]
    alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

    text = ReadFile("textToEncrypt.txt")
    text = ClearText(text,alphabet)
    encryptionIndex = []
    for key in keys:
        if len(key) <= len(text):
            encryptedText = VigenereEncrypt(text,key,alphabet)
            with open(f"EncryptedWithPeriod{len(key)}.txt", "w") as file:
                file.write(encryptedText)
            encryptionIndex.append([len(key),ConformityIndex(encryptedText,alphabet)])
        else:
            print("Encryption key length must be equal or shorter than text!")
    encryptionIndex.append(["Clear text", ConformityIndex(text,alphabet)])
    GenerateCSV("EncryptedIndex", encryptionIndex, ["r value", "Index"])

    #Task3

    textToDecrypt = ReadFile("textToDecrypt.txt")
    textToDecrypt = ClearText(textToDecrypt,alphabet)
    decryptionIndex = DecryptionIndex(textToDecrypt,alphabet)
    GenerateCSV("DecryptionIndex",decryptionIndex,["r value","Index"])
    possibleKeys = FindPossibleKeys(decryptionIndex,"OnlyLetters.csv")
    blocksOfCeasar = BlocksOfCeasar(textToDecrypt,possibleKeys[0])
    vigenereKey = ''
    for block in blocksOfCeasar:
        key = FindCeasarKey(block,alphabet)
        vigenereKey += alphabet[key]
    #print(vigenereKey)
    vigenereKey = 'чугунныенебеса' #чкгунныенебеиа
    decryptedText = VigenereDecrypt(textToDecrypt,vigenereKey,alphabet)
    with open("DecryptedText.txt","w") as file:
        file.write(decryptedText)