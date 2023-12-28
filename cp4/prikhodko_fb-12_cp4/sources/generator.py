import random
import sys
sys.setrecursionlimit(4096)

def gcd(a:int, b:int) -> int:
    if b == 0: 
        return a 
    else: 
        return gcd(b, a%b)

def egcd(a:int, b:int) -> tuple:
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def mod_pow(a:int,b:int,m:int) -> int:
    r = 1
    a = a % m 
    while b > 0:
        if (b & 1) == 1:
            r = (r * a) % m 
        b = b >> 1
        a = (a * a) % m 
    return r

def inverse(a:int,m:int) -> int:
    g,x,y = egcd(a,m)
    if g != 1:
        return -1
    return x % m

def mr_test(n:int,d:int) -> bool:
    x = random.randint(1, n)
    if gcd(n, x) != 1:
        return False 
    r = mod_pow(x, d, n)
    if r == 1 or r == n - 1:
        return True
    while d != n - 1:
        r = (r * r) % n 
        d *= 2
        if r == 1:
            return False 
        if r == n - 1:
            return True 
    return False

def is_prime(n:int, k:int = 5) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    
    d = n - 1
    c = 0
    while not d % 2:
        d //= 2
        c += 1
    for i in range(k):
        if not mr_test(n, d):
            return False 
    return True

def gen_prime(bits:int) -> int:
    tmp = random.randint(2**(bits-1),(2**bits)-1)
    if not tmp % 2:
        tmp += 1 
    while not is_prime(tmp):
        tmp += 2
    return tmp
    
def gen_rsa_primes(bits:int) -> tuple:
    qp = []
    for _ in range(2):
        qp += [gen_prime(bits)]
        # tmp = gen_prime(bits)
        # c = 2
        # while not is_prime(2*tmp + 1):
            # c += 1
            # tmp = tmp * c
        # qp += [2*tmp + 1]
    return tuple(qp)

