import re
from collections import Counter
import math

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def preprocess_text(text):
    text = re.sub(fr'[^{alphabet}\s]', ' ', text.lower())
    return re.sub(r'\s+', ' ', text)

def calculate_frequency(items, total_count):
    return {item: count / total_count for item, count in items.items()}

def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def calculate_redundancy(h0, h_inf):
    return 1 - (h_inf / h0)

def count_and_print_frequency(items, label):
    total_count = sum(items.values())
    frequency = calculate_frequency(items, total_count)
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

    print(f"\nЧастота появи {label} :")
    for item, freq in sorted_frequency:
        print(f"{item}: {freq:.7f}")

    return frequency


file_path = 'text.txt'

with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

preprocessed_text = preprocess_text(text)
preprocessed_text_no_spaces = ''.join(preprocessed_text.split())

# Частота букв
frequency_with_spaces = count_and_print_frequency(Counter(preprocessed_text), "букв з пробілами")
frequency_without_spaces = count_and_print_frequency(Counter(filter(lambda x: x in alphabet, preprocessed_text)),"букв без пробілів")

# Частота біграмм
frequency_bigram_with_spaces = count_and_print_frequency(Counter(zip(preprocessed_text, preprocessed_text[1:])),"біграм з пробілом")
frequency_bigram_without_spaces = count_and_print_frequency(Counter(zip(preprocessed_text_no_spaces, preprocessed_text_no_spaces[1:])), "біграм без пробіла")
frequency_bigram_step_2_with_spaces = count_and_print_frequency(Counter(zip(preprocessed_text[::2], preprocessed_text[1::2])), "біграм з пробілом с шагом 2")
frequency_bigram_non_overlapping_without_spaces = count_and_print_frequency(Counter(zip(preprocessed_text_no_spaces[::2], preprocessed_text_no_spaces[1::2])), "біграм без пробіла з шагом 2")

# Ентропія і надлишковість
entropy_h1_with_spaces = calculate_entropy(frequency_with_spaces.values())
entropy_h1_without_spaces = calculate_entropy(frequency_without_spaces.values())

entropy_h2_with_spaces = calculate_entropy(frequency_bigram_with_spaces.values()) / 2
entropy_h2_without_spaces = calculate_entropy(frequency_bigram_without_spaces.values()) / 2

entropy_h2_step_2_with_spaces = calculate_entropy(frequency_bigram_step_2_with_spaces.values()) / 2
entropy_h2_non_overlapping_without_spaces = calculate_entropy(frequency_bigram_non_overlapping_without_spaces.values()) / 2

redundancy_h1_with_spaces = calculate_redundancy(math.log2(34), entropy_h1_with_spaces)
redundancy_h1_without_spaces = calculate_redundancy(math.log2(33), entropy_h1_without_spaces)

redundancy_h2_with_spaces = calculate_redundancy(math.log2(34), entropy_h2_with_spaces)
redundancy_h2_without_spaces = calculate_redundancy(math.log2(33), entropy_h2_without_spaces)

redundancy_h2_step_2_with_spaces = calculate_redundancy(math.log2(34),entropy_h2_step_2_with_spaces)
redundancy_h2_non_overlapping_without_spaces = calculate_redundancy(math.log2(33),entropy_h2_non_overlapping_without_spaces)

# Результати
print("\nЕнтропія H1:")
print(f"З пробілами: {entropy_h1_with_spaces:.7f}")
print(f"Без пробілів: {entropy_h1_without_spaces:.7f}")

print("\nЕнтропія H2:")
print(f"З пробілами: {entropy_h2_with_spaces:.7f}")
print(f"Без пробілів: {entropy_h2_without_spaces:.7f}")
print(f"З пробілами і з шагом 2: {entropy_h2_step_2_with_spaces:.7f}")
print(f"Без пробілів і з шагом 2: {entropy_h2_non_overlapping_without_spaces:.7f}")

print("\nНадлишковість R:")
print(f"H1 З пробілами: {redundancy_h1_with_spaces:.7f}")
print(f"H1 Без пробілів: {redundancy_h1_without_spaces:.7f}")

print(f"H2 з пробілами: {redundancy_h2_with_spaces:.7f}")
print(f"H2 без пробілів: {redundancy_h2_without_spaces:.7f}")
print(f"H2 з пробілами і з шагом 2: {redundancy_h2_step_2_with_spaces:.7f}")
print(f"H2 без пробілів і з шагом 2: {redundancy_h2_non_overlapping_without_spaces:.7f}")
