from prettytable import PrettyTable
import math
import time

def countFrequency(path):
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()

    dcs_frequency_table = {} 
    contents = ''
    
    for char in text: 
        if char.isalpha():
            contents += char.lower()
        
    for char in range(0, (len(contents) - 1), 2):
        bigram = (contents[char] + contents[char+1])
        if bigram in dcs_frequency_table:
            dcs_frequency_table[bigram] += 1
        else:
            dcs_frequency_table[bigram] = 1

    sorted_dcs = dict(sorted(dcs_frequency_table.items(), key=lambda item: item[1], reverse=True))

    dcs_table = PrettyTable(['Bigram', 'Amount'])

    for bigram, count in sorted_dcs.items():
            dcs_table.add_row([bigram, count])

    print(dcs_table)  

    return sorted_dcs

def collectingKeys(path):
    alphabet = ['а', 'б', 'в', 'г', 'д',
                'е', 'ж', 'з', 'и', 'й',
                'к', 'л', 'м', 'н', 'о',
                'п', 'р', 'с', 'т', 'у',
                'ф', 'х', 'ц', 'ч', 'ш',
                'щ', 'ы', 'ь', 'э', 'ю',
                'я']
    all_bigrams = countFrequency(path)
    good_bigrams = ['ст', 'но', 'ен', 'то', 'на']
    bad_bigrams = []
    possible_keys = []

    for bigram, count in all_bigrams.items():
        bad_bigrams.append(bigram)
        if len(bad_bigrams) == 5:
            break

    def findingAB(bi1, bi2, bi3, bi4):
        bi_list = [bi1, bi2, bi3, bi4]
        num_list = []
 
        for bigram in bi_list:
            digit1 = alphabet.index(bigram[0])
            digit2 = alphabet.index(bigram[1])
            num_list.append(digit1 * 31 + digit2)

        num1, num2, num3, num4 = num_list

        dig1 = (num1 - num2)%961 #X* - X**
        dig2 = (num3 - num4)%961 #Y* - Y**

        possible_a = []
        possible_b = []
        for i in range (961):
            dig3 = (i * dig1)%961 #a(X* - X**)(mod m^2)
            if dig3 == dig2:
                possible_a.append(i)
                dig4 = (num3 - i*num1)%961
                
                possible_b.append(dig4)
                

        return possible_a, possible_b  
        print(num_list)
        
    for i in range (4):
        for j in range (i+1 ,5):
            for x in range (5):
                for y in range (5):
                    if y == x:
                        continue
                    possible_keys.append(findingAB(good_bigrams[i], good_bigrams[j], bad_bigrams[x], bad_bigrams[y]))
    print(possible_keys)
    with open("keys.txt", 'w', encoding='utf-8') as file:
        for i in possible_keys:
            file.write(f"a={str(i[0])} b={str(i[1])}\n")


collectingKeys('16.txt')

