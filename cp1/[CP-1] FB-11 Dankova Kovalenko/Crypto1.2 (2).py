import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
import re
import string
from collections import Counter
import math

#Основна частина. Форматування тексту. Підрахунок частоти окремих букв та біграм
def russian_letter_frequency(text):

   file = open(r'C:\Users\Admin\PycharmProjects\crypto1.2\crypto1.2.txt', encoding ='utf-8')
   text = file.read()

   #preproccessing
   text = re.sub(r'[^а-яА-ЯёЁ]', '', text)
   #text = text.replace("\r","")
   text = text.lower()
   #spec_chars = string.punctuation + '\n\xa0«»\t—…'
   #text = "".join([ch for ch in text if ch not in spec_chars])

   # letter_frequency with spaces
   letter_frequency = Counter(text)
   # bigrams with spaces
   all_bigrams1 = [text[i:i + 2] for i in range(len(text) - 1)]
   all_bigram1_frequency = Counter(all_bigrams1)
   all_bigrams2 = [text[i:i + 2] for i in range(len(text) - 2)]
   all_bigram2_frequency = Counter(all_bigrams2)

   return letter_frequency, all_bigram1_frequency, all_bigram2_frequency

#Підрахунок ентропії за формулою
def calculate_entropy(frequency):
    total = sum(frequency.values())
    entropy = -sum((count / total) * math.log2(count / total) for count in frequency.values())
    return entropy


if __name__ == "__main__":
    input_text_with_spaces = " "
    input_text_without_spaces = input_text_with_spaces.replace(" ", "") #просто додатково видялємо пробіли

    letter_frequencies_with_spaces, all_bigram1_frequencies_with_spaces, all_bigram2_frequencies_with_spaces = russian_letter_frequency(input_text_with_spaces)
    letter_frequencies_without_spaces, all_bigram1_frequencies_without_spaces, all_bigram2_frequencies_without_spaces = russian_letter_frequency(input_text_without_spaces)

    h1_with_spaces = calculate_entropy(letter_frequencies_with_spaces)
    h2_with_spaces = calculate_entropy(all_bigram1_frequencies_with_spaces)
    h22_with_spaces = calculate_entropy(all_bigram2_frequencies_with_spaces)


    h1_without_spaces = calculate_entropy(letter_frequencies_without_spaces)
    h2_without_spaces = calculate_entropy(all_bigram1_frequencies_without_spaces)/2
    h22_without_spaces = calculate_entropy(all_bigram2_frequencies_without_spaces)/2

    #print("З пробілами:")
    #print(f"Частота літер: {letter_frequencies_with_spaces}")
    #print(f"Частота біграм: {all_bigram_frequencies_with_spaces}")
    #print(f"H1 (Ентропія для одинарних символів): {h1_with_spaces}")
    #print(f"H2 (Ентропія для біграм): {h2_with_spaces}")

    print("З пробілами:")
    print("Частота всіх літер: ")
    for letter, count in sorted(letter_frequencies_without_spaces.items()):
        print(f"{letter}: {count}")
    print("Частота біграм по зміщенню 1")
    for bigram1, count in sorted(all_bigram1_frequencies_without_spaces.items()):
        print(f"{bigram1}: {count}")
    print("Частота біграм по зміщенню 2")
    for bigram2, count in sorted(all_bigram2_frequencies_without_spaces.items()):
        print(f"{bigram2}: {count}")
    print(f"H1 (Ентропія для одинарних символів): {h1_without_spaces}")
    print(f"H2 (Ентропія для біграмм): {h2_without_spaces}")
    print(f"H22 (Ентропія для біграмм): {h22_without_spaces}")


#import string
#spec_chars = string.punctuation
#text = "".join([ch for ch in text if ch not in spec_chars]) #разделяй, убирай, соединяй
#Токенізація
#print(text)
#text_tokens = word_tokenize(text) #list of words(tokens)
#text = nltk.Text(text_tokens) #tokens to Text
#fdist = FreqDist(text) #frequency distributions
#print(type(text))
#print(fdist)
