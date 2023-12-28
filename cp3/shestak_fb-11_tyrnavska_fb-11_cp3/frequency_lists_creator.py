import text_manipulator
from collections import defaultdict
import csv


alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


# counting frequency of each letter
def letters_frequency(input_path, output_path, space=False):
    text = text_manipulator.get_text(input_path)
    frequencies = defaultdict()
    for l in alphabet:
        frequencies[l] = text.count(l) / len(text)
    if space:
        frequencies[" "] = text.count(" ") / len(text)
    sorted_frequencies = sorted(frequencies.items(), key=lambda i: i[1], reverse=True)
    with open(output_path, 'a', encoding="UTF-8") as writer:
        for k, v in sorted_frequencies:
            res = f'{k},{v}\n'
            writer.write(res)


# counting frequency for each bigram
def bigrams_frequency(input_path, output_path, step):
    bigrams = set()
    text = text_manipulator.get_text(input_path)
    frequencies = defaultdict()

    for l in range(0, len(text) - 1, step):
        full_l = text[l:l + 2]
        bigrams.add(full_l)

    for b in bigrams:
        frequencies[b.replace(" ", "_")] = text.count(b) / len(text)
    sorted_frequencies = sorted(frequencies.items(), key=lambda i: i[1], reverse=True)

    with open(output_path, 'w', encoding="UTF-8") as writer:
        n = 0
        for k, v in sorted_frequencies:
            n += 1
            if n == 6:
                break
            res = f'{k},{v}\n'
            writer.write(res)


# get frequency dict
def get_frequency(input_path):
    res_dict = {}
    with open(input_path, mode='r', newline='', encoding="UTF-8") as file:
        reader = csv.reader(file)
        for row in reader:
            res_dict[row[0]] = row[1]

    return res_dict


if __name__ == '__main__':
    # counting frequency of each letter
    # with spaces
    letters_frequency('valid_text_with_spaces.txt', 'output/letters_frequency_with_spaces.csv', space=True)
    # without spaces
    letters_frequency('valid_text_without_spaces.txt', 'output/letters_frequency_without_spaces.csv')

    # counting frequency for each overlapping bigram
    # with spaces
    bigrams_frequency('valid_text_with_spaces.txt', 'output/overlapping_bigrams_frequency_with_spaces.csv', 1)
    # without spaces
    bigrams_frequency('valid_text_without_spaces.txt', 'output/overlapping_bigrams_frequency_without_spaces.csv', 1)

    # counting frequency for each non-overlapping bigram
    # with spaces
    bigrams_frequency('valid_text_with_spaces.txt', 'output/non_overlapping_bigrams_frequency_with_spaces.csv', 2)
    # without spaces
    bigrams_frequency('valid_text_without_spaces.txt', 'output/non_overlapping_bigrams_frequency_without_spaces.csv', 2)
