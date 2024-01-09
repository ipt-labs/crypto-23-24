import random as rd

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def milrab(p):
    primes = [2, 3, 5, 7]
    for prime in primes:
        if p % prime == 0:
            return False
    
    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    
    chosen = []
    x = rd.randint(2, p - 1)

    k = 10
    for _ in range(k):
        while x in chosen:
            x = rd.randint(2, p - 1)
        chosen.append(x)
        if egcd(x, p)[0] > 1:
            return False
        
        xr = pow(x, d, p)
        if xr == 1 or xr == p - 1:
            continue
        
        ispsp = False
        for _ in range(1, s):
            xr = pow(xr, 2, p)
            if xr == p - 1:
                ispsp = True
                break
            if xr == 1:
                return False
        
        if not ispsp:
            return False
    
    return True

def genrand(lower_bound, upper_bound, _depth = 0):
    if _depth > 5:
        return genrand(lower_bound, upper_bound * 2)
    x = rd.randint(lower_bound, upper_bound)
    m = x
    if x % 2 == 0:
        m += 1
    
    i = 0
    while m + 2 * i < (upper_bound - m) // 2:
        p = m + 2 * i
        if milrab(p):
            return p
        i += 1
    
    return genrand(lower_bound, upper_bound, _depth + 1)