from collections import Counter
import math
import pandas as pd
#correct one

def file_read(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def remove_spaces(text):
    return text.replace(' ', '')

# def remove_spaces(text):
#     new_text = ''
#     for char in text:
#         if char != ' ':
#             new_text += char
#     text = new_text
#     return text

def filter_text(text):
    text = text.lower()
    filtered_text = ""
    for char in text:
        if 'а' <= char <= 'я' or char == ' ':
            if char == 'ё':
                char = 'е'
            if char == 'ъ':
                char = 'ь'
            filtered_text += char
    filtered_text = ' '.join(filtered_text.split())
    return filtered_text

def count_monograms(text):
    total_chars = len(text)
    monograms = Counter(text)
    monograms_freq = {char: count / total_chars for char, count in monograms.items()}
    entropy = -sum(p*math.log2(p) for p in monograms_freq.values())
    redundancy = 1 - (entropy / math.log2(len(monograms_freq)))
    print(f"{'Monogram'} - {'Frequency'}")
    for monogram, freq in monograms_freq.items():
        print(f'{monogram:<5}  {freq}')
    return entropy, redundancy


def count_bigrams(text, include_overlaps, include_spaces):
    total_bigrams = len(text) - 1
    if include_overlaps:
        bigrams = [text[i:i + 2] for i in range(total_bigrams)]
    else:
        bigrams = [text[i:i + 2] for i in range(0, total_bigrams, 2)]
    if not include_spaces:
        bigrams = [bigram for bigram in bigrams if ' ' not in bigram]
    bigram_count = Counter(bigrams)
    bigram_freq = {bigram: count / total_bigrams for bigram, count in bigram_count.items() }
    entropy = -sum(p*math.log2(p) for p in bigram_freq.values())
    entropy = entropy / 2
    redundancy = 1 - (entropy/math.log2(len(bigram_freq)))
    return entropy, redundancy, bigram_freq


def display_bigram_matrix(bigram_dict, output_file, save_as_excel=True):
    df = pd.DataFrame(list(bigram_dict.items()), columns=['bigram', 'frequency'])
    df[['letter1', 'letter2']] = df['bigram'].apply(lambda x: pd.Series(list(x)))
    matrix = df.pivot_table(index='letter1', columns='letter2', values='frequency', fill_value=0)
    if save_as_excel:
        matrix.to_excel(output_file)
    else:
        matrix.to_csv(output_file)



input_file = 'text.txt'
text = file_read(input_file)
text = filter_text(text)
filtered_text_spaces = filter_text(text)
filtered_text_no_spaces = remove_spaces(text)


print('Monograms analysys with spaces:')
monogram_entropy, monogram_redundancy = count_monograms(filtered_text_spaces)
print(f"Entropy for Monograms: {monogram_entropy}")
print(f"Redundancy for Monograms: {monogram_redundancy}\n")

print('Monograms analysys without spaces:')
monogram_entropy, monogram_redundancy = count_monograms(filtered_text_no_spaces)
print(f"Entropy for Monograms: {monogram_entropy}")
print(f"Redundancy for Monograms: {monogram_redundancy}\n")



print('bigrams analysys with spaces and overlaping:')
bigram_entropy, bigram_redundancy, bigram_frequencies = count_bigrams(filtered_text_spaces, include_overlaps=True,
                                                                      include_spaces=True)
print(f"Entropy for Bigrams: {bigram_entropy}")
print(f"Redundancy for Bigrams: {bigram_redundancy}\n")
output_file_with_spaces_and_overlap = "bigram_matrix_with_spaces_and_overlap.xlsx"
display_bigram_matrix(bigram_frequencies, output_file_with_spaces_and_overlap)


print('Bigrams analysys with no spaces and overlaping:')
bigram_entropy, bigram_redundancy, bigram_frequencies = count_bigrams(filtered_text_no_spaces, include_overlaps=True,
                                                                      include_spaces=False)
print(f"Entropy for Bigrams: {bigram_entropy}")
print(f"Redundancy for Bigrams: {bigram_redundancy}\n")
output_file_with_no_spaces_and_overlap = "bigram_matrix_with_no_spaces_and_overlap.xlsx"
display_bigram_matrix(bigram_frequencies, output_file_with_no_spaces_and_overlap)


print('Bigrams analysys with spaces and no overlaping:')
bigram_entropy, bigram_redundancy, bigram_frequencies = count_bigrams(filtered_text_spaces, include_overlaps=False,
                                                                      include_spaces=True)
print(f"Entropy for Bigrams: {bigram_entropy}")
print(f"Redundancy for Bigrams: {bigram_redundancy}\n")
output_file_with_spaces_and_no_overlap = "bigram_matrix_with_spaces_and_no_overlap.xlsx"
display_bigram_matrix(bigram_frequencies, output_file_with_spaces_and_no_overlap)


print('Bigrams analysys with no spaces and no overlaping:')
bigram_entropy, bigram_redundancy, bigram_frequencies = count_bigrams(filtered_text_no_spaces, include_overlaps=False,
                                                                      include_spaces=False)
print(f"Entropy for Bigrams: {bigram_entropy}")
print(f"Redundancy for Bigrams: {bigram_redundancy}\n")
output_file_with_no_spaces_and_no_overlap = "bigram_matrix_with_no_spaces_and_no_overlap.xlsx"
display_bigram_matrix(bigram_frequencies, output_file_with_no_spaces_and_no_overlap)

