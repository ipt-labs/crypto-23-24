from typing import List, Dict, Tuple
import re
from consts import *


def normalize_string(string: str, alphabet: str, trans) -> str:
    lower_string = string.lower()
    translated_string = lower_string.translate(trans)
    rexp_valid_chars = f'[^{alphabet}]'
    normalized_string = re.sub(rexp_valid_chars, '', translated_string)

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


def to_indexes(text: str, alpha: str) -> List[int]:
    return [alpha.find(t) for t in text]


def from_indexes(i_list: List[int], alpha: str) -> str:
    return ''.join(alpha[i] for i in i_list)


def to_index(letter: str, alpha: str) -> List[int]:
    if len(letter) != 1:
        raise ValueError("Expected one letter")
    return alpha.find(letter)


def from_index(i: int, alpha: str) -> str:
    return alpha[i]


def letter_freq(text: str) -> List[Tuple[str, float]]:
    return [(letter, text.count(letter) / len(text)) for letter in set(text)]


def md_table_rows(rows) -> str:
    return '\n'.join(['|' + '|'.join(map(str, row)) + '|' for row in rows])


def md_table_columns(columns: Tuple[List, List], formats: List[str] | Tuple = '%s') -> str:
    columns = [[format(columns[i][row], formats[i]) for row in range(
        len(columns[i]))] for i in range(len(columns))]

    return '\n'.join(['|' + '|'.join(row) + '|' for row in zip(*columns)])


def extended_euclid(a: int, b: int) -> Tuple[int, int, int]:
    """returns gcd, u, v"""
    q = list()
    r = [a, b]

    while True:
        gcd = r[1]
        q.append(r[0] // r[1])
        r[0], r[1] = r[1], r[0] - q[-1] * r[1]
        if r[1] == 0:
            break

    u = list((1, 0))
    v = list((0, 1))

    for qi in q[:-1]:
        u.append(u[-2] - qi * u[-1])
        v.append(v[-2] - qi * v[-1])

    # sanity check
    # TODO REMOVE
    assert gcd == a * u[-1] + b * v[-1], "algo broken"

    return gcd, u[-1], v[-1]


def mul_inverse(a, m) -> int | None:
    """returns multiplicative inverse of a modulo m, or None if it doesn't exist"""
    gcd, u, _ = extended_euclid(a, m)
    if abs(gcd) != 1:
        return None
    else:
        return u


def gcd(a, b):
    """returns (positive) gcd of a, b"""
    return abs(extended_euclid(a, b)[0])


def solve_congruence(a: int, b: int, m: int) -> List[int]:
    """solves ax == b mod m and returns a list of solutions (if any)"""
    gcd_am, a_inv, _ = extended_euclid(a, m)
    if a_inv is None:
        return []

    if b % gcd_am != 0:
        return []

    s = []
    for r in range(1, gcd_am+1):
        s.append((b*a_inv % m)*r)

    return s


def import_freq_from(file: str) -> Dict[str, float]:
    import json
    with open(file, 'rt') as f:
        return json.load(f)


def sort_fqs(fmap: Dict[str, float]) -> List[str]:
    return list(
        map(lambda x: x[0],
            sorted(
                fmap.items(),
                key=lambda x:
                x[1],
                reverse=True
        )))


def sort_fqs_val(fmap: Dict[str, float]) -> List[Tuple[str, float]]:
    return sorted(
        fmap.items(),
        key=lambda x:
        x[1],
        reverse=True
    )


def bg_to_num(bg: str) -> int:
    return to_index(bg[0], ALPHABET) * len(ALPHABET) + to_index(bg[1], ALPHABET)


def num_to_bg(num: int) -> str:
    return from_index((num - (num % len(ALPHABET))) // len(ALPHABET), ALPHABET) + from_index(num % len(ALPHABET), ALPHABET)


def encrypt(msg: str, key: Tuple[int, int]):
    a, b = key
    m = len(ALPHABET)**2

    dec = list()
    for i in range(0, len(msg) // 2, 2):
        dec.append(
            num_to_bg(
                (bg_to_num(msg[i:i+2]) * a + b) % m
            )
        )


def decrypt(cypher: str, key: Tuple[int, int]) -> str:
    a, b = key
    m = len(ALPHABET)**2

    dec = list()
    for i in range(0, len(cypher) // 2, 2):
        dec.append(
            num_to_bg(
                ((bg_to_num(cypher[i:i+2]) - b) * mul_inverse(a, m)) % m
            )
        )

    return ''.join(dec)


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 3:
        with open(sys.argv[1], 'rt', encoding='utf-8') as file:
            text = file.read()
        print("Normalizing text...")
        try:
            with open(sys.argv[2], 'xt', encoding='utf-8') as file:
                file.write(normalize_string(text, ALPHABET, TRANSLATOR))
        except FileExistsError:
            print('Overwriting existing file')
            with open(sys.argv[2], 'wt', encoding='utf-8') as file:
                file.write(normalize_string(text, ALPHABET, TRANSLATOR))
    else:
        print('arguments: from to')
        exit(1)
