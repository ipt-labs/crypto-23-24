import string
import collections
import re
import math
import random

def stepin(x, a, n):
    arr_a = []
    while (a!=0):
        arr_a.insert(0, a%2)
        a = a//2
    y = 1
    for i in range(0, len(arr_a)):
        y = (y*y)%n
        if (arr_a[i]==1):
            y = (y*x)%n
        else:
            y = y%n
    return y



def evclid(a, b):
    u, u_temp, v, v_temp = 1, 0, 0, 1
    while (b!=0):
        q = a // b
        a, b = b, a % b
        u, u_temp = u_temp, u - u_temp*q
        v, v_temp = v_temp, v - v_temp*q
    return (u, v, a)

def rivnyanya(a, b, n):
    all_x = []
    gcd = evclid(a, n)[2]
    if (gcd==1):
        all_x.append((evclid(a, n)[0])*b%n)
        return all_x
    if (b%gcd!=0):
        return None
    x = (evclid(a//gcd, n//gcd)[0])*(b//gcd)%(n//gcd)
    for i in range(gcd):
        x_temp = x + (n//gcd)*i
        all_x.append(x_temp)
    return all_x

def CheckTriv(n):
    """ Check if the number is prime using trial division """

    trivial_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    for i in trivial_prime:
        if (n % i == 0):
            return False
    return True

def MillerRabin(n, k=20):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for i in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def GenerateTriv(n):
    p = random.getrandbits(n)
    if (CheckTriv(p)==True):
        if (MillerRabin(p, 20)==True):
            return p
        else:
            return  GenerateTriv(n)
    else:
        return GenerateTriv(n)

def GenerateQP(n):
    p = GenerateTriv(n)

    q = GenerateTriv(n)
    """
    i = 1
    p = 2*i*p+1
    while (MillerRabin(p, 20)!=True):
        i = i+1
        p = 2 * i * p + 1

    j = 1
    q = 2 * j * q + 1
    while (MillerRabin(q, 20) != True):
        j = j + 1
        q = 2 * j * q + 1
    """

    return (p, q)

def GenerateKayPair(x):
    s = GenerateQP(x)
    p = s[0]
    q = s[1]
    n = p*q
    o = (p-1)*(q-1)
    e = 65537
    d = rivnyanya(e, 1, o)
    public = (n, e)
    privat = (p, q, d)
    return public, privat

def Encrypt(text, n, e):
    c = pow(text, e, n)
    return c

def Decrypt(text, d, n):
    m = pow(text, d, n)
    return m

def Sign(text, d, n):
    s = Decrypt(text, d, n)
    return s

def Verify(m, s, e, n):
    if (m==pow(s, e, n)):
        return True
    else:
        return False

def SendKey(k, n, n1, e1, d):
    k1 = Encrypt(k, n1, e1)
    s = Sign(k, d, n)
    s1 = Encrypt(s, n1, e1)
    return (k1, s1)

def ReceiveKey(k1, s1, d1, n, e, n1):
    k = Decrypt(k1, d1, n1)
    s = Sign(s1, d1, n1)
    if (Verify(k, s, e, n)):
        return k
    else:
        return 'Not verify'


"""print(pow(6,3)%7)
x = GenerateKayPair()
print(x)
public = x[0]
privat = x[1]
n = public[0]
e = public[1]
d = privat[2]
d1 = d[0]
print(Encrypt(37, n, e))
num = Encrypt(37, n, e)
print(Decrypt(num,d1, n))"""



print(pow(7, 8, 11))
print(stepin(7, 8, 11))
print(MillerRabin(997))
g = GenerateQP(256)[0]
print(g)
print(len(bin(g))-2)
nt = int("A5AF350F2DEBA38E405F663435CD4A2CF1F949AFF52BB09BF93DC4E0E8C4EFD7", 16)
et = int("10001", 16)
M = "Hello"
if not isinstance(M, int):
    M = int.from_bytes(M.encode('utf-8'), byteorder='big')
print(Encrypt(M, nt, et))
print(hex(Encrypt(M, nt, et)))

print('Abonen A generate key...')
#A abonent
x_a = GenerateKayPair(265)
public_a = x_a[0]
privat_a = x_a[1]
n = public_a[0]
e = public_a[1]
d = privat_a[2][0]
print(n, e, d)
print(len(bin(n))-2)

print('Abonen B generate key...')
#B abonent
x_b = GenerateKayPair(265)
while (x_b[0][0]<n):
    x_b = GenerateKayPair(265)
public_b = x_b[0]
privat_b = x_b[1]
n1 = public_b[0]
e1 = public_b[1]
d1 = privat_b[2][0]
print(n1, e1, d1)
print((len(bin(n1))-2))

print('Abonen A encrypt message...')
#A abonent
k = int(input('A number'))
message_a = SendKey(k, n, n1, e1, d)
print(message_a)

print('Abonen B decrypt message...')
#B abonent
encrypt_a = ReceiveKey(message_a[0], message_a[1], d1, n, e, n1)
print(encrypt_a)





