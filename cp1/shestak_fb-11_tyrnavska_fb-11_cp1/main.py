import frequency_lists_creator
import math


alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


# function for counting entropy and R
def entropy_r_counting(frequencies: dict, input_type: str, space=False) -> tuple:
    for_entropy_counting = []
    for i in frequencies.values():
        for_entropy_counting.append(-(float(i) * math.log2(float(i))))
    if input_type == 'l':
        if space:
            return sum(for_entropy_counting), 1 - (sum(for_entropy_counting) / math.log2(len(alphabet)+1))
        else:
            return sum(for_entropy_counting), 1 - (sum(for_entropy_counting) / math.log2(len(alphabet)))
    elif input_type == 'b':
        if space:
            return sum(for_entropy_counting) / 2, 1 - ((sum(for_entropy_counting) / 2) / math.log2(len(alphabet)+1))
        else:
            return sum(for_entropy_counting) / 2, 1 - ((sum(for_entropy_counting) / 2) / math.log2(len(alphabet)))


# creating variables to easier output handling
h1_r_with_spaces = entropy_r_counting(frequency_lists_creator.get_frequency('output/letters_frequency_with_spaces.csv'), 'l', space=True)
h1_r_without_spaces = entropy_r_counting(frequency_lists_creator.get_frequency('output/letters_frequency_without_spaces.csv'), 'l')
h2_r_with_spaces_overlapping = entropy_r_counting(frequency_lists_creator.get_frequency('output/overlapping_bigrams_frequency_with_spaces.csv'), 'b', space=True)
h2_r_without_spaces_overlapping = entropy_r_counting(frequency_lists_creator.get_frequency('output/overlapping_bigrams_frequency_without_spaces.csv'), 'b')
h2_r_with_spaces_non_overlapping = entropy_r_counting(frequency_lists_creator.get_frequency('output/non_overlapping_bigrams_frequency_with_spaces.csv'), 'b', space=True)
h2_r_without_spaces_non_overlapping = entropy_r_counting(frequency_lists_creator.get_frequency('output/non_overlapping_bigrams_frequency_without_spaces.csv'), 'b')

# output of all code
print(f"Letters entropy with spaces (H1): {h1_r_with_spaces[0]}, R: {h1_r_with_spaces[1]}")
print(f"Letters entropy without spaces (H1): {h1_r_without_spaces[0]}, R: {h1_r_without_spaces[1]}")
print(f"Overlapping bigrams entropy with spaces (H2): {h2_r_with_spaces_overlapping[0]}, R: {h2_r_with_spaces_overlapping[1]}")
print(f"Overlapping bigrams entropy without spaces (H2): {h2_r_without_spaces_overlapping[0]}, R: {h2_r_without_spaces_overlapping[1]}")
print(f"Non-overlapping bigrams entropy with spaces (H2): {h2_r_with_spaces_non_overlapping[0]}, R: {h2_r_with_spaces_non_overlapping[1]}")
print(f"Non-overlapping bigrams entropy without spaces (H2): {h2_r_without_spaces_non_overlapping[0]}, R: {h2_r_without_spaces_non_overlapping[1]}")
