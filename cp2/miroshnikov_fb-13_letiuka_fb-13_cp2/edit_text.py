import re

def preprocess_text(text):
    text = re.sub(r'[^а-яА-Я\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('ё', 'е')
    text = text.lower()
    return text

with open(r'Labs\Crypt_labs\Lab2\var3.txt', encoding='utf-8') as file:
    text = file.read()

with open(r'Labs\Crypt_labs\Lab2\var3_edit.txt', 'w', encoding='utf-8') as file:
    file.write(preprocess_text(text=text))
