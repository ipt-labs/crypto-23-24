import string
import re
from collections import Counter
from math import log

# Функція для підрахунку частот букв в тексті
def calculate_letter_frequencies(text):
    text = re.sub(r'[^а-яё]', ' ', text.lower())  # Видалити всі символи, крім російських букв та пробілів
    letter_frequencies = Counter(text)
    total_letters = len(text)
    letter_probabilities = {letter: count / total_letters for letter, count in letter_frequencies.items()}
    sorted_probabilities = dict(sorted(letter_probabilities.items(), key=lambda x: x[1], reverse=True))
    return sorted_probabilities

# Функція для підрахунку частот біграм в тексті та створення матриці частот
def calculate_bigram_frequencies(text):
    text = re.sub(r'[^а-яё ]', ' ', text.lower())
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    bigram_frequencies = Counter(bigrams)
    total_bigrams = len(bigrams)

    # Створення матриці частот біграм
    alphabet = list(" абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    bigram_matrix = [[0] * len(alphabet) for _ in range(len(alphabet))]

    for bigram, count in bigram_frequencies.items():
        first_letter, second_letter = bigram
        first_index = alphabet.index(first_letter)
        second_index = alphabet.index(second_letter)
        bigram_matrix[first_index][second_index] = count / total_bigrams

    return bigram_matrix, alphabet

# Функція для підрахунку частот біграм без перетинів в тексті та створення матриці частот
def calculate_non_overlapping_bigrams(text):
    text = re.sub(r'[^а-яё]', ' ', text.lower())  
    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, 2)]  
    bigram_frequencies_non_overlapping = Counter(bigrams)
    total_bigrams_non_overlapping = len(bigrams)

    # Створення матриці частот біграм
    alphabet_non_overlapping = list(" абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    bigram_matrix_non_overlapping = [[0] * len(alphabet_non_overlapping) for _ in range(len(alphabet_non_overlapping))]

    for bigram, count in bigram_frequencies_non_overlapping.items():
        first_letter, second_letter = bigram
        first_index = alphabet_non_overlapping.index(first_letter)
        second_index = alphabet_non_overlapping.index(second_letter)
        bigram_matrix_non_overlapping[first_index][second_index] = count / total_bigrams_non_overlapping

    return bigram_matrix_non_overlapping, alphabet_non_overlapping

# Функція для підрахунку частот біграм без перетинів в тексті без пробілів та створення матриці частот
def calculate_non_overlapping_no_spaces_bigrams(text):
    text = re.sub(r'[^а-яё]', '', text.lower())  
    bigrams = [text[i:i+2] for i in range(0, len(text) - 1, 2)]  
    bigram_frequencies_non_overlapping_no_spaces = Counter(bigrams)
    total_bigrams_non_overlapping_no_spaces = len(bigrams)

    # Створення матриці частот біграм
    alphabet_non_overlapping_no_spaces = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    bigram_matrix_non_overlapping_no_spaces = [[0] * len(alphabet_non_overlapping_no_spaces) for _ in range(len(alphabet_non_overlapping_no_spaces))]

    for bigram, count in bigram_frequencies_non_overlapping_no_spaces.items():
        first_letter, second_letter = bigram
        first_index = alphabet_non_overlapping_no_spaces.index(first_letter)
        second_index = alphabet_non_overlapping_no_spaces.index(second_letter)
        bigram_matrix_non_overlapping_no_spaces[first_index][second_index] = count / total_bigrams_non_overlapping_no_spaces

    return bigram_matrix_non_overlapping_no_spaces, alphabet_non_overlapping_no_spaces


# Функція для підрахунку частот біграм в тексті без пробілів та створення матриці частот
def calculate_bigram_frequencies_no_spaces(text):
    text = re.sub(r'[^а-яё]', '', text.lower())  # Вилучити всі символи, крім російських букв
    bigrams = [text[i:i+2] for i in range(len(text) - 1)]
    bigram_frequencies_no_spaces = Counter(bigrams)
    total_bigrams_no_spaces = len(bigrams)

    # Створення матриці частот біграм
    alphabet_no_spaces = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    bigram_matrix_no_spaces = [[0] * len(alphabet_no_spaces) for _ in range(len(alphabet_no_spaces))]

    for bigram, count in bigram_frequencies_no_spaces.items():
        first_letter, second_letter = bigram
        first_index = alphabet_no_spaces.index(first_letter)
        second_index = alphabet_no_spaces.index(second_letter)
        bigram_matrix_no_spaces[first_index][second_index] = count / total_bigrams_no_spaces

    return bigram_matrix_no_spaces, alphabet_no_spaces


# Функція для обчислення значення H1 за безпосереднім визначенням
def calculate_h1(probabilities):
    return -sum(prob * log(prob, 2) for prob in probabilities.values())

# Функція для обчислення значення H2 за безпосереднім визначенням
def calculate_h2(bigram_matrix):
    h2 = 0.0
    for row in bigram_matrix:
        for prob in row:
            if prob > 0:
                h2 -= (prob * log(prob, 2))/2
    return h2

# Зчитування тексту з файлу
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        text = file.read()
    return text

# Задайте шлях до файлу, який містить текст
file_path = 'H:\web\Te.txt'

# Зчитайте текст з файлу
text = read_text_from_file(file_path)

# Обчислення H0 для текстів з пробілами
h0 = log(34, 2)

# Обчислення H0 для текстів з пробілами
h0_no_spaces = log(33, 2)

# Обчислення частот букв та біграм
letter_probabilities = calculate_letter_frequencies(text)
bigram_matrix, unique_bigrams = calculate_bigram_frequencies(text)
h1 = calculate_h1(letter_probabilities)
h2 = calculate_h2(bigram_matrix)

print("Частоти букв (відсортовані за спаданням):")
for letter, probability in letter_probabilities.items():
    print(f"{letter}: {probability:.4f}")
print("\nH1: ",h1)
print("\nR: ", 1 - (h1/h0))

print("\nМатриця частот біграм з перетинами:")
print("   " + " ".join(unique_bigrams))
for i, row in enumerate(bigram_matrix):
    print(f"{unique_bigrams[i]} " + " ".join([f"{prob:.4f}" for prob in row]))
print("\nH2 (з перетинами)",h2)
print("\nR: ", 1 - (h2/h0))
text_without_spaces = text.replace(" ", "")

# Обчислення H1 та H2 на тексті без пробілів
letter_probabilities_no_spaces = calculate_letter_frequencies(text_without_spaces)
bigram_matrix_no_spaces, unique_bigrams_no_spaces = calculate_bigram_frequencies_no_spaces(text_without_spaces)
h1_no_spaces = calculate_h1(letter_probabilities_no_spaces)
h2_no_spaces = calculate_h2(bigram_matrix_no_spaces)

#print("\nТекст без пробілів:")
#print(text_without_spaces)
print("Частоти букв (відсортовані за спаданням):")
for letter, probability in letter_probabilities_no_spaces.items():
    print(f"{letter}: {probability:.4f}")
print("\nH1 (без пробілів):", h1_no_spaces)
print("\nR: ", 1 - (h1_no_spaces/h0_no_spaces))
print("\nМатриця частот біграм з перетинами без пробілів:")
print("   " + " ".join(unique_bigrams_no_spaces))
for i, row in enumerate(bigram_matrix_no_spaces):
    print(f"{unique_bigrams_no_spaces[i]} " + " ".join([f"{prob:.4f}" for prob in row]))
print("H2 (без пробілів з перетинами):", h2_no_spaces)
print("\nR: ", 1 - (h2_no_spaces/h0_no_spaces))

# Обчислення частот біграм без перетинів
bigram_matrix_non_overlapping, unique_bigrams_non_overlapping = calculate_non_overlapping_bigrams(text)
h2_non_overlapping = calculate_h2(bigram_matrix_non_overlapping)

print("\nМатриця частот біграм без перетинів:")
print("   " + " ".join(unique_bigrams_non_overlapping))
for i, row in enumerate(bigram_matrix_non_overlapping):
    print(f"{unique_bigrams_non_overlapping[i]} " + " ".join([f"{prob:.4f}" for prob in row]))
print("H2 (без перетинів):", h2_non_overlapping)
print("\nR: ", 1 - (h2_non_overlapping/h0))

# Обчислення частот біграм без перетинів та без пробілів
bigram_matrix_non_overlapping_no_spaces, unique_bigrams_non_overlapping_no_spaces = calculate_non_overlapping_no_spaces_bigrams(text)
h2_non_overlapping_no_spaces = calculate_h2(bigram_matrix_non_overlapping_no_spaces) 

print("\nМатриця частот біграм без перетинів та без пробілів:")
print("   " + " ".join(unique_bigrams_non_overlapping_no_spaces))
for i, row in enumerate(bigram_matrix_non_overlapping_no_spaces):
    print(f"{unique_bigrams_non_overlapping_no_spaces[i]} " + " ".join([f"{prob:.4f}" for prob in row]))
print("H2 (без перетинів та без пробілів):", h2_non_overlapping_no_spaces)
print("\nR: ", 1 - (h2_non_overlapping_no_spaces/h0_no_spaces))

