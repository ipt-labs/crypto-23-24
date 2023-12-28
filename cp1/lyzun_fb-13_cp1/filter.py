import re

with open('unfiltered.txt', 'r', encoding='utf-8') as file:
    text = file.read()

text = text.lower()
text = text.replace('ё', 'е')
text = text.replace('ъ', 'ь')
text = text.replace('\n', ' ')
text = re.sub(r'[^а-яе ]', '', text)
text = re.sub(r'\s+', ' ', text)

with open('filtered.txt', 'w', encoding='utf-8') as file:
    file.write(text)

text = text.replace(' ', '')
with open('filtered_no_space.txt', 'w', encoding='utf-8') as file:
    file.write(text)