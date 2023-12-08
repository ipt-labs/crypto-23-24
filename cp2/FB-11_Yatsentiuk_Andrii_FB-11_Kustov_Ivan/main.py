with open('text.txt', 'r', encoding='utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()

file_contents = file_contents.replace(",", "")
file_contents = file_contents.replace("!", "")
file_contents = file_contents.replace("?", "")
file_contents = file_contents.replace("=", "")
file_contents = file_contents.replace("-", "")
file_contents = file_contents.replace("_", "")
file_contents = file_contents.replace(".", "")
file_contents = file_contents.replace(":", "")
file_contents = file_contents.replace(";", "")
file_contents = file_contents.replace("1", "")
file_contents = file_contents.replace("2", "")
file_contents = file_contents.replace("3", "")
file_contents = file_contents.replace("4", "")
file_contents = file_contents.replace("5", "")
file_contents = file_contents.replace("6", "")
file_contents = file_contents.replace("7", "")
file_contents = file_contents.replace("8", "")
file_contents = file_contents.replace("9", "")
file_contents = file_contents.replace("0", "")
file_contents = file_contents.replace(" ", "")
file_contents = file_contents.replace("'", "")
file_contents = file_contents.replace("\n", "")



ukrainian_lowercase = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"


def Encoding(text, key):  # only lowercase text without spaces, key is also lowercase
    ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    key_array = [ukrainian_alphabet.index(char) for char in key]
    result = ""
    for i, char in enumerate(text):
        if char in ukrainian_alphabet:
            plain_pos = ukrainian_alphabet.index(char)
            new_pos = (plain_pos + key_array[i % len(key_array)]) % len(ukrainian_alphabet)
            result += ukrainian_alphabet[new_pos]
    return result




def Decode(text, key):
    ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    key_array = []
    for char in key:
        key_array.append(ukrainian_alphabet.index(char))
    result = ""
    i = 0
    while i < len(text):
        if text[i] in ukrainian_alphabet:  # Check if character is in the Ukrainian alphabet
            encoded_pos = ukrainian_alphabet.index(text[i])
            new_pos = (encoded_pos - key_array[i % len(key_array)]) % len(ukrainian_alphabet)
            result = result + ukrainian_alphabet[new_pos]
        i = i + 1
    return result

# Encoding
text = file_contents
key = "ва"
encoded = Encoding(text, key)
with open("encoded_output2.txt", "w", encoding="utf-8") as file:
    file.write(encoded)
#print(encoded)

# Encoding
text = file_contents
key = "гжя"
encoded = Encoding(text, key)
with open("encoded_output3.txt", "w", encoding="utf-8") as file:
    file.write(encoded)
#print(encoded)

# Encoding
text = file_contents
key = "фрмя"
encoded = Encoding(text, key)
with open("encoded_output4.txt", "w", encoding="utf-8") as file:
    file.write(encoded)
#print(encoded)

# Encoding
text = file_contents
key = "щлавн"
encoded = Encoding(text, key)
with open("encoded_output5.txt", "w", encoding="utf-8") as file:
    file.write(encoded)
#print(encoded)

# Encoding
text = file_contents
key = "шякрамифжя"
encoded = Encoding(text, key)
with open("encoded_output10.txt", "w", encoding="utf-8") as file:
    file.write(encoded)
#print(encoded)

text = file_contents
key = "пжрвдхичаедфжис"
encoded = Encoding(text, key)
with open("encoded_output15.txt", "w", encoding="utf-8") as file:
    file.write(encoded)
#print(encoded)

# Encoding
text = file_contents
key = "имривдщеупаодифражвш"
encoded = Encoding(text, key)
with open("encoded_output20.txt", "w", encoding="utf-8") as file:
    file.write(encoded)
#print(encoded)
