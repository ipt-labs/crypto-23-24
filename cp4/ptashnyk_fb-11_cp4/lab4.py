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
    #publicKeyServer = (4760048197000665795791613885719943586008752085234376197045500646937015811001627877789039059408854216981909573295563700874070918605082166848985524500710481, 
    #                   65537)
    #privateKeyServer = (1817674995470324583143581932405012560591040628729961681298513804266990519647271377104049990774111353269500135933418868718071722234497762180274312452252745, 
    #                    57118080886460008612666937053955382494938567652287974903213305464144007566799, 
    #                    83336977067957613182660920615611173339185099662998084735021632363480102218719)
    #
    #publicKeyProgram = (8684944387944291035534816841511807371169203898073859285737713058041207306048724858765575769198690546782598847971950460787003622258516572294037518768298897, 
    #                    65537)
    #privateKeyProgram = (1849842664621730603552657404071948961565999621789416692396855769675102808873331642555577728263684717097441031449023026663751280744731191780015611313757693, 
    #                     102859931232048261086373034384133824342961802102105418558751187833277027117727, 
    #                     84434670370830528756455114000739072414283248654816777815252463258248570485711)
    #
    #encryptedByServer = 1031372753584574620025735401026518734384613066620641376018720860559390532208356335779579099834102000918344081192243693730426379155522514228428908608816857
    #decryptedByProgram = Decrypt(encryptedByServer, privateKeyProgram)
    #print("Decryption by program:", decryptedByProgram)
    #message = 999999999
    #encryptedByProgram = Encrypt(message, publicKeyServer)
    #print("Encryption by program:", encryptedByProgram)

if __name__ == "__main__":
    main()