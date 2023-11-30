import re
import math
from collections import Counter
import pandas as pd

def preprocess_text(text, delete_space=False):
    # Заміна прописних літер на стрічні
    text = text.lower()

    # Вилучення всіх символів окрім текстових літер та пробілів
    text = re.sub(r'[^а-яё\s]', '', text)
    if delete_space:
        text = re.sub(r'\s+', '', text)
    # Заміна послідовностей пробілів на один пробіл
    else:
        text = re.sub(r'\s+', '_', text)

    return text

def calculate_frequencies(text):
    # Рахуємо частоти букв
    letter_freq = Counter(text)

    # Рахуємо біграми
    bigrams = [text[i:i+2] for i in range(0, len(text)-1, 1)]
    bigram_freq = Counter(bigrams)

    bigram_2 = [text[i:i+2] for i in range(0, len(text)-1, 2)]
    bigram_2_freq = Counter(bigram_2)

    return letter_freq, bigram_freq, bigram_2_freq

def calculate_entropy(probabilities, n=1):
    # Розрахунок ентропії за безпосереднім означенням
    entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
    return entropy/n

def calculate_redundancy(entropy, alphabet_size):
    redundancy = 1 - (entropy / math.log2(alphabet_size))
    return redundancy

def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=["Symbol", "Frequency"])
    df["Frequency"] = df["Frequency"].apply(lambda x: f"{x:.8f}")
    df.to_excel(filename, index=False)

def redundancy_task(left_entropy, right_entropy, symbol):
    left_r = calculate_redundancy(left_entropy, 31)
    right_r = calculate_redundancy(right_entropy, 31)
    print(f"{left_r} < {symbol} < {right_r}")

def program(text, extension):

    with open(f"text_edited{extension}.txt", 'w', encoding='utf-8') as file:
        file.write(text)
        print(f"Edited text written in text_edited{extension}.txt")
    # Обчислюємо частоти букв і біграм в тексті
    letter_freq, bigram_freq, bigram_2_freq = calculate_frequencies(text)

    # Виводимо частоти букв у порядку спадання
    sorted_letter_freq = dict(sorted(letter_freq.items(), key=lambda x: x[1], reverse=True))
    sorted_bigram_freq = dict(sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True))
    sorted_bigram_2_freq = dict(sorted(bigram_2_freq.items(), key=lambda x: x[1], reverse=True))

    total_characters = len(text)

    # Виводимо частоти букв відносно всіх символів
    letter_data = [(letter, freq / total_characters) for letter, freq in sorted_letter_freq.items()]

    # Зберігаємо частоти букв в Excel
    save_to_excel(letter_data, f"letter_frequencies{extension}.xlsx")

    # Обчислюємо загальну кількість біграм в тексті
    total_bigrams_in_text = sum(bigram_freq.values())

    # Виводимо частоти біграм відносно всіх біграмів
    bigram_data = [(bigram, freq / total_bigrams_in_text) for bigram, freq in sorted_bigram_freq.items()]

    # Зберігаємо частоти біграм в Excel
    save_to_excel(bigram_data, f"bigram_frequencies{extension}.xlsx")

    # Обчислюємо загальну кількість біграм2 в тексті
    total_bigram_2_freq = sum(bigram_2_freq.values())

    # Виводимо частоти біграм відносно всіх біграмів
    bigram_2_data = [(bigram, freq / total_bigram_2_freq) for bigram, freq in sorted_bigram_2_freq.items()]

    # Зберігаємо частоти біграм, що не перетинаються, в Excel
    save_to_excel(bigram_2_data, f"bigram_2_frequencies{extension}.xlsx")

    # Обчислюємо імовірності букв і біграм
    letter_probabilities = {letter: freq/total_characters for letter, freq in letter_freq.items()}
    bigram_probabilities = {bigram: freq/total_bigrams_in_text for bigram, freq in bigram_freq.items()}
    bigram_2_probabilities = {bigram: freq/total_bigram_2_freq for bigram, freq in bigram_2_freq.items()}

    # Обчислюємо ентропію H1 і H2
    entropy_h1 = calculate_entropy(list(letter_probabilities.values()))
    entropy_h2 = calculate_entropy(list(bigram_probabilities.values()), 2)
    entropy_2_h2 = calculate_entropy(list(bigram_2_probabilities.values()), 2)

    r1 = calculate_redundancy(entropy_h1, 33)
    r2 = calculate_redundancy(entropy_h2, 33)
    r2_2 = calculate_redundancy(entropy_2_h2, 33)

    print(f'Ентропія H1: {entropy_h1}   Надлишковість R1: {r1}')
    print(f'Ентропія H2: {entropy_h2}   Надлишковість R2: {r2}')
    print(f'Ентропія H2_2: {entropy_2_h2}   Надлишковість R2_2: {r2_2}')

# Зчитуємо текст з файлу
with open('my_text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Попередня обробка тексту
text_w_space = preprocess_text(text)
text_w_nospace = preprocess_text(text, True)

print("Text with space:")
program(text_w_space, "_w_space")
print("\nText without space:")
program(text_w_nospace, "_no_space")

print("\nCalculate redundancy")
redundancy_task(2.40914871605956, 3.18660852753104, "H^(10)")
redundancy_task(1.63863918745959, 2.41299174943185, "H^(20)")
redundancy_task(1.98026977879394, 2.71433428621155, "H^(30)")