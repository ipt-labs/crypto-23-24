import math
def clean_text(text):

    text = ' '.join(text.split())
    text = text.lower()
    text = ''.join(char for char in text if (char.isalpha() and ord(char)>1071 and ord(char)<1106) or char.isspace())

    
    text=text.replace("  "," ")
    text=text.replace("   "," ")
    text=text.replace("    "," ")
    return text
def entropy(original_text,letter_freq):
    entropy=float(0)
    for chastota in letter_freq.values():
        entropy+=(chastota/len(original_text))*math.log2(chastota/len(original_text))
    return -entropy 
def entropy_bigram_with_overlap(bigram_amount,letter_freq):
    entropy=float(0)
    for chastota in letter_freq.values():
        entropy+=(chastota/(len(bigram_amount)-1))*math.log2(chastota/(len(bigram_amount)-1))*0.5
    return -entropy
def entropy_bigram_without_overlap(bigram_amount,letter_freq):
    entropy=float(0)
    for chastota in letter_freq.values():
        entropy+=(chastota/(len(bigram_amount)/2))*math.log2(chastota/(len(bigram_amount)/2))*0.5
    return -entropy
def find_freq(formated_text):
    letter_frequency = {}
    for litera in formated_text:
        if litera in letter_frequency:
            letter_frequency[litera] += 1
        else:
            letter_frequency.update({litera: 1})
    return letter_frequency

def find_freq_2(formatted_text):
    letter_frequency = {}
    
    # Iterate through the text, taking every pair of letters
    for i in range(len(formatted_text) - 1):
        pair = formatted_text[i:i+2]
        if len(pair) == 2:
            if pair in letter_frequency:
                letter_frequency[pair] += 1
            else:
                letter_frequency[pair] = 1
    return letter_frequency
def find_freq_3(formatted_text):
    letter_frequency = {}
    
    # Iterate through the text, taking every pair of non-overlapping letters
    for i in range(0, len(formatted_text) - 1, 2):
        pair = formatted_text[i:i+2]
        if len(pair) == 2:
            if pair in letter_frequency:
                letter_frequency[pair] += 1
            else:
                letter_frequency[pair] = 1
    
    return letter_frequency

def print_freq(let_freq,formated_text):
    print("загальна "," відсоток від ")
    print("кількість"," загального")
    for letter, frequency in sorted(let_freq.items(), key=lambda x:x[1], reverse=True):
        print(f"{letter}: {frequency},    %= {round(int(frequency)/len(formated_text)*100,3)}")
    return None
def nadlishkovist_without_spaces(entropy):
    return 1-(entropy/math.log2(int(33)))

def nadlishkovist_with_spaces(entropy):
    return 1-(entropy/math.log2(int(34)))

input_file_path = 'D:\\uni year 3\\crypto labs\\tasks\\cp1\\test.txt'
with open(input_file_path, 'r', encoding='utf-8') as file:

    text = file.read()

output_with_spaces = clean_text(text)

output_with_spaces_path = 'D:\\uni year 3\\crypto labs\\tasks\\cp1\\output with spaces.txt'
with open(output_with_spaces_path, 'w', encoding='utf-8') as file:
    file.write(output_with_spaces)

output_without_spaces = output_with_spaces.replace(' ', '')

output_with_spaces_freq=find_freq(output_with_spaces)
output_without_spaces_freq=find_freq(output_without_spaces)
# print_freq(output_without_spaces_freq,output_without_spaces)

output_without_spaces_bi_freq=find_freq_2(output_without_spaces)
output_with_spaces_bi_freq=find_freq_2(output_with_spaces)

#print_freq(output_without_spaces_bi_freq,output_without_spaces)
# print_freq(output_with_spaces_bi_freq,output_with_spaces)


output_without_spaces_bi_freq_without_overlap=find_freq_3(output_without_spaces)
output_with_spaces_bi_freq_without_overlap=find_freq_3(output_with_spaces)
# print_freq(output_without_spaces_bi_freq_without_overlap,output_without_spaces)
# print_freq(output_with_spaces_bi_freq_without_overlap,output_with_spaces)

entropy_with_spaces=entropy(output_with_spaces,output_with_spaces_freq)
entropy_without_spaces=entropy(output_without_spaces,output_without_spaces_freq)
entropy_without_spaces_bigram=entropy_bigram_with_overlap(output_without_spaces,output_without_spaces_bi_freq)
entropy_with_spaces_bigram=entropy_bigram_with_overlap(output_with_spaces,output_with_spaces_bi_freq)
entropy_without_spaces_bigram_without_overlap=entropy_bigram_without_overlap(output_without_spaces,output_without_spaces_bi_freq_without_overlap)
entropy_with_spaces_bigram_without_overlap=entropy_bigram_without_overlap(output_with_spaces,output_with_spaces_bi_freq_without_overlap)
print("entropy with spaces",entropy_with_spaces)
print("R=",nadlishkovist_with_spaces(entropy_with_spaces))
print("******")
print("entropy without spaces",entropy_without_spaces)
print("R=",nadlishkovist_without_spaces(entropy_without_spaces))
print("******")
print("entropy without spaces bigram",entropy_without_spaces_bigram)
print("R=",nadlishkovist_without_spaces(entropy_without_spaces_bigram))
print("******")
print("entropy with spaces bigram",entropy_with_spaces_bigram)
print("R=",nadlishkovist_with_spaces(entropy_with_spaces_bigram))
print("******")
print("entropy without spaces bigram without overlap",entropy_without_spaces_bigram_without_overlap)
print("R=",nadlishkovist_without_spaces(entropy_without_spaces_bigram_without_overlap))
print("******")
print("entropy with spaces bigram without overlap",entropy_with_spaces_bigram_without_overlap)
print("R=",nadlishkovist_with_spaces(entropy_with_spaces_bigram_without_overlap))
print("COOL PINK PROGRAM R")
print("H(10)",nadlishkovist_with_spaces(float(2.58759931788218)), "> R >",nadlishkovist_with_spaces(float(3.17669456263237)))
print("H(20)",nadlishkovist_with_spaces(float(1.51567813452112)), "> R >",nadlishkovist_with_spaces(float(2.29225447733486)))
print("H(30)",nadlishkovist_with_spaces(float(1.13902801008919)), "> R >",nadlishkovist_with_spaces(float(1.70396957073853)))
output_without_spaces_path = 'D:\\uni year 3\\crypto labs\\tasks\\cp1\\output without spaces.txt'
with open(output_without_spaces_path, 'w', encoding='utf-8') as file:
    file.write(output_without_spaces)

