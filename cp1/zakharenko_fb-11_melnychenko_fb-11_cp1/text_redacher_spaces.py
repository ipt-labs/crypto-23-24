alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя '

with open('text.txt', 'r', encoding='utf-8') as f:
    text = f.read().lower()

result = ''
for i in text:
    if i in alphabet:
        result += i
    if i == '\n':
        result += ' '
    if i == 'ъ':
        result += 'ь'

with open('spaces_text.txt', 'w', encoding='utf-8') as nf:
    nf.write(" ".join(result.split()))

