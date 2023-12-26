from main import *

sent = True
while sent:
        p = generate_random_prime(256)
        p1 = generate_random_prime(256)
        q = generate_random_prime(256)
        q1 = generate_random_prime(256)
        if p * q < p1 * q1 or p * q == p1 * q1:
            sent = False

A_keypair = GenerateKeyPair(p,q)
B_keypair = GenerateKeyPair(p1,q1)
A_public = A_keypair[0]
A_private = A_keypair[1]
B_public = B_keypair[0]
B_private = B_keypair[1]
text_message='RSA is cool. Best computer workshop' 
print(text_message)
pt = Text2Bytes(text_message)
print(pt)
ct = Encode(pt, A_public)
print(ct)
pt_dec= Decode(ct, A_private)
print(Bytes2Text(pt_dec))

