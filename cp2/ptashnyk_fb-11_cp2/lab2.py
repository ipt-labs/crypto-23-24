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

def SplitTextIntoBlocks(text,length):
    blocks = []
    for i in range(0,len(text),length):
        blocks.append(text[i:i + length])
    return blocks

def CountLettersEntries(text,alphabet):
    entries = {}
    for char in alphabet:
        number = text.count(char)
        entries.update({char:number})
    return entries

def ConformityIndex(text,blocks,alphabet):
    entries = CountLettersEntries(text,alphabet)
    entriesSum = 0
    conformityIndex = 0
    for block in blocks:
        for char in block:
            entriesSum += entries.get(char) * (entries.get(char) - 1)
            conformityIndex += entriesSum / (len(text) * len(text) - 1)
    return conformityIndex

if __name__ == "__main__":
    keys = ["об","нам","круг","мышка","ассоциация","антикоммунистический"]
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    text = ReadFile("textToEncrypt.txt")
    text = ClearText(text,alphabet)
    for key in keys:
        if len(key) <= len(text):
            encryptedText = VigenereEncrypt(text,key,alphabet)
            print(encryptedText)
        else:
            print("Encryption key must be shorter than text!")
    blocks = SplitTextIntoBlocks(text,2)
    print(ConformityIndex(text,blocks,alphabet))