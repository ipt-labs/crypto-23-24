import re

def preprocess_text(text):
    text = re.sub(r'[^а-яА-Я\s]', '', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('ё', 'е')
    text = text.replace('ъ', 'ь')
    return text

with open('Labs\Krypt_labs\Lab1\original.txt', encoding='utf-8') as file:
    text = file.read()

with open('Labs\Krypt_labs\Lab1\edited.txt', 'w', encoding='utf-8') as file:
    file.write(preprocess_text(text=text))

