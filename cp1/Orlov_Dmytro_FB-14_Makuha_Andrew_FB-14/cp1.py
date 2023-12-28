import re
import numpy as np
import pandas as pd
import math


class TextAnalyz:

    def __init__(self,text):
        self.text = self.filter_input(text)
        self.text_without_spaces = self.remove_spaces()
        self.h1 = 0
        self.h2 = 0
        self.h1_s = 0
        self.h2_s = 0
        self.alphabet = 'абвгдеёжзийклмнопстуфхцчшщыьэюя'

    def filter_input(self, text):
        # lowercase input for filtering
        text = text.lower()

        # drop non russian symbols via regex
        text = re.sub("[^а-я]", " ", text)

        text = re.sub(r'\s+', '_', text)

        # Replace letters which not included in task alphabet
        text = text.replace("ъ", "ь").replace("ё", "е")

        return text
    
    def remove_spaces(self):
        return self.text.replace('_','')
    
    def count_h1(self, shouldSaveResults, without_spaces = False):
        if without_spaces:
            text = self.text_without_spaces
            alphabet = self.alphabet
            postfix = '_without_spaces'
        else:
            text = self.text
            alphabet = self.alphabet + '_' 
            postfix = '_with_spaces'
        count_letters = {}
        for ch in text:
            if ch in count_letters.keys():
                count_letters[ch] += 1
            else:
                count_letters[ch] = 1

        letter_frequencies = {}        

        entropy_h1 = 0

        for i in count_letters.keys():
            letter_frequencies[i] = count_letters[i]/len(text)
            entropy_h1 += -(letter_frequencies[i] * math.log2(letter_frequencies[i]))


        if shouldSaveResults:
            letter_frequencies = dict(sorted(letter_frequencies.items(), key=lambda item: item[1], reverse=True))
            df = pd.DataFrame(list(letter_frequencies.items()), columns=['Letter', 'Frequency'])
            print(df)
            df.to_excel("letter_frequencies"+postfix+'.xlsx', index=True)
        print(f"H1 entropy:{entropy_h1}")
        print(f"Redundancy:{1 - (entropy_h1 / math.log2(len(alphabet)))}")
        self.h1 = entropy_h1

    def count_h2(self, shouldSaveResults, intersection, without_spaces = False):
        if without_spaces:
            text = self.text_without_spaces
            postfix = '_without_spaces'
            alphabet = self.alphabet
        else:
            text = self.text
            postfix = '_with_spaces'
            alphabet = self.alphabet + '_' 
        
        if intersection:
            bigram  = [text[i:i + 2] for i in range(len(text)-1)]
            intersection_mark = '_with_intersection'
        else:
            bigram = [text[i:i + 2] for i in range(0, len(text) - 1 if len(text) % 2 == 1 else len(text), 2)]
            intersection_mark = '_without_intersection'

        bigram_frequency = {}

        for i in bigram:
            if i in bigram_frequency.keys():
                bigram_frequency[i] += 1/len(bigram)
            else:
                bigram_frequency[i] = 1/len(bigram)

        bigram_entropy = 0
        for i in bigram_frequency.keys():
            bigram_entropy += - (bigram_frequency[i]) * math.log2(bigram_frequency[i])

        bigram_entropy = bigram_entropy/2

        if shouldSaveResults:
            self.display_bigram_matrix(dict(sorted(bigram_frequency.items(), key=lambda item: item[1], reverse=True)), "bigram_frequencies"+intersection_mark+postfix+".xlsx")
        
        print(f"Bigram entropy ("+(intersection_mark+postfix).replace('_',' ')+"): "+ str(bigram_entropy))
        print(f"Bigram reduancy:{1 - (bigram_entropy / math.log2(len(alphabet)))}")
        

    def display_bigram_matrix(self,bigram_dict, file):
        
        unique_letters = sorted(set(bigrams[0] for bigrams in bigram_dict.keys()))
       
        unique_letters_str = ''.join(unique_letters)

        matrix_size = len(unique_letters)
        matrix = np.zeros((matrix_size, matrix_size))

        for i in bigram_dict.keys():
            matrix[unique_letters_str.find(i[0])][unique_letters_str.find(i[1])] = bigram_dict[i]
        df = pd.DataFrame(matrix, index=unique_letters, columns=unique_letters)
        df.to_excel(file, index=True, engine='openpyxl')


def read_file_content(path):
    with open(path,'r',encoding='utf-8') as file:
        content = file.read()
    return content



content = read_file_content("example_text.txt")
analyz = TextAnalyz(content)

analyz.count_h1(True,True)
analyz.count_h1(True,False)

analyz.count_h2(True,False,False)
analyz.count_h2(True,False,True)
analyz.count_h2(True,True,False)
analyz.count_h2(True,True,True)
