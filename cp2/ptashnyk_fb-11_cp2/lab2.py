from csv import reader,writer

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

def SplitTextIntoBlocks(text,numberOfBlocks):
    blocks = []
    for i in range(0,numberOfBlocks):
        blocks.append(text[i::numberOfBlocks])
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

def GenerateCSV(filename,data):
    with open(f"{filename}.csv", "w", newline = "") as file:
        csvwriter = writer(file)
        csvwriter.writerows(data)

def FindEncryptionKey(textToDecrypt,fileWithData):
    decryptionIndex = {}
    for r in range(2,31):
        blocks = SplitTextIntoBlocks(textToDecrypt,r)
        decryptionIndex.update({r:BlocksConformityIndex(blocks,decryptionAlphabet)})
    possibleKeys = []
    theoreticalIndex = TheoreticalConformityIndex(fileWithData)
    for key, value in decryptionIndex.items():
        if abs(theoreticalIndex - value) <= 0.01:
            possibleKeys.append(key)
    return possibleKeys

def VigenereDecrypt(encryptedText,key,alphabet):
    entries = CountLettersEntries(encryptedText,alphabet)
    blocks = SplitTextIntoBlocks(encryptedText,len(encryptedText) // key)
    print(blocks)


if __name__ == "__main__":
    keys = ["об","нам","круг","мышка","ассоциация","антикоммунистический"]
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    decryptionAlphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    text = ReadFile("textToEncrypt.txt")
    text = ClearText(text,alphabet)
    encryptionIndex = [["r value", "Index"]]
    for key in keys:
        if len(key) <= len(text):
            encryptedText = VigenereEncrypt(text,key,alphabet)
            with open(f"Encrypted with period {len(key)}.txt", "w") as file:
                file.write(encryptedText)
            encryptionIndex.append([len(key),ConformityIndex(encryptedText,alphabet)])
        else:
            print("Encryption key length must be equal or shorter than text!")
    encryptionIndex.append(["Clear text", ConformityIndex(text,alphabet)])
    GenerateCSV("Encrypted Index", encryptionIndex)

    textToDecrypt = ReadFile("textToDecrypt.txt")
    textToDecrypt = ClearText(textToDecrypt,decryptionAlphabet)
    possibleKeys = FindEncryptionKey(textToDecrypt,"OnlyLetters.csv")
    VigenereDecrypt(textToDecrypt,possibleKeys[0],decryptionAlphabet)