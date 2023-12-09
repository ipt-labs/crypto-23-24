import random
from random import randrange

## ex 1

def GCD(a,b):
    if b == 0:
        return a, 1, 0
    d, x, y = GCD(b, a % b)
    return d, y, x - (a // b) * y

def reverse(num, mod):
    gcd, x, y = GCD(num, mod)
    if gcd == 1:
        return (x % mod + mod) % mod
    else:
        return -1

def horner(num, pow, mod):
    result = 1

    while pow > 0:
        if pow & 1:
            result = (result * num) % mod
        num = (num * num) % mod
        pow >>= 1

    return result

def rand_prime(N = 256):
    iter = 0
    while (True):
        iter = iter + 1
        bin_str = "1"
        for i in range(N - 1):
            bit = random.randint(0, 1)
            bin_str = bin_str + str(bit)
        num = int(bin_str, 2)
        if Miller_Rabin(num) == True:
            return num

def Miller_Rabin(number):
    if number % 2 == 0 or number % 3 == 0 or number % 5 == 0 or number % 7 == 0:
        return False
    s, d = 0, number - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    for k in range(50):
        x = randrange(2, number - 1)
        gcd = GCD(x, number)[0]
        if gcd > 1:
            return False
        y = horner(x, d, number)
        if y == 1 or y == number - 1:
            return True
        while s > 1:
            y = horner(y, y, number)
            if y == 1:
                return False
            if y == -1:
                return True
            s -= 1
        return False

def rand_primes(N=256):
    p = rand_prime()
    q = rand_prime()

    p1 = rand_prime()
    q1 = rand_prime()

    while p * q <= p1 * q1:
        # Якщо pq <= p1q1, генеруємо нові пари чисел
        p = rand_prime()
        q = rand_prime()
        p1 = rand_prime()
        q1 = rand_prime()

    return p, q, p1, q1

def key_pair(p, q):
    n = p * q
    f = (p - 1) * (q - 1)

    while True:
        e = randrange(2, f)
        if GCD(e, f)[0] == 1:
            break

    d = reverse(e, f)

    public_key = [e, n]
    private_key = [d, p, q]

    return public_key, private_key



