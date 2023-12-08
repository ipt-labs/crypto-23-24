from collections import Counter

with open("C:\\Users\\Polya\\Desktop\\KPI\\crypto\\crypto-23-24\\cp2\\gogoleva_fb-12_cp2\\decode.txt", "r", encoding="cp1251") as file:
    text = file.read()

block_count = 16
blocks = [""] * block_count
block_index = 0

for char in text:
    blocks[block_index] += char
    block_index = (block_index + 1) % block_count

result = ""

for i, block in enumerate(blocks):
    # Рахуємо частоту літер у блоку
    letter_counts = Counter(block)
    most_common_letter = letter_counts.most_common(1)[0][0]  # Найчастіше зустрічаючася літера

    # Визначаємо номер літери в російському алфавіті
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    
    letter_index = alphabet.index(most_common_letter)

    # Віднімаємо 14 (номер літери "О") і виводимо відповідну букву
    decoded_letter_index = (letter_index - 14) % len(alphabet)
    decoded_letter = alphabet[decoded_letter_index]
    
    result += decoded_letter

print(result)
