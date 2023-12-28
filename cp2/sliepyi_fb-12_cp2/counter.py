import numpy as np

def count_letters_and_length(text):
    letter_count = {}
    text_length = len(text)

    for char in text:
        if char.isalpha():
            char = char.lower()
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1

    return letter_count, text_length

def read_text_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def calculate_coincidence_index(letter_count, text_length):
    counts = np.array(list(letter_count.values()))
    coincidence_sum = np.sum(counts * (counts - 1))
    index_of_coincidence = coincidence_sum / (text_length * (text_length - 1))
    return index_of_coincidence

if __name__ == "__main__":
    file_name = 'variant.txt' 
    text = read_text_from_file(file_name)
    letter_count, text_length = count_letters_and_length(text)
    print(f"Кількість появи кожної літери:")
    for letter, count in letter_count.items():
        print(f"'{letter}': {count} разів")
    print(f"Загальна довжина тексту: {text_length} символів")
    index_of_coincidence = calculate_coincidence_index(letter_count, text_length)
    print(f"Індекс відповідності: {index_of_coincidence:.12}")
