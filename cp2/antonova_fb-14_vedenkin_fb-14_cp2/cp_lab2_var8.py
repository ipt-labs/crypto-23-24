from collections import Counter
import matplotlib.pyplot as plt

with open('text_var8.txt', 'r', encoding='utf-8') as file:
    encrypted_text = file.read()

alph = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

def calculate_index_of_coincidence(text):
    total_chars = len(text)
    if total_chars < 2:
        return 0  # Повертаємо 0 для тексту з менше ніж 2 символами
    letter_counts = Counter(text)
    index = sum(n * (n - 1) for n in letter_counts.values()) / (total_chars * (total_chars - 1))
    return index

results = {}

for key_length in range(2, 33):
    blocks = [encrypted_text[i::key_length] for i in range(key_length)]

    # Обчислюємо індекс відповідності для кожного блоку
    block_index_of_coincidence = [calculate_index_of_coincidence(block) for block in blocks]

    average_index = sum(block_index_of_coincidence) / len(block_index_of_coincidence)
    results[key_length] = average_index

for key_length, index in results.items():
    print(f'Довжина ключа: {key_length}, Індекс відповідності: {index}')

best_key = max(results, key=results.get) 
print('Довжина нашого ключа: ', best_key)   


x = list(results.keys())
y = list(results.values())

plt.bar(x, y, color='red')
plt.xlabel('Довжина ключа')
plt.ylabel('Індекс відповідності')
plt.title('Індекси відповідності для різних довжин ключів')
plt.show()

def vigenere_decrypt(encrypted_text, key):
    decrypted_text = []

    for i, char in enumerate(encrypted_text):
        if char in alph:
            shift = alph.index(key[i % len(key)])
            decrypted_char_index = (alph.index(char) - shift) % len(alph)
            decrypted_text.append(alph[decrypted_char_index])
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)

    
blocks = [encrypted_text[i::best_key] for i in range(best_key)]

most_likely_letter = 'о'
alph2 = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

k = ''
for block in blocks:
    y = alph2.index(Counter(block).most_common()[0][0])
    x = alph2.index(most_likely_letter)
    k = k + (alph2[y-x])
print(k)
print(vigenere_decrypt(encrypted_text, k))