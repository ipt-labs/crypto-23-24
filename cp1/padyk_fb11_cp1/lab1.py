import re
import math
import csv

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "



def save_dict_to_csv(data_dict, file_name):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Key', 'Value'])
        writer.writerows(data_dict.items())
    print(f'Dictionary saved to {file_name} successfully.')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\sа-яё]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def no_whitespaces(text):
    return re.sub(r'\s+', '', text)

def open_textfile(input_file):
    # Open the input file for reading
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def save_textfile(text,output_file):
    # Open the output file for writing and save the cleaned text
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

def char_frequency(text):
    # Initialize a dictionary to store character frequencies
    dict_with_frequency = {}
    for char in alphabet:
        dict_with_frequency[char] = 0

    # Count the frequencies of characters in the text
    for item in text:
        if item in dict_with_frequency:
            dict_with_frequency[item] += 1
    # Calculate and print normalized character frequencies
    for char in alphabet:
        dict_with_frequency[char] = dict_with_frequency[char] / len(text)
    return dict_with_frequency 


def entropy(dict_with_frequency):   
    entropy_list = []
    for i in dict_with_frequency.values():
        if i != 0:
         entropy_list.append(-(i * math.log2(i)))
        else:
            entropy_list.append(0)
            
    for j in dict_with_frequency.keys():
        if len(j) > 1:   
            entropy = 0.5 * sum(entropy_list)
        else:
            entropy = sum(entropy_list)
    print(f"Entropy: {entropy}")
    return entropy


def bigram_frequency(text):

 
    bigrams = []

    # Extract bigrams from the text
    for i in range(0, len(text), 2):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            bigrams.append(bigram)


    for i in range(1, len(text), 2):
        bigram = text[i:i + 2]
        if len(bigram) == 2:
            bigrams.append(bigram)

    # Count the frequencies of bigrams in the text
    frequency = {}
    for i in bigrams:
        if i in frequency:
            frequency[i] += 1
        else:
            frequency[i] = 1

    # Sort the bigram dictionary by frequency 
    frequency = dict(sorted(frequency.items(), key=lambda x: x[1]))
    # Calculate normalized bigram frequencies
    for i in list(frequency.keys()):
        frequency[i] = frequency[i] / len(bigrams)

    return frequency

def redundancy(entropy, alphabet_num):
    redundancy = 1 - (entropy / math.log2(alphabet_num))
    return redundancy


text = open_textfile("input.txt")
text_with_spaces = clean_text(text)
save_textfile(text_with_spaces,"output.txt")
text_no_spaces = no_whitespaces(text_with_spaces)
save_textfile(text_no_spaces,"output2.txt")


print("1.")
result1 = char_frequency(text_with_spaces)
entropy1 = entropy(result1)
print(redundancy(entropy1,len(alphabet)))
save_dict_to_csv(result1,"result1.csv")

print("2.")
result2 = char_frequency(text_no_spaces)
entropy2 = entropy(result2)
print(redundancy(entropy2,len(alphabet)-1))
save_dict_to_csv(result2,"result2.csv")

print("3.")
result3 = bigram_frequency(text_with_spaces)
entropy3 = entropy(result3)
print(redundancy(entropy3,len(alphabet)))
save_dict_to_csv(result3,"result3.csv")

print("4.")
result4 = bigram_frequency(text_no_spaces)
entropy4 = entropy(result4)
print(redundancy(entropy4,len(alphabet)-1))
save_dict_to_csv(result4,"result4.csv")




