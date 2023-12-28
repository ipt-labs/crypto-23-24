import sys
from lib import *


def main(file: str):
    with open(file, 'rt', encoding='utf-8') as textfile:
        sample_text_string = textfile.read()

    configs = [
        # W/wo whitespace , w/wo overlapping
        (True, True),
        (False, True),
        (True, False),
        (False, False)
    ]

    for whitespace_inclusion in (True, False):
        letter_executor(whitespace_inclusion, sample_text_string)

    for config in configs:
        bigram_executor(*config, sample_text_string)


def letter_executor(whitespaces: bool, text: str):
    text = normalize_string(text, VALID_LETTERS, whitespaces)
    pmap = ngram_frequencies(text, 1, False)
    entropy = entropy_from_probabilities(pmap.values())

    print(f"{'Letter frequencies with whitespaces:' if whitespaces else 'Letter frequencies without whitespaces'}")
    print()
    print_freq_plain(pmap, 5, 4)
    print(f"Entropy: {entropy}")
    print(f"Redundancy: {redundancy(entropy, log2(len(VALID_LETTERS) + (1 if whitespaces else 0)))}")
    print()


def bigram_executor(whitespaces: bool, overlapping: bool, text: str):
    text = normalize_string(text, VALID_LETTERS, whitespaces)
    pmap = ngram_frequencies(text, 2, overlapping)

    print(
        f"Bigram frequencies, {'overlapping' if overlapping else 'non-overlapping'}, {'with' if whitespaces else 'without'} whitespaces:")
    print()
    print_bigram_freq_table(pmap)
    entropy_per_char = entropy_from_probabilities(pmap.values()) / 2
    print(f"Entropy per character: {entropy_per_char}")
    print(f"Redundancy: {redundancy(entropy_per_char, log2(len(VALID_LETTERS) + (1 if whitespaces else 0)))}")
    print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: pass text file location as the only argument")
        exit(1)

    main(sys.argv[1])
