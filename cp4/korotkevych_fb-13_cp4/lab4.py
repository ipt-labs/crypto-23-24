from random import seed
from random import randint
from random import randrange
import secrets
import json


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

#Function that implements Euclid algorithm
def egcd(a, b):
    u0, u1 = 1, 0
    v0, v1 = 0, 1

    while a != 0:
        q = b // a
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
        a, b = b % a, a

    return b, v0, u0


#Function that finds inverse element
def inverse_elem(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m


#Generate random 526 bit number
def number_256bit():
    random_number = secrets.randbits(256)
    return random_number


#Function to check if number is prime
def check_prime(p, k=15):

    if p % 2 == 0 or p % 3 == 0 or p % 5 == 0 or p % 7 == 0:
        return False
    
    s = 0
    d = (p - 1)
    while d % 2 == 0:
        d //= 2
        s += 1

    for i in range(k):
        x = randrange(2, p - 1)

        if gcd(x, p) > 1:
            return False
        
        a = pow(x, d, p)
        if a == 1 or a == -1:
            continue
        
        for _ in range(1, s):
            a = pow(a, 2, p)

            if a == p - 1:
                break
            
        else:
            return False
        
    return True  


#Function to select prime candidate
def select_prime(number):

    if number % 2 == 0:
        x = number + 1
    else:
        x = number

    i = 1
    while i < number / 2:
        if check_prime(x) == True:
            return x
        
        x += 2*i
        i += 1

    return x


#Generate key pair
def GenerateKeyPair(p, q):
    n = p*q
    phi_n = (p-1)*(q-1)
    exp = secrets.randbits(16)
    e = select_prime(exp)
    d = inverse_elem(e, phi_n)
    return n, e, d


#Encrypt message
def Encrypt(M, e, n):
    C = pow(M, e, n)
    return C


#Sign the message
def Sign(M, d, n):
    S = pow(M, d, n)
    return S


#Descrypt the message
def Decrypt(C, d, n):
    M = pow(C, d, n)
    return M


#Verify integrigty of the message
def Verify(M, S, e, n):
    if M == pow(S, e, n):
        return True
    return False


#Function that sends common secret
def SendKey(k, d, e1, n, n1):
    k1 = pow(k, e1, n1)
    S = pow(k, d, n)
    S1 = pow(S, e1, n1)
    return k1, S1


#Function that recieves common secret
def RecieveKey(k1, S1, d1, n1):
    k = pow(k1, d1, n1)
    S = pow(S1, d1, n1)
    return k, S


#Write keys from file
def write_to_file(filepath, data):
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=2)

    return True
    

#Read keys from file
def read_from_file(filepath):
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    return data


#Main activity
number1 = number_256bit()
number2 = number_256bit()
number3 = number_256bit()
number4 = number_256bit()
num1 = select_prime(number1)
num2 = select_prime(number2)
num3 = select_prime(number3)
num4 = select_prime(number4)


keys = [num1, num2, num3, num4]
keys.sort()
p = keys[0]
q = keys[1]
p1 = keys[2]
q1 = keys[3]

n, e, d = GenerateKeyPair(p, q)    #public and private keys for A
n1, e1, d1 = GenerateKeyPair(p1, q1)    #public and private keys for B

data = {
    "p" : p,
    "q" : q,
    "p1" : p1,
    "q1" : q1,
    "e" : e,
    "e1" : e1,
    "d" : d,
    "d1" : d1,
    "n" : n,
    "n1" : n1
}

json_file_path = input('Input file path:')
write_to_file(json_file_path, data)
data = read_from_file(json_file_path)
p = data["p"]
q = data["q"]
p1 = data["p1"]
q1 = data["q1"]
e = data["e"]
e1 = data["e1"]
d = data["d"]
d1 = data["d1"]
n = data["n"]
n1 = data["n1"]

M = 12345
Ma = 12345
Mb = 67890
Sb = Sign(Mb, d, n)       #Person A sings message with his private key (d) and public (n) and then encrypts message with persons B public key(e1, n1)
Cb = Encrypt(Mb, e1, n1)
Sa = Sign(Ma, d1, n1)
Ca = Encrypt(Ma, e, n)
print("Ciphertext for B: ", Cb)
print("e1: ", e1)
print("Modulus1: ", n1)
print("Signature for b: ", Sb)
print("Ciphertext for A: ", Ca)
print("e: ", e)
print("Modulus: ", n)
print("Signature for b: ", Sa)


DecMb = Decrypt(Cb, d1, n1) 
DecMa = Decrypt(Ca, d, n)
print("Verification result for B: ", Verify(DecMb, Sb, e, n)) 
print("e: ", e)
print("Modulus: ", n)                       #Person B decrypts message with his private key (d1) and public (n1) and the verifies if the message is correct with S and persons A public key(e,n)
print("Plaintext: ", DecMb)
print("Verification result: ", Verify(DecMa, Sa, e1, n1)) 
print("e1: ", e1)
print("Modulus1: ", n1)                       #Person B decrypts message with his private key (d1) and public (n1) and the verifies if the message is correct with S and persons A public key(e,n)
print("Plaintext: ", DecMa)



k1, S1 = SendKey(M, d, e1, n, n1)
print("k1", k1)
print("S1: ", S1)
k, S = RecieveKey(k1, S1, d1, n1)
print("k: ", k)
print("Verification result: ", Verify(k, S, e, n))