from random import randint

def euclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
        g, x, y = euclid(b, a % b)
        return (g, y, x - y * (a // b))

def inverted(a, mod):
    g, x, y = euclid(a, mod)
    if g != 1:
        return None
    return x

def RandomPrime(length = 256):
    while 1==1:
        num = randint(1 << (length - 1), (1 << length) - 1)
        if MillerRabinTest(num):
            return num

def MillerRabinTest(num, k = 100):
    if num % 2 == 0:
        return False
    s = 0
    d = num - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    for _ in range(k):
        x = randint(1, num)
        g, _, _ = euclid(num, x)
        if g != 1:
            return False
        xd = pow(x, d, num)
        if xd == 1 or xd == num - 1:
            continue
        xr = xd
        for _ in range(1, s):
            xr = pow(xr, 2, num)
            if xr == 1:
                return False
            elif xr == num - 1:
                break
        else:
            return False
    return True

def GenerateKeyPair(p, q):
    n = p * q
    e = (2**16) + 1
    f = (p-1)*(q-1)
    d = inverted(e, f)
    public_key = [n, e]
    private_key = d
    return public_key, private_key

def Encrypt(M, public_k):
    n = public_k[0]
    e = public_k[1]
    C = pow(M, e, n)
    return C

def Decrypt(C, d, n):
    M = pow(C, d, n)
    return M

def Sign(k, d, n):
    S = pow(k, d, n)
    return S

def Verify(k, S, public_k):
    n = public_k[0]
    e = public_k[1]
    return k == pow(S, e, n)

def SendKey(k, d, n, public_k1):
    k1 = Encrypt(k, public_k1)
    S = Sign(k, d, n)
    S1 = Encrypt(S, public_k1)
    return k1, S1

def ReceiveKey(k1, S1, d1, n1, public_k):
    k = Decrypt(k1, d1, n1)
    S = Decrypt(S1, d1, n1)
    verification = Verify(k, S, public_k)
    return verification, k


p = RandomPrime()
q = RandomPrime()
p1 = RandomPrime()
q1 = RandomPrime()
if p*q > p1*q1:
    public_keyA, dA = GenerateKeyPair(p1, q1)
    public_keyB, dB = GenerateKeyPair(p, q)
else:
    public_keyA, dA = GenerateKeyPair(p, q)                   #public_key = [n, e]
    public_keyB, dB = GenerateKeyPair(p1, q1)

print("Ключі абонента А: "+str(public_keyA)+" "+str(dA))
print("Ключі абонента B: "+str(public_keyB)+" "+str(dB))
M = randint(0, public_keyB[0])
print("Повідомлення: "+str(M))
C = Encrypt(M,public_keyB)
print("Абонент А зашифрував повідомлення: "+str(C))
Md = Decrypt(C, dB, public_keyB[0])
print("Абонент B розшифрував повідомлення: "+str(Md))
S = Sign(M, dA, public_keyA[0])
print("Абонент А підписав повідомлення: "+str(S))
print("Абонент B перевірив підпис: "+str(Verify(M, S, public_keyA)))
k = randint(0, public_keyB[0])
print("Секретний ключ k: "+str(k))
k1, S1 = SendKey(k, dA, public_keyA[0], public_keyB)
print("Абонент А відправив секретний ключ k: "+str(k1)+" "+str(S1))
verification, kk = ReceiveKey(k1, S1, dB, public_keyB[0], public_keyA)
print("Абонент B перевірив автентифікацію: "+str(S))
if verification:
    print("Перевірка пройшла успішно!")
    print("Абонент B розшифрував секретний ключ k: "+str(kk))
else:
    print("Перевірка пройшла неуспішно!")

#Server
p = RandomPrime()
q = RandomPrime()
public_keyA, dA = GenerateKeyPair(p, q)
print("Our public key: n="+str(hex(public_keyA[0]))+" e="+str(hex(public_keyA[1])))
n1 = int(str(input("Enter server Modulus: ")), 16)
e1 = int(str(input("Enter server exponent: ")), 16)
public_keyB = [n1, e1]
print("Decrypting message from server")
C1 = int(str(input("Enter ciphertext: ")), 16)
print("Decrypted message: "+ str(hex(Decrypt(C1, dA, public_keyA[0]))))
print("Encrypting message for server")
M = randint(0, public_keyB[0])
print("Message: "+ str(hex(M)))
C = Encrypt(M, public_keyB)
print("Encrypted message: "+ str(hex(C)))
print("Verifing signature from server")
sk = int(str(input("Enter server message: ")), 16)
sS =  int(str(input("Enter server signature: ")), 16)
if Verify(sk, sS, public_keyB):
    print("Verification successful!")
else:
    print("Verification failed!")
print("Signing message for server")
M = randint(0, public_keyB[0])
print("Message: "+ str(hex(M)))
print("Signed message: "+ str(hex(Sign(M, dA, public_keyA[0]))))
print("Receving key from server")
k1 = int(str(input("Enter server key: ")), 16)
S1 =  int(str(input("Enter server signature: ")), 16)
verification, kk = ReceiveKey(k1, S1, dA, public_keyA[0], public_keyB)
if verification:
    print("Verification successful!")
    print("Server key: "+str(hex(kk)))
else:
    print("Verification failed!")
print("Sending key to server")
while public_keyA[0]>public_keyB[0]:
    p = RandomPrime()
    q = RandomPrime()
    public_keyA, dA = GenerateKeyPair(p, q)
print("Our (possibly new) public key: n="+str(hex(public_keyA[0]))+" e="+str(hex(public_keyA[1])))
k = randint(0, public_keyB[0])
print("Open key: "+str(hex(k)))
k1, S1 = SendKey(k, dA, public_keyA[0], public_keyB)
print("Key: "+str(hex(k1)))
print("Signature: "+str(hex(S1)))
