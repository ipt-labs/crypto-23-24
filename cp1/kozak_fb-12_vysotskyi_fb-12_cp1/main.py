from math import log2
from re import sub

path = "clean_text.txt"

def clean_text(filepath):
    text = read_text(filepath)
    text = text.lower()
    text = sub("[^а-яё ]", " ", text)
    text = sub("\s+", " ", text)
    return text

def text_without_spaces(filepath):
    text = read_text(filepath)
    text = sub("\s", "", text)
    return text


def save_text(filepath, text):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

def read_text(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        file_content = f.read()
    return file_content

def count_letters(filepath):    # Підрахунок символів у тексті
    letter_dict = {}
    text = read_text(filepath)
    for letter in text:
        if letter in letter_dict:
            letter_dict[letter] += 1
        else:
            letter_dict[letter] = 1
    letter_dict = dict(sorted(letter_dict.items(), key=lambda x: x[1], reverse=True))
    return letter_dict

def count_letter_frequency(filepath):    # Підрахунок частоти символів
    letter_dict = count_letters(filepath)
    total_count = sum(letter_dict.values())   # Повна кількість символів
    letter_frequency = {letter: count / total_count for letter, count in letter_dict.items()}
    letter_frequency = dict(sorted(letter_frequency.items(), key=lambda x: x[1], reverse=True))
    return letter_frequency

def count_letter_frequency_without_spaces(filepath):  # Підрахунок частоти символів без пробілів
    letter_dict = count_letters(filepath)
    spaces_count = letter_dict.get(' ')
    total_count_no_spaces = sum(letter_dict.values()) - spaces_count
    del letter_dict[' ']
    letters_frequency_without_spaces = {letter: count / total_count_no_spaces for letter, count in letter_dict.items()}
    letters_frequency_without_spaces = dict(sorted(letters_frequency_without_spaces.items(), key=lambda x: x[1], reverse=True))
    return letters_frequency_without_spaces

def count_bigrams(filepath, step=1):    # Підрахунок біграм з різним кроком
    text = read_text(filepath)
    bigram_dict = {}
    for i in range(0, len(text) - 1, step):
        bigram = text[i:i+2].replace(" ", "_")
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    bigram_dict = dict(sorted(bigram_dict.items(), key=lambda x: x[1], reverse=True))  # Сортування за значеннями ключів
    return bigram_dict

def count_bigram_frequency(filepath, step=1):    # Частота біграм з пробілами з різним кроком
    bigram_dict = count_bigrams(filepath, step)
    total_count = sum(bigram_dict.values())
    bigram_frequency = {bigram: count / total_count for bigram, count in bigram_dict.items()}
    return bigram_frequency

def count_bigram_frequency_without_spaces(filepath, step=1):   # Частота біграм без пробілів з різним кроком
    text = text_without_spaces(filepath)
    bigram_dict = {}
    for i in range(0, len(text) - 1, step):
        bigram = text[i:i + 2]
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    bigram_dict = dict(sorted(bigram_dict.items(), key=lambda x: x[1], reverse=True))
    total_count = sum(bigram_dict.values())
    bigram_frequency = {bigram: count / total_count for bigram, count in bigram_dict.items()}
    return bigram_frequency

def output_list(frequency: dict):
    text = ""
    for element in frequency:
        print(element, round(frequency[element], 4))
        text += f"{element},{round(frequency[element], 4)}\n"
    return text


def output_table(frequency: dict) -> str:
    rows = []
    first_letters_dublicated = [x[0] for x in frequency.keys()]
    first_letters = []
    [first_letters.append(x) for x in first_letters_dublicated if x not in first_letters]
    second_letters_dublicated = [x[1] for x in frequency.keys()]
    second_letters = []
    [second_letters.append(x) for x in second_letters_dublicated if x not in second_letters]
    text = "\\  " + "-     ".join(first_letters) + "-     \n"
    for second_letter in second_letters:
        text += "'-" + second_letter + " "
        for first_letter in first_letters:
            bigram = first_letter+second_letter
            text += f"{round(frequency[bigram], 4) if bigram in frequency else 0:0<6} "
        text += "\n"

    print(text)
    return text


def calculate_entropy(frequencies: dict, length: int) -> float:
    entropy = 0.0
    for frequency in frequencies.values():
        entropy -= frequency*log2(frequency)
    return entropy/length


def calculate_redundancy(entropy: float, alphabet_power: int, length: int) -> float:
    h0 = log2(alphabet_power)/length
    return 1-entropy/h0


if __name__ == "__main__":
    text = ""
    letters = count_letter_frequency(path)
    letters_no_spaces = count_letter_frequency_without_spaces(path)
    bigrams_step_1 = count_bigram_frequency(path)
    bigrams_step_2 = count_bigram_frequency(path, 2)
    bigrams_step_1_no_spaces = count_bigram_frequency_without_spaces(path)
    bigrams_step_2_no_spaces = count_bigram_frequency_without_spaces(path, 2)

    text += output_list(letters)
    text += output_list(letters_no_spaces)
    bigram_frequencies = [bigrams_step_1, bigrams_step_2, bigrams_step_1_no_spaces, bigrams_step_2_no_spaces]
    all_frequencies = [letters, letters_no_spaces] + bigram_frequencies
    for frequencies in bigram_frequencies:
        text += output_table(frequencies)

    for frequencies in all_frequencies:
        length = 1 if frequencies in [letters, letters_no_spaces] else 2
        entropy = round(calculate_entropy(frequencies, length), 5)
        redundancy = round(calculate_redundancy(entropy, len(frequencies), length), 5)
        text += f"{entropy} {redundancy}\n"
        print(entropy, redundancy)
    save_text("data.csv", text)

    print("Redundancies from CoolPinkProgram")
    print(round(calculate_redundancy(2.44563, 32, 1), 5))
    print(round(calculate_redundancy(3.17705, 32, 1), 5))
    print(round(calculate_redundancy(1.38487, 32, 1), 5))
    print(round(calculate_redundancy(2.05225, 32, 1), 5))
    print(round(calculate_redundancy(1.29114, 32, 1), 5))
    print(round(calculate_redundancy(2.04913, 32, 1), 5))
