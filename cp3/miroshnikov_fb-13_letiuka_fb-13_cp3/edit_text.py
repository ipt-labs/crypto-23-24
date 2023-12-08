import re

def preprocess_text(text):
    text = re.sub(r'[^а-яА-Я\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('ё', 'е')
    text = text.replace('ъ', 'ь')
    text = text.replace(' ', '')
    text = text.lower()
    return text


with open(r'Labs\Crypt_labs\Lab3\var3_or.txt', encoding='utf-8') as file:
    text = file.read()

with open(r'Labs\Crypt_labs\Lab3\var3_edit.txt', 'w', encoding='utf-8') as file:
    file.write(preprocess_text(text=text))