def ExtendedEuclidAlgorithm(a, b):
    if a == 0:
        return b, 0, 1
    gcd, u, v = ExtendedEuclidAlgorithm(b % a, a)
    return gcd, v - (b // a) * u, u

def SolveLinearComparison(a, b, n = 33):
    roots = []
    gcd, u, v = ExtendedEuclidAlgorithm(a, n)
    if gcd == 1:
        roots.append((u * b) % n)
        return roots
    if b % gcd != 0:
        return roots
    x0 = ((b // gcd) * ExtendedEuclidAlgorithm(a // gcd, n // gcd)[1]) % (n // gcd)
    for i in range(gcd):
        roots.append(x0 + i * n // gcd)
    return roots

def main():
    a = SolveLinearComparison(15, 18)
    print(a)

if __name__ == "__main__":
    main()