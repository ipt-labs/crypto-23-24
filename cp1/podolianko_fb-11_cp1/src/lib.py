from typing import Iterable, Dict
from math import log2
import re
import functools

VALID_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя";


def entropy_from_probabilities(probabilities: Iterable) -> float:
    """Calculate entropy on `probabilities` (log2)"""
    return -sum(map(lambda p: p * log2(p), probabilities))

@functools.cache
def normalize_string(string: str, alphabet: str, preserve_whitespace: bool) -> str:
    """returns lowercase string consisting only of `alphabet` characters, or also single whitespaces between words, if `preserve_whitespace` is true."""
    lower_string = string.lower()

    rexp_valid_chars = f'[^{VALID_LETTERS}]'
    rexp_single_whitespace = '\s+'

    valid_chars_only = re.sub(rexp_valid_chars, ' ', lower_string)
    space_replace = ''
    if preserve_whitespace:
        space_replace = ' '

    normalized_string = re.sub(rexp_single_whitespace, space_replace, valid_chars_only)

    return normalized_string


def ngram_frequencies(text: str, n: int, overlap: bool) -> Dict[str, float]:
    """
    Calculates frequencies for ngrams in the supplied `text`
     * `text` - a String of text
     * `n` - ngram length in characters
     * `overlap` - will calculate frequencies of overlapping ngrams if true, e.g. 'abcd' wil result in ab=1/3, bc=1/3, cd=1/3; otherwise will count only non-overlapping ngrams, e.g. 'abcd' will result in ab=1/2, cd=1/2
    """
    step = n
    if overlap:
        step = 1

    freq_map = dict()
    for i in range(0, len(text) + 1 - n, step):
        ngram = text[i:i + n]
        if ngram in freq_map:
            freq_map[ngram] += 1
        else:
            freq_map[ngram] = 1

    total = sum(freq_map.values())
    for freq in freq_map.keys():
        freq_map[freq] = freq_map[freq] / total

    return freq_map


def print_freq_plain(freq_map: Dict[str, float], max_columns: int, float_precision: int):
    """
    Print a sorted table of ngrams and corresponding frequencies.
     * `max_columns` - specifies maximum number of columns, the table may actually consist of less columns than specified by this argument.
     * `float_precision` - specifies floating-point precision of frequencies
    """
    columns = max_columns

    ngrams = sorted(freq_map.keys())

    extra_column = 0
    if len(ngrams) // columns != 0:
        extra_column = 1

    rows = (len(ngrams) // columns) + extra_column

    for row in range(0, rows):
        for col in range(0, columns):
            index = col * rows + row

            if index >= len(ngrams):
                break

            ngram = ngrams[index]
            print(f"| {ngram}:{freq_map.get(ngram):^.{float_precision}f} ", end='')
        print("|")


def print_bigram_freq_table(freq_map: Dict[str, float]):
    first_char_set = sorted(set(map(lambda k: k[0], freq_map.keys())))
    second_char_set = sorted(set(map(lambda k: k[1], freq_map.keys())))

    table_x, table_y = len(second_char_set), len(first_char_set)

    cell_width = 7
    float_precision = cell_width - 2

    # print header
    print(f"|{' ':{cell_width}}", end='')
    for x in range(0, table_x):
        print(f"|{second_char_set[x]:^{cell_width}}", end='')

    print("|")

    # print separator
    print(f"|{'-':-<{cell_width}}", end='')
    for _x in range(0, table_x):
        print(f"+{'':-<{cell_width}}", end='')
    print("|")

    # print rows
    for y in range(0, table_y):
        print(f"|{first_char_set[y]:^{cell_width}}", end='')
        for x in range(0, table_x):
            key = first_char_set[y] + second_char_set[x]
            freq = freq_map.get(key)
            if freq is None:
                print(f"|{'-':^{cell_width}}", end='')
            else:
                print(f"|{freq:^{cell_width}.{float_precision}f}", end='')
        print("|")


def redundancy(h_inf: float, h_0: float) -> float:
    return 1 - (h_inf / h_0)
