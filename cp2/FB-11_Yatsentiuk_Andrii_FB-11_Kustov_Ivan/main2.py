def IndexVidpovidnosty(encoded_text):
    ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    j = 0
    sum = 0
    while j < len(ukrainian_alphabet):
        encoded_text_count = encoded_text.count(ukrainian_alphabet[j])
        sum = sum + (encoded_text_count * (encoded_text_count - 1))
        j = j + 1
    result = (1/(len(file_contents) * (len(file_contents)-1))) * sum
    return result


with open('text.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()

file_contents = file_contents.replace(",","")
file_contents = file_contents.replace("!","")
file_contents = file_contents.replace("?","")
file_contents = file_contents.replace("=","")
file_contents = file_contents.replace("-","")
file_contents = file_contents.replace("_","")
file_contents = file_contents.replace(".","")
file_contents = file_contents.replace(":","")
file_contents = file_contents.replace(";","")
file_contents = file_contents.replace("1","")
file_contents = file_contents.replace("2","")
file_contents = file_contents.replace("3","")
file_contents = file_contents.replace("4","")
file_contents = file_contents.replace("5","")
file_contents = file_contents.replace("6","")
file_contents = file_contents.replace("7","")
file_contents = file_contents.replace("8","")
file_contents = file_contents.replace("9","")
file_contents = file_contents.replace("0","")
file_contents = file_contents.replace(" ", "")
file_contents = file_contents.replace("'", "")
file_contents = file_contents.replace("\n", "")

print(f"Відкритий текст:",IndexVidpovidnosty(file_contents))


with open('encoded_output2.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()
print(f"Довжина ключа 2:",IndexVidpovidnosty(file_contents))

with open('encoded_output3.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()
print(f"Довжина ключа 3:",IndexVidpovidnosty(file_contents))

with open('encoded_output4.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()
print(f"Довжина ключа 4:",IndexVidpovidnosty(file_contents))

with open('encoded_output5.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()
print(f"Довжина ключа 5:",IndexVidpovidnosty(file_contents))

with open('encoded_output10.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()
print(f"Довжина ключа 10:",IndexVidpovidnosty(file_contents))

with open('encoded_output15.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()
print(f"Довжина ключа 15:",IndexVidpovidnosty(file_contents))

with open('encoded_output20.txt', 'r', encoding = 'utf-8') as file:
    file_contents = file.read()
    file_contents = file_contents.lower()
print(f"Довжина ключа 20:",IndexVidpovidnosty(file_contents))
