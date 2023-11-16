from typing import Union, Optional
from math import log2


def compute_entropy(n: int, freq_dict: dict[str: float]) -> float:
    entropy = 0
    for freq in freq_dict.values():
        entropy -= freq * log2(freq)

    return entropy / n


def ext_euclid(a: int, b: int) -> tuple[int, int, int]:
    prev_r, r = a, b
    prev_u, u = 1, 0
    prev_v, v = 0, 1

    while r:
        q = prev_r // r
        prev_r, r = r, prev_r - q * r
        prev_u, u = u, prev_u - q * u
        prev_v, v = v, prev_v - q * v

    return prev_r, prev_u, prev_v


def get_modulo_inverse(a: int, mod: int) -> tuple[Optional[int], int]:
    gcd, inverse, _ = ext_euclid(a, mod)

    if gcd == 1:
        return inverse % mod, gcd
    
    return None, gcd


def linear_comparsion(a: int, b: int, mod: int) -> Union[int, list[int], None]:
    inverse, gcd = get_modulo_inverse(a, mod)

    if inverse:
        return inverse * b % mod
    
    if b % gcd == 0:
        old_gcd = gcd
        a, b, mod = a // gcd, b // gcd, mod // gcd
        inverse, gcd = get_modulo_inverse(a, mod)
        return [i for i in range(inverse * b % mod, inverse * b % mod + old_gcd * mod, mod)]
    
    return None
