def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x


def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    return x % m if g == 1 else None


def solve_linear_congruence(a, b, m):
    roots = []
    a, b = a % m, b % m
    g = gcd(a, m)
    if g == 1:
        a_inv = mod_inverse(a, m)
        roots.append((a_inv * b) % m)
        print(roots)
        return roots
    elif g > 1 and b % g == 0:
        a1 = a // g
        b1 = b // g
        m1 = m // g
        roots = solve_linear_congruence(a1, b1, m1)
        roots.extend((roots[0] + m1 * i) % m for i in range(g))
        print(roots)
        return roots
    else:
        return None


print(gcd(17,18))
print(mod_inverse(56, 221))
solve_linear_congruence(5, 16, 22)