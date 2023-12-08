from collections import Counter

def most_common_letter(text):
    letter_counts = Counter(char.lower() for char in text if char.isalpha())
    most_common = letter_counts.most_common(1)[0][0]
    return most_common


with open("9var.txt", "r", encoding="utf-8") as file:
    text = file.read()

blocks = [[] for _ in range(17)]
for i, char in enumerate(text):
    block_index = i % 17
    blocks[block_index].append(char)

most_common_letters = []

for block in blocks:
    block_text = ''.join(block)
    most_common = most_common_letter(block_text)
    most_common_letters.append(most_common)

for i, letter in enumerate(most_common_letters):
    print(f"Найчастіше в блоці {i + 1}: {letter}")