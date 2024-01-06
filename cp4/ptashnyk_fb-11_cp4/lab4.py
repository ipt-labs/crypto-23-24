from random import randint, getrandbits

def GornerScheme(x, a, m):
    binary = str(bin(a))[2:]
    y = 1
    for i in binary:
        y = (y * y) % m
        y = (y * x ** int(i)) % m
    return y

def ExtendedEuclidAlgorithm(a, b):
    if a == 0:
        return b, 0, 1
    gcd, u, v = ExtendedEuclidAlgorithm(b % a, a)
    return gcd, v - (b // a) * u, u

def PrimeFactorization(n):
    s = 0
    d = n
    while d % 2 == 0:
        s += 1
        d //= 2
    return d, s

def MillerRabinTest(p, k):
    d, s = PrimeFactorization(p - 1)
    counter = 0
    while counter < k:
        counter += 1
        x = randint(2, p - 1)
        gcd = ExtendedEuclidAlgorithm(x, p)[0]
        if gcd > 1:
            return False
        gornerResult = GornerScheme(x, d, p)
        if gornerResult == 1 or gornerResult == p - 1:
            continue
        for r in range(1, s - 1):
            xR = GornerScheme(x, d * 2 ** r, p)
            if xR == p - 1:
                break
            if xR == 1:
                return False
        else:
            return False
    return True

def TestDivision(n):
    divisionArray = [2, 3, 5, 7, 11]
    for i in divisionArray:
        if n % i == 0:
            return False
    return True

def GenerateRandomPrime(start = None, end = None, length = None):
    print("Random prime number generation...")
    if start is not None and end is not None:
        while(True):
            n = randint(start, end)
            if TestDivision(n):
                if MillerRabinTest(n, 15):
                    print("Candidate:", n, " passed the test")
                    return n
                else:
                    print("Candidate:", n, " failed the test")
            else:
                print("Candidate:", n, " failed the test")
    if length is not None:
        while(True):
            n = getrandbits(length)
            if TestDivision(n):
                if MillerRabinTest(n, 15):
                    print("Candidate:", n, " passed the test")
                    return n
                else:
                    print("Candidate:", n, " failed the test")
            else:
                print("Candidate:", n, " failed the test")

def GeneratePrimePairs():
    while(True):
        p = GenerateRandomPrime(length = 256)
        q = GenerateRandomPrime(length = 256)
        p1 = GenerateRandomPrime(length = 256)
        q1 = GenerateRandomPrime(length = 256)
        if p * q <= p1 * q1:
            return p, q, p1, q1

def GenerateKeyPair(p, q):
    n = p * q
    oiler = (p - 1) * (q - 1)
    e = 2 ** 16 + 1
    d = ExtendedEuclidAlgorithm(e, oiler)[1] % oiler
    publicKey = (n, e)
    privateKey = (d, p, q)
    return publicKey, privateKey

def Encrypt(M, publicKey):
    return GornerScheme(M, publicKey[1], publicKey[0])

def Decrypt(C, privateKey):
    n = privateKey[1] * privateKey[2]
    return GornerScheme(C, privateKey[0], n)

def Sign(M, privateKey):
    n = privateKey[1] * privateKey[2]
    return (M, GornerScheme(M, privateKey[0], n))

def Verify(S, publicKey):
    return S[0] == GornerScheme(S[1], publicKey[1], publicKey[0])

def SendKey(publicKeyA, publicKeyB, privateKeyA, k):
    if publicKeyB[0] >= publicKeyA[0]:
        k1 = Encrypt(k, publicKeyB)
        S = Sign(k, privateKeyA)[1]
        S1 = Encrypt(S, publicKeyB)
        return (k1, S1)

def ReceiveKey(privateKeyB, k1, S1, publicKeyA):
    k = Decrypt(k1, privateKeyB)
    S = Decrypt(S1, privateKeyB)
    return Verify((k, S), publicKeyA)

def main():
    p, q, p1, q1 = GeneratePrimePairs()
    publicKeyA, privateKeyA = GenerateKeyPair(p, q)
    print("Public key for user A: ( n -", publicKeyA[0], ", e -", publicKeyA[1], ")")
    print("Private key for user A: ( d -", privateKeyA[0], ", p -", privateKeyA[1], ", q -", privateKeyA[2], ")")
    publicKeyB, privateKeyB = GenerateKeyPair(p1, q1)
    print("Public key for user B: ( n1 -", publicKeyB[0], ", e1 -", publicKeyB[1], ")")
    print("Private key for user B: ( d1 -", privateKeyB[0], ", p1 -", privateKeyB[1], ", q1 -", privateKeyB[2], ")")

    M = 10
    print("message M:", M)
    encryptedA = Encrypt(M, publicKeyA)
    decryptedA = Decrypt(encryptedA, privateKeyA)
    print("encrypted message C by A:", encryptedA, "\ndecrypted message M by A:", decryptedA)
    encryptedB = Encrypt(M, publicKeyB)
    decryptedB = Decrypt(encryptedB, privateKeyB)
    print("encrypted message C by B:", encryptedB, "\ndecrypted message M by B:", decryptedB)
    signA = Sign(M, privateKeyA)
    print("Signature for user A:", signA)
    VerifyA = Verify(signA, publicKeyA)
    print("result of verifying signature A:", VerifyA)
    signB = Sign(M, privateKeyB)
    print("Signature for user B:", signB)
    VerifyB = Verify(signB, publicKeyB)
    print("result of verifying signature B:", VerifyB)

    k = 55555
    k1, S1 = SendKey(publicKeyA, publicKeyB, privateKeyA, k)
    print("Sended values by user A to user B: ( k1 -", k1, ", S1 -", S1, ")")
    result = ReceiveKey(privateKeyB, k1, S1, publicKeyA)
    print("Authentication of user A:", result)

    #Server check

    # publicKeyServer = (int("ABB56B149D2B8AC5BA1C9764C4431C7A6CAFC0D6FFE1145B4B4C30905B17F3B9", 16), 
    #                    int("10001", 16))

    # pProgram = GenerateRandomPrime(length = 128)
    # qProgram = GenerateRandomPrime(length = 128)

    # publicKeyProgram, privateKeyProgram = GenerateKeyPair(pProgram, qProgram)

    # print(publicKeyProgram)
    # print(privateKeyProgram)

    # publicKeyProgram = (41887016183231955725709937040856737739607424282165092723873588768948795089469,
    #                     65537)
    
    # privateKeyProgram = (25178738766474249596630040583556634927380026189639794459545454434999512306773,
    #                      209439695060123648592801721058537048411,
    #                      199995593820968326575863902654491115079)

    
    # print("Public key of program:", hex(publicKeyProgram[0])[2:].upper())

    # encryptedByServer = int("345309F52AD379F345916874A9071CB08EA2480421BC2E61E44F40FA25962FB3", 16)
    # decryptedByProgram = Decrypt(encryptedByServer, privateKeyProgram)
    # print("Decrypted by program:", hex(decryptedByProgram)[2:].upper())

    # message = 999999999
    # print("hex of", message, ":", hex(message)[2:].upper())
    # encryptedByProgram = Encrypt(message, publicKeyServer)
    # print("Encrypted by program:", hex(encryptedByProgram)[2:].upper())

    # message = 55555
    # print("hex of", message, ":", hex(message)[2:].upper())

    # signByServer = int("6BFD032DDE2250D28AAC82B841FBE0474A75DCA42A057FBB0B008EF6E9C38734", 16)
    # verifyByProgram = Verify((message, signByServer), publicKeyServer)
    # print("Result of verifying by program:", verifyByProgram)

    # message = 22
    # print("hex of", message, ":", hex(message)[2:].upper())
    # signByProgram = Sign(message, privateKeyProgram)
    # print("Sign by program:", hex(signByProgram[1])[2:].upper())

    # kServer = int("2FC51C5D61B20DAF21D639DDDF0F9381295774B4DDF9ED5DDD1D5D5E5AD49F0F", 16)
    # sServer = int("37CEF8F0892B53D9EDB79C7B7810134B7415D8140EAA323722CF3B25146B3156", 16)
    # receiveResult = ReceiveKey(privateKeyProgram, kServer, sServer, publicKeyServer)
    # print("Result of receiving key:", receiveResult)

    # kProgram = 565655
    # print("hex of", kProgram, ":", hex(kProgram)[2:].upper())
    # sendResult = SendKey(publicKeyProgram, publicKeyServer, privateKeyProgram, kProgram)
    # print("kProgram:", hex(sendResult[0])[2:].upper())
    # print("sProgram:", hex(sendResult[1])[2:].upper())

if __name__ == "__main__":
    main()