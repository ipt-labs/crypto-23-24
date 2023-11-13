def ExtendedEuclidAlgorithm(a, b):
    if a == 0:
        return b, 0, 1
    gcd, u, v = ExtendedEuclidAlgorithm(b % a, a)
    return gcd, v - (b // a) * u, u

def SolveLinearComparison(a, b, n = 31):
    roots = []
    gcd, u, v = ExtendedEuclidAlgorithm(a, n)
    if gcd == 1:
        roots.append((u * b) % n)
        return roots
    if b % gcd != 0:
        return roots
    x0 = ((b // gcd) * ExtendedEuclidAlgorithm(a // gcd, n // gcd)[1]) % (n // gcd)
    for i in range(gcd):
        roots.append(x0 + i * n // gcd)
    return roots

def BigramFrequency(text):
    bigramFrequency = {}
    for i in range(1, len(text), 2):
        bigram = text[i - 1: i + 1]
        if bigram in bigramFrequency:
            bigramFrequency[bigram] += 1
        else:
            bigramFrequency[bigram] = 1
    return list(dict(sorted(bigramFrequency.items(), key = lambda x : x[1], reverse = True)).keys())[:5]

def LetterFrequency(text, alphabet):
    letterFrequency = {}
    for letter in alphabet:
        number = text.count(letter)
        frequency = number / len(text)
        letterFrequency[letter] = frequency
    return letterFrequency

def ReadFile(filename):
    with open(filename, encoding = "utf-8", mode = "r") as file:
        text = file.read().lower()
    return text

def ClearText(text):
    alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
    text = " ".join("".join(filter(alphabet.__contains__,text)).split())
    return text

def BigramPairs(commonBigrams, encryptedBigrams):
    bigramPairs = []
    for common in commonBigrams:
        for encrypted in encryptedBigrams:
            bigramPairs.append([common, encrypted])
    return bigramPairs

def FindKeys(bigramPairs, alphabet):
    keys = []
    for firstPair in bigramPairs:
        for secondPair in bigramPairs:
            if firstPair[0] != secondPair[0] and firstPair[1] != secondPair[1]:
                x1, y1 = ConvertBigramToInt(firstPair[0], alphabet), ConvertBigramToInt(firstPair[1], alphabet)
                x2, y2 = ConvertBigramToInt(secondPair[0], alphabet), ConvertBigramToInt(secondPair[1], alphabet)
                roots = SolveLinearComparison(x1 - x2, y1 - y2, len(alphabet) * len(alphabet))
                if roots:
                    for a in roots:
                        keys.append([a, (y1 - a * x1) % (len(alphabet) * len(alphabet))])
    return keys

def ConvertBigramToInt(bigram,alphabet):
    return alphabet.index(bigram[0]) * len(alphabet) + alphabet.index(bigram[1])

def ConvertIntToBigram(int, alphabet):
    return alphabet[int // len(alphabet)] + alphabet[int % len(alphabet)]

def DecryptText(text, keys, alphabet):
    decryptedText = ""
    result = []
    for key in keys:
        for i in range(1, len(text), 2):
            y = ConvertBigramToInt(text[i - 1: i + 1], alphabet)
            x = (ExtendedEuclidAlgorithm(key[0], len(alphabet) * len(alphabet))[1] * (y - key[1])) % (len(alphabet) * len(alphabet))
            decryptedText += ConvertIntToBigram(x, alphabet)
        result.append([key, decryptedText])
        decryptedText = ""
    return result

def CheckDecryption(decryptedTexts, alphabet):
    for text in decryptedTexts:
        letterFrequency = LetterFrequency(text[1], alphabet)
        if abs(letterFrequency.get("ф") - 0.001) < 0.01 and abs(letterFrequency.get("щ") - 0.003) < 0.01 and abs(letterFrequency.get("ь") - 0.02) < 0.01:
            return text

def main():
    alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"
    mostCommonBigrams = ["ст", "но", "то", "на", "ен"]
    text = ReadFile("12.txt")
    text = ClearText(text)
    mostEncryptedBigrams = BigramFrequency(text)
    print(mostEncryptedBigrams)
    bigramPairs = BigramPairs(mostCommonBigrams, mostEncryptedBigrams)
    keys = FindKeys(bigramPairs, alphabet)
    decryptedTexts = DecryptText(text, keys, alphabet)
    decryptedText = CheckDecryption(decryptedTexts, alphabet)
    print(decryptedText[0])
    with open(file = "12_decrypted.txt", encoding = "utf-8", mode = "w") as file:
        file.write(decryptedText[1])

if __name__ == "__main__":
    main()