import math

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def text_format_spaceless(text: str):  # I expect lowercase
    return "".join([i for i in text if i in alphabet])


def text_format(text: str):
    return "".join([i for i in text if i in alphabet or i == " "])


def char_freq(text: str):
    char_dict = {}
    for char in text:
        keys = char_dict.keys()
        if char in keys:
            char_dict[char] += 1
        else:
            char_dict[char] = 1
    return char_dict


def bigram_freq(text: str, mode: int):
    bigram_dict = {}
    if mode == 1:
        bigram_range = range(len(text) - 1)
    elif mode == 2:
        bigram_range = range(0, len(text) - 1, 2)
    for i in bigram_range:
        bigram = text[i:i + 2]
        if bigram in bigram_dict:
            bigram_dict[bigram] += 1
        else:
            bigram_dict[bigram] = 1
    return bigram_dict


def get_entropy_r(freq_dict, text_length, alphabet_len, bigram: bool):
    entropy = 0.0
    for count in freq_dict.values():
        probability = count / text_length
        entropy -= probability * math.log2(probability)

    if bigram:
        entropy = entropy / 2

    r = 1 - entropy / math.log2(alphabet_len)
    return entropy, r


def print_freqs(freq_dict, text_length):
    print("\nЧастота літер/біграм в тексті:")
    for char in freq_dict.keys():
        frequency = (freq_dict[char] / text_length) * 100
        print(f"{char}: {frequency:.4f}%")


if __name__ == "__main__":
    with open("text", 'r') as file:
        text = file.read().lower()

    text_spaceless = text_format_spaceless(text)
    text_full = text_format(text)

    letter_frequency_without_spaces = char_freq(text_spaceless)
    letter_frequency = char_freq(text_full)

    bigram_frequency_without_spaces_1 = bigram_freq(text_spaceless, 1)
    bigram_frequency_1 = bigram_freq(text_full, 1)

    bigram_frequency_without_spaces_2 = bigram_freq(text_spaceless, 2)
    bigram_frequency_2 = bigram_freq(text_full, 2)

    print_freqs(letter_frequency, len(text_full))
    print_freqs(bigram_frequency_1, len(text_full))

    es, rs = get_entropy_r(letter_frequency, len(text_full), 34, False)
    e, r = get_entropy_r(letter_frequency_without_spaces, len(text_spaceless), 33, False)
    ebs, rbs = get_entropy_r(bigram_frequency_1, len(text_full), 34, True)
    eb, rb = get_entropy_r(bigram_frequency_without_spaces_1, len(text_spaceless), 33, True)
    eb2s, rb2s = get_entropy_r(bigram_frequency_2, (len(text_full)) // 2, 34, True)
    eb2, rb2 = get_entropy_r(bigram_frequency_without_spaces_2, (len(text_spaceless)) // 2, 33, True)

    print("Ентропія і надлишковість H1:", e, r)
    print("Ентропія і надлишковість H1 з пробілами:", es, rs)
    print("Ентропія і надлишковість H2:", eb, rb)
    print("Ентропія і надлишковість H2 з пробілами: ", ebs, rbs)
    print("Ентропія і надлишковість H2 без перетинів:", eb2, rb2)
    print("Ентропія і надлишковість H2 з пробілами без перетинів і :", eb2s, rb2s)

