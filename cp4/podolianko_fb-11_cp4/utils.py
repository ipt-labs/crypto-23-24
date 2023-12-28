import logging
import secrets
import random
from typing import Tuple


def miller_rabin_test(p: int, k: int = 10) -> bool:
    # 0
    # p - 1 = d * 2**s
    s = 0; d = p - 1
    while d & 1 == 0: s += 1; d = d >> 1
    assert 2 ** s * d == p - 1, "?!"

    counter = 0

    is_spp = False
    while counter < k:
        # 1
        x = random.randint(2, p - 1)
        if my_gcd(x, p) > 1:
            return False
        # 2 2.1
        c2_1 = hpow(x, d, p)
        if c2_1 == -1 % p or c2_1 == 1:
            is_spp = True
        else:
            # 2.2
            r = 1
            xr = hpow(x, d * 2, p)
            while True:
                if xr == -1 % p:
                    is_spp = True
                    break
                elif xr == 1:
                    is_spp = False
                    break
                else:
                    pass

                r += 1
                if r > s - 1:
                    break
                xr = hpow(xr, 2, p)
        # 2.3
        if not is_spp:
            return False
        else:
            counter += 1
        # 3 (loop)

    return is_spp


def is_prime(p: int) -> bool:
    for q in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107]:
        if p != q and p % q == 0:
            logging.info(f'N = {p:0X} not prime (division)')
            return False

    m = miller_rabin_test(p)
    if not m:
        logging.info(f'N = {p:0X} not prime (miller-rabin)')

    return m


def get_prime(bits: int) -> int:
    while True:
        p = secrets.randbits(bits)
        if is_prime(p): return p


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

    return gcd, u[-1], v[-1]


def my_gcd(a, b):
    """returns (positive) gcd of a, b"""
    return abs(extended_euclid(a, b)[0])


def mul_inverse(a, m) -> int | None:
    """returns multiplicative inverse of a modulo m, or None if it doesn't exist"""
    gcd, u, _ = extended_euclid(a, m)
    if abs(gcd) != 1:
        return None
    else:
        return u


def hpow(a: int, b: int, m: int | None = None):
    if m < 2:
        raise ValueError("modulo < 2")
    if a == 0:
        return 0
    if b == 0 or a == 1:
        return 1

    if b < 0:
        b = -b
        a = mul_inverse(a, m)
        if a is None:
            raise ValueError("base is not invertible for the given modulus")

    c = 1
    s = a
    if m is None:
        for i in range(0, b.bit_length()):
            if b & (1 << i) != 0:
                c *= s
            s *= s
    else:
        for i in range(0, b.bit_length()):
            if b & (1 << i) != 0:
                c *= s % m
            s *= s % m

    return c % m
