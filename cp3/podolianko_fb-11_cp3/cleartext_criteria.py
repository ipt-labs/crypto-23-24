from typing import *
from utils import *
from math import log2

BANNED = ["ъъ", "ыы", "эы"]

def entropy_from_probabilities(probabilities: Iterable) -> float:
    """Calculate entropy on `probabilities` (log2)"""
    return -sum(map(lambda p: p * log2(p), probabilities))


def check_entropy(text: str, letter_freq: Dict[str, float], e_threshold = 4.9) -> bool:
    return entropy_from_probabilities(letter_freq.values()) < e_threshold


def check_letter_min_freq(text: str, letter_freq: Dict[str, float], sample_freqs: Dict[str, float], n=5, q=0.70) -> bool:
    sorted_freq = sort_fqs_val(sample_freqs)
    return all((letter_freq[s[0]] >= s[1] * q for s in sorted_freq[:n]))
