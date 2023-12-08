import math
import matplotlib.pyplot as plt


alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
alphabet_len = len(alphabet)
alphabet_set = {alphabet[i]:i for i in range(alphabet_len)}
print(alphabet_set)
file = "encoded_v14.txt"

print("Alphabet: ", alphabet, "\nLength: ", alphabet_len)

def print_diagram(data):
    keys = list(data.keys())
    values = list(data.values())

    # Create a bar chart
    plt.bar(keys, values)

    # Set labels and title
    plt.xlabel('Key')
    plt.ylabel('Value')
    plt.title('Bar Chart of Dictionary Data')

    # Display the chart
    plt.show()

def read_text_from_file(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        text = file.read()
    return text.strip()

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
    # for char in alphabet:
    #     dict_with_frequency[char] = dict_with_frequency[char] / len(text)
    
    dict_with_frequency_indexed = {}
    for i in dict_with_frequency:
        # dict_with_frequency_indexed[f"{i}:{alphabet_set[i]}"] = dict_with_frequency[i]
        dict_with_frequency_indexed[f"{alphabet_set[i]}"] = dict_with_frequency[i]

    return dict_with_frequency_indexed

def compliance_index(text,freq):
    text_len = len(text)
    return sum([freq[key]*(freq[key]-1) for key in freq])     /     (text_len*(text_len-1))


text = read_text_from_file(file)
def detect_key_length():
    diagram_dict = {}
    def temp(text,i):      
        dict_with_frequency = char_frequency(text)
        diagram_dict[i]= compliance_index(text,dict_with_frequency)
        # sorted_dict_with_frequency = dict(sorted(dict_with_frequency.items(), reverse=True, key= lambda item:item[1]))
        # print(sorted_dict_with_frequency)

    for i in range(1,40):
        # print(f"\nEach {i} char analysys:\n")
        temp(text[::i],i)
    print_diagram(diagram_dict)



# detect_key_length()
# detected key length for variant 14 key_length=19











key_length = 19 
caesar_strings = [0]*key_length
for i in range(key_length):
    caesar_strings[i] = text[i::key_length]

# print("caesar_strings\n", caesar_strings)

def detect_key():
    for index in range(key_length):
        value = caesar_strings[index]
        dict_with_frequency = char_frequency(value)
        sorted_dict_with_frequency = dict(sorted(dict_with_frequency.items(), reverse=True, key= lambda item:item[1]))
        # print(f"\nanalyzying each {index} column:")
        print(" ".join(list(sorted_dict_with_frequency.keys())[:4]))


# detect_key()






# # detected column_keys
found_key = 'конкистадорыгермеса'
column_keys = [alphabet_set[i] for i in found_key]

def caesar_decrypt(ciphertext, shift, alphabet):
    decrypted_text = ""

    for char in ciphertext:
        if char in alphabet:
            char_index = alphabet.index(char)
            decrypted_char_index = (char_index - shift) % len(alphabet)
            decrypted_char = alphabet[decrypted_char_index]
            decrypted_text += decrypted_char
        else:
            decrypted_text += char

    return decrypted_text

decrypted_caesar_strings = []
for i in range(key_length):
    decrypted_caesar_strings.append(caesar_decrypt(caesar_strings[i], column_keys[i], alphabet))

decrypted_text = ""

# print("decrypted_caesar_strings /n",decrypted_caesar_strings)
len1 = len(decrypted_caesar_strings[1])
break_point = key_length-1
for i in range(key_length):  
    if len(decrypted_caesar_strings[i])< len1:
        break_point = i
        break

   
   

for i in range(len1):
    for j in range(key_length):
        if i == len1-1 and j==break_point :
            break
        else :
            decrypted_text += decrypted_caesar_strings[j][i]

print(decrypted_text)




print(len(text))
print(len(decrypted_text))





