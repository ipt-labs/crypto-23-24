from collections import Counter
from math import log2
import csv


# Алфавіти
ALPHABET: str = 'абвгдежзийклмнопрстуфхцчшщыьэюя '
ALPHABET_NO_SPACE: str = 'абвгдежзийклмнопрстуфхцчшщыьэюя'


# Ця функція зчитує текстовий файл та поверає string з текстом цього файлу
def file_read(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        text: str = file.read()
    return text


# Ця функція отримує текст та повертає редагований текст для подальшого аналізу
def text_edit(text: str) -> str:
    text = text.replace('ё', 'е')
    text = text.replace('ъ', 'ь')
    text = text.lower()
    text = ''.join(char for char in text if char in ALPHABET)
    return text


# Ця фунція видаляє пробіли у тексті
def space_remove(text: str) -> str:
    text = text.replace(' ', '')
    return text


# Ця функція повертає dict з кількістю символів у тексті
def char_count(text: str) -> Counter:
    character_dict: Counter = Counter(text)
    return character_dict


# Ця функція повертає dict з частотою появи літер
def char_frequency(character_dict: Counter, text: str) -> dict:
    frequency_dict = {}
    for char in character_dict:
        frequency_dict[char] = character_dict.get(char)/len(text)
    return frequency_dict


# Ця функція створює dict з біграмами, що перетинаються/не перетинаються та кількістью цих біграм
def bigram_create(text: str, step: int) -> dict:
    bigram_dict: dict = {}
    for i in range(0, len(text), step):
        bigram = text[i:i+2]
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    return bigram_dict


# Ця функція повертає dict з частотою появи біграм
def bigram_frequency(bigram_dict: dict) -> dict:
    frequency_dict: dict = {}
    bigram_count: int = 0
    for value in bigram_dict.values():
        bigram_count += value
    for bigram in bigram_dict:
        frequency_dict[bigram] = bigram_dict[bigram]/bigram_count
    return frequency_dict


# Ця функція рахує ентропію
def entropy(frequency_dict: dict, bigram: bool) -> float:
    entropy_value: float = 0
    for value in frequency_dict.values():
        entropy_value += -(value * log2(value))
    if bigram:
        entropy_value /= 2
    return entropy_value


# Ця функція створює csv файл з результатами
def create_csv_file(filename: str, count_dict: dict, frequency_dict: dict):
    with open(filename, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Символ(и)", "Кількість", "Частота"])
        for item in frequency_dict:
            item = str(item)
            count = count_dict[item]
            frequency = frequency_dict[item]
            writer.writerow([str(item), count, frequency])


# Ця функція рахує надлишковість
def redundancy(entropy_value: float, alph: str) -> float:
    redundancy_value = 1 - (entropy_value/log2(len(alph)))
    return redundancy_value


def main():
    text = file_read('text.txt')
    text = text_edit(text)
    text_no_space = space_remove(text)

    entropy_h1_spaces = entropy(char_frequency(char_count(text), text), bigram=False)
    redundancy_h1_spaces = redundancy(entropy_h1_spaces, ALPHABET)

    entropy_h1_no_spaces = entropy(char_frequency(char_count(text_no_space), text_no_space), bigram=False)
    redundancy_h1_no_spaces = redundancy(entropy_h1_no_spaces, ALPHABET_NO_SPACE)

    entropy_h2_s1_spaces = entropy(bigram_frequency(bigram_create(text, step=1)), bigram=True)
    redundancy_h2_s1_spaces = redundancy(entropy_h2_s1_spaces, ALPHABET)

    entropy_h2_s1_no_spaces = entropy(bigram_frequency(bigram_create(text_no_space, step=1)), bigram=True)
    redundancy_h2_s1_no_spaces = redundancy(entropy_h2_s1_no_spaces, ALPHABET_NO_SPACE)

    entropy_h2_s2_spaces = entropy(bigram_frequency(bigram_create(text, step=2)), bigram=True)
    redundancy_h2_s2_spaces = redundancy(entropy_h2_s2_spaces, ALPHABET)

    entropy_h2_s2_no_spaces = entropy(bigram_frequency(bigram_create(text_no_space, step=2)), bigram=True)
    redundancy_h2_s2_no_spaces = redundancy(entropy_h2_s2_no_spaces, ALPHABET_NO_SPACE)
    print('------------------------------')
    print(f"Ентропія для літер з пробілом: {entropy_h1_spaces}")
    print(f"Надлишковість для літер з пробілом: {redundancy_h1_spaces}")
    create_csv_file("Mono_space.csv", char_count(text),
                    (char_frequency(char_count(text), text)))
    print('------------------------------')
    print(f'Ентропія для літер без пробілу: {entropy_h1_no_spaces}')
    print(f'Надлишковість для літер без пробілу: {redundancy_h1_no_spaces}')
    create_csv_file("Mono_no_space.csv", char_count(text_no_space),
                    (char_frequency(char_count(text_no_space), text_no_space)))
    print('------------------------------')
    print(f'Ентропія біграм з пробілом, які перетинаються: {entropy_h2_s1_spaces}')
    print(f'Надлишковість біграм з пробілом, які перетинаються: {redundancy_h2_s1_spaces}')
    create_csv_file("Bi_step1_space.csv", bigram_create(text, step=1),
                    bigram_frequency(bigram_create(text, step=1)))
    print('------------------------------')
    print(f'Ентропія біграм без пробілу, які перетинаються: {entropy_h2_s1_no_spaces}')
    print(f'Надлишковість біграм без пробілу, які перетинаються: {redundancy_h2_s1_no_spaces}')
    create_csv_file("Bi_step1_no_space.csv", bigram_create(text_no_space, step=1),
                    bigram_frequency(bigram_create(text_no_space, step=1)))
    print('------------------------------')
    print(f'Ентропія біграм з пробілом, які не перетинаються: {entropy_h2_s2_spaces}')
    print(f'Надлишковість біграм з пробілом, які не перетинаються: {redundancy_h2_s2_spaces}')
    create_csv_file("Bi_step2_space.csv", bigram_create(text, step=2),
                    bigram_frequency(bigram_create(text, step=2)))
    print('------------------------------')
    print(f'Ентропія біграм без пробілу, які не перетинаються: {entropy_h2_s2_no_spaces}')
    print(f'Надлишковість біграм без пробілу, які не перетинаються: {redundancy_h2_s2_no_spaces}')
    create_csv_file("Bi_step2_no_space.csv", bigram_create(text_no_space, step=2),
                    bigram_frequency(bigram_create(text_no_space, step=2)))
    print('------------------------------')


if __name__ == "__main__":
    main()
