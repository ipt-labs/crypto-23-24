import matplotlib.pyplot as plt
import numpy as np  # Import NumPy for array manipulation

with open('message.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()
    file_contents = file_contents.replace("\n","")

def closest_number(arr, target):
    return min(arr, key=lambda x: abs(x - target))

def IndexVidpovidnosty(encoded_text):
    ukrainian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    length = len(encoded_text)
    j = 0
    sum = 0
    while j < len(ukrainian_alphabet):
        encoded_text_count = encoded_text.count(ukrainian_alphabet[j])
        sum = sum + (encoded_text_count * (encoded_text_count - 1))
        j = j + 1
    result = (1/(length * (length-1))) * sum
    return result


def Decode(text, key):
    ukrainian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    key_array = []
    for char in key:
        key_array.append(ukrainian_alphabet.index(char))
    result = ""
    i = 0
    while i < len(text):
        encoded_pos = ukrainian_alphabet.index(text[i])
        new_pos = (encoded_pos - key_array[i%len(key_array)])%len(ukrainian_alphabet)
        result = result + ukrainian_alphabet[new_pos]
        i = i + 1
    return result


def get_letters_with_period(input_string, period):
    if period <= 0:
        raise ValueError("Period should be a positive integer.")

    result = input_string[::period]
    return result


def rotate_array(arr, rotations):
    if len(arr) == 0:
        return arr

    rotations = rotations % len(arr)  # Ensure that rotations are within the array's length
    return arr[-rotations:] + arr[:-rotations]


russian_letter_frequencies = [
    0.0801, 0.0159, 0.0454, 0.0165, 0.0298, 0.0845, 0.0072, 0.016, 0.0735,
    0.0106, 0.0321, 0.0497, 0.0333, 0.067, 0.1097, 0.0281, 0.0473, 0.0547, 0.0626,
    0.0262, 0.0026, 0.0097, 0.0048, 0.0144, 0.0073, 0.0061, 0.0004, 0.019, 0.0174,
    0.0032, 0.0064, 0.0201
]



i = 1
while i < 51:
    temp_text = ""
    j = 0
    while j < (len(file_contents)):
        temp_text = temp_text + file_contents[j]
        j = j + i
    print(f"Індекс для ключа {i} - ", IndexVidpovidnosty(temp_text))
    i = i + 1


#13!!!!
file_contents = file_contents[:]
russian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
string = get_letters_with_period(file_contents, 13)
string_freq = []
i = 0
while i < len(russian_alphabet):
    string_freq.append(string.count(russian_alphabet[i])/len(string))
    i = i+1

string_freq = rotate_array(string_freq, -3)

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ,14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
bar_width = 0.3  # Adjust this value to control the separation between bars
x_adjusted = np.arange(len(x))

# Create bar charts for both datasets
plt.bar(x_adjusted - bar_width/2, russian_letter_frequencies, width=bar_width, label='Russian Letter Frequencies', color='b')
plt.bar(x_adjusted + bar_width/2, string_freq, width=bar_width, label='Obtained Letter Frequencies', color='r')

# Add labels and a legend
plt.xlabel('Letter number')
plt.ylabel('Frequency')
plt.legend()

# Display the graph
plt.show()

key = [-3,-16,-14,-12,-27,-10,-14,-2,-5,-4,-28,-12,0]
string_key = ''
for value in key:
    string_key += russian_alphabet[abs(value)]

print(string_key)

#громыковедьма
print(Decode(file_contents, string_key))