#!/usr/bin/env python
import collections
import numpy as np





def GetProbability(Filename, Alphabet):
    File = open(Filename, "r")
    RawText = File.read().lower()
    RawText = RawText.replace('ё','е')
    RawText = RawText.replace('ъ','ь')

    TextList = [i for i in RawText if i in Alphabet]

    LetterCount = collections.Counter(TextList)
    TotalAmount = 0
    for i in LetterCount.values():
        TotalAmount += i
    print(f"Total letters: {TotalAmount}")

    LetterProbablilty =  {}
    for i in LetterCount.keys():
        LetterProbablilty[i] = LetterCount[i]/TotalAmount
    return LetterProbablilty


def GetBigrams(Filename, Alphabet, Step=False):
    File = open(Filename, "r")
    RawText = File.read().lower()
    RawText = RawText.replace('ё','е')
    RawText = RawText.replace('ъ','ь')

    TextList = [i for i in RawText if i in Alphabet]
    if Step == False:
        BigramsCount = len(list(zip(TextList,TextList[1:])))
        Bigrams = collections.Counter(zip(TextList,TextList[1:]))
    else:
        BigramsCount = len(list(zip(TextList,TextList[2:])))
        Bigrams = collections.Counter(zip(TextList,TextList[2:]))


    ReportFile = open("BigramProb.txt", "w")
    for i in Bigrams.keys():
        Bigrams[i] = Bigrams[i]/BigramsCount

    return Bigrams




def GetBigramEntropy(Probabilities):
    Probabilities = [i for i in Probabilities.values()]
    Entropy = -np.sum(Probabilities * np.log2(Probabilities))
    return Entropy

def GetTextEntropy(Probablilties):
    Probabilities = [i for i in Probablilties.values()]
    Entropy = -np.sum(Probabilities * np.log2(Probabilities))
    return Entropy


def GetHn(H, n, Aplhabet):
    if n == 0:
        return np.log2(len(Alphabet))
    else:
        return (1/n)*H


def GetRedurancy(H_inf, H0):
    return 1-(H_inf/H0)



def WriteProbToFile(Filename, Probabilities):
    ReportFile = open(Filename, "w")
    Sorted = sorted(Probabilities.items(), key = lambda x:x[1], reverse = True)
    for i in Sorted:
        Formatted = f"{i[0]}: {i[1]:.4f}\n"
        ReportFile.write(Formatted)

    return



def main():
    Filename = "karam.txt"
    Alphabet = ['к','ф','щ','й','и','у','т','л','э','я','е','с','ш','д','в','з','п','а','р','г','н','ч','о','х','м','ы','ю','б','ц','ь','ж'] 
    AlphabetSpace = Alphabet.copy()
    AlphabetSpace.append(" ")

    BigramProbability = GetBigrams(Filename, Alphabet)
    BigramProbabilityStep = GetBigrams(Filename, Alphabet, Step=True)
    BigramEntropy = GetBigramEntropy(BigramProbability)
    BigramEntropyStep = GetBigramEntropy(BigramProbabilityStep)
    LetterProbablilty = GetProbability(Filename, Alphabet)
    LetterEntropy = GetTextEntropy(LetterProbablilty)


    BigramProbabilitySpace = GetBigrams(Filename, AlphabetSpace)
    BigramEntropySpace = GetBigramEntropy(BigramProbabilitySpace)
    BigramProbabilityStepSpace = GetBigrams(Filename, AlphabetSpace, Step=True)
    BigramEntropyStepSpace = GetBigramEntropy(BigramProbabilityStepSpace)


    H1 = GetHn(LetterEntropy, 1, Alphabet)
    H2 = GetHn(BigramEntropy, 2, Alphabet)
    H2Step = GetHn(BigramEntropyStep, 2, Alphabet)
    H2Space = GetHn(BigramEntropySpace, 2, AlphabetSpace)
    H2StepSpace = GetHn(BigramEntropyStepSpace, 2, AlphabetSpace)

    R1 = GetRedurancy(H1,np.log2(len(Alphabet)))
    R2 = GetRedurancy(H2,np.log2(len(Alphabet)))
    R2Step = GetRedurancy(H2Step,np.log2(len(Alphabet)))
    R2Space = GetRedurancy(H2Space, np.log2(len(AlphabetSpace)))
    R2StepSpace = GetRedurancy(H2StepSpace, np.log2(len(AlphabetSpace)))

    WriteProbToFile("BigramProbability.txt", BigramProbability)
    WriteProbToFile("BigramProbabilityStep.txt", BigramProbabilityStep)
    WriteProbToFile("BigramProbabilitySpace.txt", BigramProbabilitySpace)
    WriteProbToFile("BigramProbabilityStepSpace.txt", BigramProbabilityStepSpace)
    WriteProbToFile("LetterProbablilty.txt", LetterProbablilty)

    print(f"Letter entropy is: {LetterEntropy:4f}")
    print(f"Bigram entropy without step is: {BigramEntropy:.4f}")
    print(f"Bigram entropy with step is: {BigramEntropyStep:.4f}")
    print(f"Bigram Entropy with space is {BigramEntropySpace:.4f}")
    print(f"Bigram Entropy with step and space is {BigramEntropyStepSpace:.4f}")
    print("*"+"-"*40+"*")

    print(f"H1 is {H1:.4f}")
    print(f"H2 is {H2:.4f}")
    print(f"H2Step is {H2Step:.4f}")
    print(f"H2Space is {H2Space:.4f}")
    print(f"H2StepSpace is {H2StepSpace:.4f}")
    print("*"+"-"*40+"*")

    print(f"Redurancy 1 is: {R1:.4f}")
    print(f"Redurancy 2 without step is: {R2:.4f}")
    print(f"Redurancy 2 with step is: {R2Step:.4f}")
    print(f"Redurancy 2 with space is: {R2Space:.4f}")
    print(f"Redurancy 2 with step and space is: {R2StepSpace:.4f}")
    print("*"+"-"*40+"*")









if __name__ ==  '__main__':
    main()
