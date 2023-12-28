import math
from collections import Counter

def is_letter_in_alf(letter):
    return letter in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def is_letter_in_bigram(bigram):
    return all(is_letter_in_alf(letter) for letter in bigram)

def calculate_letter_frequencies(text):
    text = text.lower()
    letter_count = Counter(letter for letter in text if is_letter_in_alf(letter) or letter == ' ')
    total_letters_count = sum(letter_count.values())
    letter_frequencies = {letter: count / total_letters_count for letter, count in letter_count.items()}
    return letter_frequencies

def calculate_bigram_frequencies(text,step = 1):
    text = text.lower()
    bigram_count = Counter([text[i:i + 2] for i in range(0, len(text) - 1, step) if is_letter_in_bigram(text[i:i + 2])])
    total_bigram_count = sum(bigram_count.values())
    bigram_frequencies = {bigram: count / total_bigram_count for bigram, count in bigram_count.items()}
    return bigram_frequencies

def calculate_entropy(probabilities):
    return -sum(p * (0 if p == 0 else math.log2(p)) for p in probabilities.values())

def remove_spaces(text):
    return ''.join(text.split())

# Зчитування тексту з файлу
file_path = r'C:\Users\alexd\Desktop\tekstnew.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Видалення пробілів з тексту
text_without_spaces = remove_spaces(text)

# Підрахунок частот букв та біграм та виведення їх
letter_probabilities = calculate_letter_frequencies(text)
letter_probabilities_no_spaces = calculate_letter_frequencies(text_without_spaces)

non_overlapping_bigram_probabilities_no_spaces = calculate_bigram_frequencies(text_without_spaces,2)
non_overlapping_bigram_probabilities = calculate_bigram_frequencies(text,2)

overlapping_bigram_probabilities_no_spaces = calculate_bigram_frequencies(text_without_spaces)
overlapping_bigram_probabilities = calculate_bigram_frequencies(text)

print("Частоти букв з пробілами:")
for letter, probability in letter_probabilities.items():
    print(f"{letter}: {probability:.6f}")

print("Частоти букв без пробілів:")
for letter, probability in letter_probabilities_no_spaces.items():
    print(f"{letter}: {probability:.6f}")

print("\nЧастоти біграм з перетином та пробілами:")
for bigram, probability in overlapping_bigram_probabilities.items():
    print(f"{bigram}: {probability:.6f}")

print("Частоти біграм з перетином без пробілів:")
for bigram, probability in overlapping_bigram_probabilities_no_spaces.items():
    print(f"{bigram}: {probability:.6f}")

print("\nЧастоти біграм без перетину з пробілами:")
for bigram, probability in non_overlapping_bigram_probabilities.items():
    print(f"{bigram}: {probability:.6f}")

print("Частоти біграм без перетину без пробілів:")
for bigram, probability in non_overlapping_bigram_probabilities_no_spaces.items():
    print(f"{bigram}: {probability:.6f}")

# Підрахунок H1 і H2 за безпосереднім означенням
H1 = calculate_entropy(letter_probabilities)
H1_no_spaces = calculate_entropy(letter_probabilities_no_spaces)

H2_overlapping_no_spaces = calculate_entropy(overlapping_bigram_probabilities_no_spaces)/2
H2_overlapping = calculate_entropy(overlapping_bigram_probabilities)/2
H2_non_overlapping = calculate_entropy(non_overlapping_bigram_probabilities)/2
H2_non_overlapping_no_spaces = calculate_entropy(non_overlapping_bigram_probabilities_no_spaces)/2

print(f"\nH1 (Ентропія букв з пробілами): {H1}")
print(f"H1 (Ентропія букв без пробілів): {H1_no_spaces}")
print(f"H2 (Ентропія біграм з перетином та пробілами): {H2_overlapping}")
print(f"H2 (Ентропія біграм з перетином без пробілів): {H2_overlapping_no_spaces}")
print(f"H2 (Ентропія біграм без перетину з пробілами): {H2_non_overlapping}")
print(f"H2 (Ентропія біграм без перетину без пробілів): {H2_non_overlapping_no_spaces}")