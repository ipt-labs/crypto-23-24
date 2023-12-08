from typing import List, Dict, Tuple, Iterable
from numbers import Number
import re

import matplotlib.pyplot

from consts import *

# TODO move this somewhere
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout, format=f'%(levelname)s: %(message)s')


def index_of_coincidence(text: str) -> float:
    actually_present_letters = set(text)

    return sum([text.count(t) * (text.count(t) - 1) for t in actually_present_letters]) / (len(text) * (len(text) - 1))


def normalize_string(string: str, alphabet: str, trans) -> str:
    lower_string = string.lower()
    translated_string = lower_string.translate(trans)
    rexp_valid_chars = f'[^{alphabet}]'
    normalized_string = re.sub(rexp_valid_chars, '', translated_string)

    return normalized_string


def to_indexes(text: str, alpha: str) -> List[int]:
    return [alpha.find(t) for t in text]


def from_indexes(i_list: List[int], alpha: str) -> str:
    return ''.join(alpha[i] for i in i_list)


def split_as_caesar_blocks(text: str, key_len: int) -> List[List[str]]:
    if len(text) % key_len == 0:
        logging.log(logging.DEBUG, "Couldn't split text into whole blocks")

    return [[text[ri + bi * key_len] for bi in range(0, len(text) // key_len)] for ri in range(key_len)]


def coincidence_count(blocks: List[List[str]]) -> int:
    """Expects blocks from *split_as_caesar_blocks*"""
    return sum([sum([1 if block[i] == block[i + 1] else 0 for i in range(len(block) - 1)]) for block in blocks])


def coincidence_count2(text: str, key_len) -> int:
    s = 0
    for i in range(len(text) - key_len):
        s += 1 if text[i] == text[i + key_len] else 0

    return s


def naive_first_peak(data: Dict[Number, Number]) -> Tuple[Number, Number]:
    AVG = sum(data.values()) / len(data.values())

    keys = sorted(data.keys())
    prem = (0, 0)
    m = (0, 0)
    for key in keys:
        if data[key] > m[1]:
            prem = m
            m = (key, data[key])
        else:
            if (prem[1] > data[key]) and abs(m[1] - data[key]) > THRESHOLD:
                break
    return m


def guess_key_len_1(text: str, ioc_random: float, ioc_theoretical: float, max_considered_len=30, diagram=False) -> int:
    block_iocs_avg: Dict[int, float] = dict()
    for r in range(2, max_considered_len):
        blocks = split_as_caesar_blocks(text, r)
        block_iocs = [index_of_coincidence(''.join(block)) for block in blocks]
        block_iocs_avg.update({r: sum(block_iocs) / len(block_iocs)})

    text_ioc = index_of_coincidence(text)

    logging.log(logging.INFO, f'Text ioc: {text_ioc}')
    logging.log(logging.INFO, f'Average block iocs for different r\'s: %s', block_iocs_avg)
    logging.log(logging.INFO, f'Max ioc: {max(block_iocs_avg.items(), key=lambda x: x[1])}')

    # plotting
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.set_title('Усереднені і.в. блоків для різних r')
    ax.scatter(block_iocs_avg.keys(), block_iocs_avg.values())
    ax.set(ylim=(IOC_RANDOM, 0.06))
    ax.set_xlabel('r')
    ax.set_ylabel('і.в.')
    ax.minorticks_on()
    plt.savefig('./data/avg_iocs.png')

    return naive_first_peak(data=block_iocs_avg)[0]


def letter_freq(text: str) -> List[Tuple[str, float]]:
    return [(letter, text.count(letter) / len(text)) for letter in set(text)]

def md_table_rows(rows) -> str:
    return '\n'.join(['|' + '|'.join(map(str, row)) + '|' for row in rows])

def md_table_columns(columns: Tuple[List, List], formats: List[str] | Tuple = '%s') -> str:
    columns = [[format(columns[i][row], formats[i]) for row in range(len(columns[i]))] for i in range(len(columns))]

    return '\n'.join(['|' + '|'.join(row) + '|' for row in zip(*columns)])


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 3:
        with open(sys.argv[1], 'rt', encoding='utf-8') as file:
            text = file.read()
        try:
            with open(sys.argv[2], 'xt', encoding='utf-8') as file:
                file.write(normalize_string(text, ALPHABET, TRANSLATOR))
        except FileExistsError:
            print('Overwriting existing file')
            with open(sys.argv[2], 'wt', encoding='utf-8') as file:
                file.write(normalize_string(text, ALPHABET, TRANSLATOR))
    else:
        print('arguments from to')
        exit(1)
