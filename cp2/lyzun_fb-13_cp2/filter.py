import re

with open('unfiltered.txt', 'r', encoding='utf-8') as file:
    text = file.read()

text = text.lower()
text = text.replace('ё', 'е')
text = text.replace('ъ', 'ь')
text = text.replace('\n', ' ')
text = re.sub(r'[^а-яе ]', '', text)
text = text.replace(' ', '')
with open('filtered.txt', 'w', encoding='utf-8') as file:
    file.write(text)