import random

def generateSimple(left_b, right_b=0):
    while True:
        if right_b == 0:
            length = (2 ** left_b) - 1
            rand = random.randint(length, length * 2)
        else:
            rand = random.randint(left_b, right_b)

        def tryDivision(x):
            divisors = [2, 3, 5, 7, 11, 13, 17, 19]
            return all(x % d > 0 for d in divisors)

        def testMillerRabin(x):
            n, m = 0, x - 1
            while m % 2 == 0:
                n += 1
                m //= 2

            for _ in range(20):
                base = random.randint(2, x - 2)
                y = pow(base, m, x)

                if y == 1 or y == x - 1:
                    continue

                for _ in range(n - 1):
                    y = pow(y, 2, x)
                    if y == x - 1:
                        break
                else:
                    return False

            return True

        if tryDivision(rand) and testMillerRabin(rand):
            return rand

def keyGen():
    keyp1 = generateSimple(256)
    keyq1 = generateSimple(256)
    keyp2 = generateSimple(256)
    keyq2 = generateSimple(256)
    if keyp1*keyq1 >= keyp2*keyq2:
        return keyp1, keyq1, keyp2, keyq2
    else:
        return keyGen()

def genKeyPair(x, y):
    n = x*y
    m = (x-1)*(y-1)
    e = 65537
    d = pow(e, -1, m)
    openk = (n, e)
    secretk = (d, x, y)
    return openk, secretk

def encrypt(text,okey):
    encrypted = pow(text,okey[1],okey[0])
    return encrypted

def decrypt(text,okey,skey):
    decrypted = pow(text,skey[0],okey[0])
    return decrypted

def sign(text,okey,skey):
    signed = pow(text,skey[0],okey[0])
    return (text, signed)

def verify(signature, okey):
    if signature[0] == pow(signature[1], okey[1], okey[0]):
        return('Message is verified')
    else:
        return('Fake sign')


ap, aq, bp, bq = keyGen()

msga = 885555555588
msgb = 606060606060

aopen, asec = genKeyPair(ap, aq)
bopen, bsec = genKeyPair(bp, bq)

print("A's keys:", aopen, ",", asec)
print("B's keys:", bopen, ",", bsec)

aencrypted = encrypt(msga, aopen)
bencrypted = encrypt(msgb, bopen)

print("A's encrypted message:", aencrypted)
print("B's encrypted message:", bencrypted)

msga_decrypted = decrypt(aencrypted, aopen, asec)
msgb_decrypted = decrypt(bencrypted, bopen, bsec)

print("A's decrypted message:", msga_decrypted)
print("B's decrypted message:", msgb_decrypted)

asignature = sign(msga, aopen, asec)    
bsignature = sign(msgb, bopen, bsec)

print("A's signed message:", asignature)
print("B's signed message:", bsignature)

print("A's key verification:", verify(asignature, aopen))
print("B's key verification:", verify(bsignature, aopen))
