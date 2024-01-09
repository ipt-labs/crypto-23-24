import random

def gcd(a,b):
    dilene=a
    dilnik=b
    mnozhnik=[]
    ostatok=1

    u_0=0
    u_1=1
    while ostatok>0:
        mnozhnik=dilene//dilnik
        ostatok=dilene%dilnik
        dilene=dilnik
        gcd=dilnik
        dilnik=ostatok
        real_u=u_1
        temp=u_1
        u_1=u_0-mnozhnik*u_1
        u_0=temp
    if real_u<0:
        real_u=a+real_u
    if gcd!=1:
        real_u=None
    return gcd,real_u

def miller_rabin(p, iteration=500):
    if p < 2:
        return False
    if p != 2 and p % 2 == 0:
        return False

    d = p - 1
    while d % 2 == 0:
        d //= 2

    for _ in range(iteration):
        x = random.randint(1, p - 1)
        if gcd(x,p)[0]>1:
            continue
        temp = d
        mod = pow(x, temp, p)

        while temp != p - 1 and mod != 1 and mod != p - 1:
            mod = (mod * mod) % p
            temp *= 2

        if mod != p - 1 and temp % 2 == 0:
            return False

    return True

def generate_random_prime(bits=256):
    """
    Generates a random prime number with the specified number of bits.
    """
    while True:
        candidate = random.randint(2**(bits-1), 2**bits - 1)
        if candidate % 2 == 0:
            candidate += 1  # Ensure it's odd
        if miller_rabin(candidate):
            print("this worked out:",candidate)
            return candidate
        else:
            print("this value didnt work out:",candidate)


def generate_pairs():
    p=0
    q=0
    p_1=0
    q_1=0
    while True:
        p=generate_random_prime()
        q=generate_random_prime()
        p_1=generate_random_prime()
        q_1=generate_random_prime()
        if p*q<=p_1*q_1:
            break
    return p,q,p_1,q_1

def generate_rsa_keys(p, q, p_1, q_1):
    n = p * q
    phi_n = (p - 1) * (q - 1)

    while True:
        e = random.randint(2, phi_n - 1)
        gcd_1, d = gcd(phi_n,e)
        if gcd_1==1:
            break
        

    n_1 = p_1 * q_1
    phi_n_1 = (p_1 - 1) * (q_1 - 1)

    while True:
        e_1 = random.randint(2, phi_n_1 - 1)
        gcd_2, d_1 = gcd(phi_n_1,e_1)
        if gcd_2==1:
            break

    public_key = (n, e)
    private_key = (d, p, q)

    public_key_1 = (n_1, e_1)
    private_key_1 = (d_1, p_1, q_1)

    return public_key, private_key, public_key_1, private_key_1

# Example usage:
p, q, p_1, q_1 = generate_pairs()
public_key_A, private_key_A, public_key_B, private_key_B = generate_rsa_keys(p, q, p_1, q_1)

print("Public Key A:", public_key_A)
print("Private Key A:", private_key_A)
print("Public Key B:", public_key_B)
print("Private Key B:", private_key_B)
def encrypt(message, public_key):
    n, e = public_key
    if message >= n:
        raise ValueError("Message is too large for the given public key")
    ciphertext = pow(message, e, n)
    return ciphertext

def decrypt(ciphertext, private_key):
    d, p, q = private_key
    n = p * q
    print("d:",d)
    plaintext = pow(ciphertext, d, n)
    return plaintext
def sign(m,private_key):
    return pow(m,private_key[0],private_key[1]*private_key[2])
def verify(s,m,public_key):
    return m==pow(s,public_key[1],public_key[0])
message_to_encrypt = 123123123123 
ciphertext_A = encrypt(message_to_encrypt, public_key_A)
print("Ciphertext A:", ciphertext_A)

# Decrypt the ciphertext using private key A
decrypted_message_A = decrypt(ciphertext_A, private_key_A)
print("Decrypted Message A:", decrypted_message_A)
sign_val=sign(message_to_encrypt,private_key_A)
print("verification result A:",verify(sign_val,message_to_encrypt,public_key_A))
sign_val_b=sign(message_to_encrypt,private_key_B)
print("verification result B:",verify(sign_val_b,message_to_encrypt,public_key_B))

def send_key(public_key_B,private_key_A,public_key_A):
    k=random.randint(0,public_key_A[0]-1)
    print("k value:",k)
    s=pow(k,private_key_A[0],public_key_A[0])
    k_1=pow(k,public_key_B[1],public_key_B[0])
    S_1=pow(s,public_key_B[1],public_key_B[0])
    return k_1,S_1
def recv_key(k_1,S_1,public_key_B,private_key_B,public_key_A):
    k=pow(k_1,private_key_B[0],public_key_B[0])
    S=pow(S_1,private_key_B[0],public_key_B[0])
    return k== pow(S,public_key_A[1],public_key_A[0])

k_1,S_1=send_key(public_key_B,private_key_A,public_key_A)

print("perevirka pidpeesu:",recv_key(k_1,S_1,public_key_B,private_key_B,public_key_A))