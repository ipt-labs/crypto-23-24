import matplotlib.pyplot as plt

alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
alphabet_len = len(alphabet)
alphabet_set = {alphabet[i]:i for i in range(alphabet_len)}
alphabet_set_reverse = {i:alphabet[i] for i in range(alphabet_len)}
file = "open_text.txt"


key2 = "це"
key3 = "цес"
key4 = "цеск"
key5 = "цеска"
key10 = "цескарбтут"
key20 = "щовибачитепередсобою"


def write_text_to_file(file_path, text, mode='w'):
    with open(file_path, mode, encoding='utf-8') as file:
        file.write(text)



def print_diagram(data):
    keys = list(data.keys())
    values = list(data.values())

    # Create a bar chart
    plt.bar(keys, values)

    # Set labels and title
    plt.xlabel('Key_length')
    plt.ylabel('Compliance_index')
    plt.title('Bar Chart of Dictionary Data')

    # Display the chart
    plt.show()

def read_text_from_file(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        text = file.read()
    return text

def viginere_encoder(text,key):
    text_len=len(text)
    key_len  = len(key)
    long_key = str(key*((text_len//key_len)+1))[:text_len]
    
    text_list = [alphabet_set[i] for i in text]
    key_list = [alphabet_set[i] for i in long_key]

    encoded_list = [text_list[i]+key_list[i] for i in range(text_len)]
    encoded_list = [i  if i<32 else i-32 for i in encoded_list]
    encoded_string_list = [alphabet_set_reverse[i] for i in encoded_list]
    return "".join(encoded_string_list)

def char_frequency(text):
    dict_with_frequency = {}
    for char in alphabet:
        dict_with_frequency[char] = 0

    for item in text:
        if item in dict_with_frequency:
            dict_with_frequency[item] += 1
    # Calculate and print normalized character frequencies
    # for char in alphabet:
    #     dict_with_frequency[char] = dict_with_frequency[char] / len(text)
    return dict_with_frequency


def compliance_index(text_len,freq):
    return sum([freq[key]*(freq[key]-1) for key in freq])     /     (text_len*(text_len-1))

text = read_text_from_file(file) 
encoded = {}
encoded[0] = text
encoded[2] = viginere_encoder(text,key2)
encoded[3]= viginere_encoder(text,key3)
encoded[4] = viginere_encoder(text,key4)
encoded[5] = viginere_encoder(text,key5)
encoded[10] = viginere_encoder(text,key10)
encoded[20] = viginere_encoder(text,key20)



compliance_indexes = {}
for i in encoded:
    compliance_indexes[i]=compliance_index(len(encoded[i]),char_frequency(encoded[i]))
    write_text_to_file(f"key_length_{i}.txt", encoded[i])
print_diagram(compliance_indexes)


