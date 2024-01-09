from random import randrange
from typing import Optional
from math import log


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def trialDiv(p: int) -> bool:
    for d in [2, 5, 7, 11, 13]:
        if p % d == 0:
            return False
        
    return True


def HornerPow(base: int, power: int, modulo: int) -> int:
    bin_rep = str(bin(power))[2:]
    res = 1
    for i in range(len(bin_rep)):
        res = (res ** 2) % modulo
        if bin_rep[i] == "1":
            res = (res * base) % modulo

    return res


def MillerRabin(p: int, k: int) -> bool:
    s, d = 0, p - 1
    while d % 2 == 0:
        d //= 2; s += 1

    for _ in range(k):
        isStrongPseudoprime = False
        x = randrange(2, p, 1)

        if gcd(x, p) > 1:
            return False
        
        if (xd := HornerPow(x, d, p)) == 1 or xd == p - 1:
            continue
        else:
            for _ in range(1, s):
                if (xd := HornerPow(xd, 2, p)) == p - 1:
                    isStrongPseudoprime = True
                    break
                elif xd == 1:
                    return False
            
            if isStrongPseudoprime == False:
                return False
            
    return True


def generatePrime(length: int):
    while True:
        n = 2 ** length

        if n > 396738:
            x = randrange(n, int(n + n/(25 * ((log(n)) ** 2))) + 1)
        else:
            x = randrange(n, 2*n - 2)
        m0 = x if x % 2 != 0 else x + 1

        for i in range(0, int((2*n - 2 - m0)/2)):
            if not trialDiv(m0 + 2*i):
                continue

            if MillerRabin(m0 + 2*i, 20):
                return m0 + 2*i
            

def extEuclid(a: int, b: int) -> tuple[int, int, int]:
    prev_r, r = a, b
    prev_u, u = 1, 0
    prev_v, v = 0, 1

    while r:
        q = prev_r // r
        prev_r, r = r, prev_r - q * r
        prev_u, u = u, prev_u - q * u
        prev_v, v = v, prev_v - q * v

    return prev_r, prev_u, prev_v


def getModuloInverse(a: int, mod: int) -> Optional[int]:
    gcd, inverse, _ = extEuclid(a, mod)

    if gcd == 1:
        return inverse % mod

    return None


def os2ip(msg: str, encoding='utf-8') -> int:
    return int.from_bytes(msg.encode(encoding), byteorder='big')


def i2byte(msg: int) -> bytes:
    return msg.to_bytes((msg.bit_length() + 7) // 8, byteorder='big')


def i2osp(msg: int, encoding='utf-8') -> str:
    return i2byte(msg).decode(encoding)
