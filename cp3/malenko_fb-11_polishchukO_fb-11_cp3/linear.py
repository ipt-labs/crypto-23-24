def euclid(a, b):
    if not a:
        return b, 0, 1

    gcd, u1, v1 = euclid(b % a, a)
    u = v1 - (b // a) * u1
    v = u1

    return gcd, u, v

def linear(a, b, n):
    a = a % n
    b = b % n

    d, u, v = euclid(a, n)
    if b % d != 0:
        return []

    x0 = (u * (b // d)) % n
    if x0 < 0:
        x0 += n

    return [(x0 + i * (n // d)) % n for i in range(d)]