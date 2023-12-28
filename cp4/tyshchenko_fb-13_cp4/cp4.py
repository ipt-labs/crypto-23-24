#!/bin/python3

from random import randint, getrandbits
import sys

MAX_K = 20

# Transform integer to hexadecimal in server's formatting.
# Returns hex of a.
def to_hex(a: int) -> str:
    return hex(a)[2:].upper()

# Calculate gcd and inverses.
# Return list [gcd(a, b), a^(-1), b^(-1)].
def euclid(a: int, b: int) -> list:
    # Make positive.
    a, b = abs(a), abs(b)
    # Initialize base values.
    u = [1, 0]
    v = [0, 1]
    a0, b0 = a, b
    # Swap values if necessary.
    if a > b:
        a, b = b, a
        u, v = v, u
        a0, b0 = b, a
    r = a % b
    q = [a // b]
    # Find gcd(a, b) and inverses.
    while a % b:
        a = b
        b = r
        r = a % b
        u.append(u[-2] - q[-1] * u[-1])
        v.append(v[-2] - q[-1] * v[-1])
        q.append(a // b)
    # If found inverses are negative, make them positive.
    if u[-1] < 0:
        u[-1] += b0
    if v[-1] < 0:
        v[-1] += a0
    return [b, u[-1], v[-1]]
    
# Calculate euler function of a.
# Returns phi(n).
def euler(n: int, p=0, q=0) -> int:
    # Case incorrect input.
    if n <= 0:
        print(f"euler: incorrect input {n}")
        return -1
    # Case factorization is given.
    if p != 0 and q != 0:
        result = (p - 1) * (q - 1)
    else:
        # Count number of coprime numbers to a that are less than a.
        result = 1
        for i in range(2, n):
            if euclid(n, i)[0] == 1:
                result += 1
    return result
    
# Calculate x in power a with module m (Horner's scheme).
# Returns x ^ a mod m.
def horner(x: int, a: int, m: int) -> int:
    # Transform a to binary form.
    # Return coefficient list [a_0, a_1, ... , a_k-1].
    def to_bin(a: int) -> list:
        result = []
        while a != 0:
            result.append(a % 2)
            a //= 2
        return result
        
    # Case incorrect input.
    if x < 0 or x >= m or a < 0:
        print(f"horner: incorrect input x={x}, a={a}, m={m}")
        return -1
    a_bin = to_bin(a)
    k = len(a_bin)
    y = 1
    for i in range(k - 1, -1, -1):
        y = (y ** 2) % m
        y = (y * x ** a_bin[i]) % m
    return y
    
# Check if p is prime.
# Returns True if it is and False otherwise.
def miller_rabin(p: int, k=MAX_K) -> bool:
    # Find such d and s that: p - 1 = d * 2 ^ s.
    # Returns list [d, s].
    def decompose(p: int) -> list:
        if p % 2 == 0:
            print(f"miller_rabin (decompose): incorrect input {p}")
            return -1
        d = p - 1
        s = 0
        # Divide p - 1 by 2 s times.
        # What is left is d.
        while d % 2 == 0:
            s += 1
            d //= 2
        return [d, s]
        
    # Check if p is a strong pseudoprime with base a (2 methods).
    # Returns True if it is and False otherwise.
    def is_pseudoprime(p: int, a: int, d: int, s: int) -> bool:
        # Method I.        
        # Check if a ^ d = 1 (mod p).
        if pow(a, d, p) == 1:
            return True
        # Method II.
        else:
            # 0 <= r < s.
            for r in range(s):
                # Check if a ^ (d * 2 ^ r) = -1 (mod p).
                if pow(a, d * 2 ** r, p) == p - 1:
                    return True
            return False
          
    # Preprocess.
    d, s = decompose(p)
    for a in [2, 3, 5, 7]:
        if not is_pseudoprime(p, a, d, s):
            return False
    # Initialize algorithm.
    counter = 0
    while counter < k:
        x = randint(2, p - 1)
        if euclid(p, x)[0] != 1:
            return False
        if not is_pseudoprime(p, a, d, s):
            return False
        else:
            counter += 1
    return True

# NOT USED
# Get a random prime number withing range [n0, n1].
def get_prime(n0: int, n1: int, k=MAX_K) -> int:
    while True:
        x = randint(n0, n1)
        m0 = x + (x % 2 == 0)
        last = (n1 - m0) // 2
        for i in range(last + 1):
            if miller_rabin(m0 + 2 * i, k):
                return m0 + 2 * i

# Get a random prime that is suitable for RSA.
# Returns prime number such p that: p = 2ip' + 1.
# p' - a prime number.
def get_RSA_prime(bits=256, k=MAX_K, simple=False) -> int:
    MAX_ITERS = 5
    
    # Generate random prime of a specified size.
    def get_RSA_prime() -> int:
        nonlocal bits, k
        while True:
            x = getrandbits(bits)
            # If x is even, make it odd.
            x += (x % 2 == 0)
            for p in range(x, (2 * x - 2) + 1, 2):
                if miller_rabin(p, k):
                    return p

    p1 = get_RSA_prime()
    # If necessary, try to find such p that: p = 2ip' + 1. 
    if not simple:
        i = 1
        counter = 0
        while counter < MAX_ITERS:
            p = 2 * i * p1 + 1
            if miller_rabin(p, k):
                return p
            i += 1
            counter += 1
    return p1

# Generate key pair list.
# Returns key list [public_key, private_key].
# public_key = [e, n]
# private_key = [d, p, q, phi(n)]
def generate_key_pair(bits=128, simple=False, e=2**16+1) -> list:
    # Set basic case.
    p = get_RSA_prime(bits=bits, simple=simple)
    q = get_RSA_prime(bits=bits, simple=simple)
    n = p * q
    phi = euler(n, p=p, q=q)
    # Find suitable primes p and q.
    val = euclid(e, phi)
    while val[0] != 1:
        p = get_RSA_prime(bits=bits, simple=simple)
        q = get_RSA_prime(bits=bits, simple=simple)
        n = p * q
        phi = euler(n, p=p, q=q)
        val = euclid(e, phi)
    d = val[1]
    return [[e, n], [d, p, q, phi]]

# Encrypt a message M with a public key pubkey = [e, n].
# Returns encrypted message.
def encrypt(M: int, pubkey: list) -> int:
    e, n = pubkey
    # Case invalid input.
    if M >= n:
        print(f"encrypt: invalid input M={M} >= n={n}")
        return -1
    
    return horner(M, e, n)
    
# Decrypt a message C with a private key privkey = [d, p, q].
# Returns decrypted message.
def decrypt(C: int, privkey: list) -> int:
    d, p, q, _ = privkey
    n = p * q
    # Case invalid input.
    if C >= n:
        print(f"decrypt: invalid input C={C} >= n={n}")
        return -1

    return horner(C, d, n)

# Sign message M with a private key privkey = [d, p. q].
# Returns list [M, S].
# S - digital signature.
def sign(M: int, privkey: list) -> list:
    d, p, q, _ = privkey
    S = horner(M, d, p * q)
    return [M, S]

# Check digital signature with a public key pubkey = [e, n].
# Returns True if signature is correct and False otherwise.
def verify(signed: list, pubkey: list) -> bool:
    M, S = signed
    e, n = pubkey
    return horner(S, e, n) == M

# A sends encrypted signed secret key k to B.
# k - secret key.
# privkeyA = [d, p, q, phi(n)]
# pubkeyA = [e, n]
# pubkeyB = [e1, n1]
# Returns list [k1, S1]
def send_key(k: int, privkeyA: list, pubkeyA: list, pubkeyB: list) -> list:
    d, p, q, _ = privkeyA
    e, n = pubkeyA
    e1, n1 = pubkeyB
    # Case invalid input.
    if k >= n:
        print(f"send_key: invalid input k={k} >= n={n}")
        return -1
    if n1 < n:
        print(f"send_key: invalid input n1={n1} < n={n}")
        return -1
        
    # Calculate digital signatures S, S1 and key k1.
    S = horner(k, d, n)
    S1 = horner(S, e1, n1)
    k1 = horner(k, e1, n1)
    return [k1, S1]

# B receives encrypted signed secret key k from A and verifies it.
# k - secret key.
# privkeyB = [d1, p1, q1, phi(n1)]
# pubkeyA = [e, n]
# pubkeyB = [e1, n1]
# Returns True if signature is correct and False otherwise.
def receive_key(signed: list, privkeyB: list, pubkeyA: list, pubkeyB: list) -> bool:
    k1, S1 = signed
    d1, p1, q1, _ = privkeyB
    e1, n1 = pubkeyB
    # Restore digital signature S and key k.
    k = horner(k1, d1, n1)
    S = horner(S1, d1, n1)
    return [k, S]
    
# Test all functions.
def tests() -> None:
    # Find gcd and inverses.
    print(f"""\n=== GCD & INVERSES TEST ===
euclid(155, 29) = {euclid(155, 29)}
euclid(2, -5) = {euclid(2, -5)}
euclid(-15, 40) = {euclid(-15, 40)}""")

    # Find euler function.
    print(f"""\n=== EULER FUNCTION TEST ===
phi(1) = {euler(1)}
phi(5) = {euler(5)}
phi(6) = {euler(6)}
phi(23147) (factorization is unknown) = {euler(23147)}
phi(23147) (factorization is given) = {euler(23147, p=79, q=293)}""")
    #print(f"phi(-1) = {euler(-1)}")
    
    # Calculate x ^ a (mod m).
    print(f"""\n=== HORNER'S SCHEME TEST ===
14 ^ 8 mod 23 = {horner(14, 8, 23)}
1 ^ 25 mod 456 = {horner(1, 25, 456)}""")
    '''
    print(f"""3 ^ 2 mod 2 = {horner(3, 2, 2)}
2 ^ 0 mod 3 = {horner(2, 0, 3)}
0 ^ 145 mod 89 = {horner(0, 145, 89)}
12 ^ -5 mod 9 = {horner(12, -5, 9)}
-7 ^ 1 mod 5 = {horner(-7, 1, 5)}""")
    '''
    
    # Check prime number.
    print(f"""\n=== PRIME CHECK TEST ===
9 is prime == {miller_rabin(9)}
13 is prime == {miller_rabin(13)}
23 is prime == {miller_rabin(23)}
293 is prime == {miller_rabin(293)}""")
    '''
    print(f"""0 is prime == {miller_rabin(0)}
1 is prime == {miller_rabin(1)}
2 is prime == {miller_rabin(2)}""")
    '''
    
    # Find some prime number on interval.
    print(f"""\n=== PRIME GENERATION TEST ===
(1, 100) = {get_prime(1, 100)}
(250, 1000) = {get_prime(250, 1000)}
(500, 10000) = {get_prime(500, 10000)}
(5000, 10000) = {get_prime(5000, 10000)}
RSA prime = {get_RSA_prime(k=10)}""")

    # Generate key pair for RSA.
    pubkey, privkey = generate_key_pair()
    print(f"""\n=== RSA KEY PAIR GENERATION TEST ===
Public key:
\te = {pubkey[0]}
\tn = {pubkey[1]}
Private key:
\td = {privkey[0]}
\tp = {privkey[1]}
\tq = {privkey[2]}""")

    # Encrypt and decrypt a message.
    M = randint(1, 2 ** 16)
    C = encrypt(M, pubkey)
    print(f"""\n=== RSA ENCRYPTION/DECRYPTION TEST ===
Original:\t{M}
Encrypted:\t{C}
Decrypted:\t{decrypt(C, privkey)}""")

    # Sign and verify a message.
    signed = sign(M, privkey)
    print(f"""\n=== RSA SIGN/VERIFY TEST ===
Message:\t{signed[0]}
Signature:\t{signed[1]}
Correct (right key):\t{verify(signed, pubkey)}""")
#Correct (wrong key):\t{verify(signed, [29, 79])}

    # Key transferring.
    k = get_prime(1, 100)
    # Generate such pair of keys that: nA <= nB.
    pubkeyA, privkeyA = generate_key_pair()
    pubkeyB, privkeyB = generate_key_pair()
    while pubkeyA[1] > pubkeyB[1]:
        pubkeyA, privkeyA = generate_key_pair()
    # Send and receive key.
    signed = send_key(k, privkeyA, pubkeyA, pubkeyB)
    received = receive_key(signed, privkeyB, pubkeyA, pubkeyB)
    print(f"""\n=== RSA SEND/RECEIVE KEY TEST ===
Secret key:\t{k}
A keys:
\te\t= {pubkeyA[0]}
\tn\t= {pubkeyA[1]}
\td\t= {privkeyA[0]}
\tp\t= {privkeyA[1]}
\tq\t= {privkeyA[2]}
\tphi(n)\t= {privkeyA[3]}
B keys:
\te1\t= {pubkeyB[0]}
\tn1\t= {pubkeyB[1]}
\td1\t= {privkeyB[0]}
\tp1\t= {privkeyB[1]}
\tq1\t= {privkeyB[2]}
\tphi(n1)\t= {privkeyB[3]}
Encrypted key:\t{signed[0]}
Encrypted signature:\t{signed[1]}
Decrypted key:\t{received[0]}
Decrypted signature:\t{received[1]}""")
    
# Establish RSA communication between client and server.
# Server link: http://asymcryptwebservice.appspot.com/?section=rsa
# Receives input and shows output.
def RSA(pubkey_server: list) -> None:
    # Create client key pair.
    pubkey_client, privkey_client = generate_key_pair()
    e_client, n_client = pubkey_client
    # Store server's public key.
    e_server, n_server = pubkey_server
    if n_client > n_server:
        print("[INFO] Client's modulus is greater than server's: " + \
            "possible data loss during encryption and key sending.")
    # Processing loop.
    while True:
        cmd = input("\nEnter command (\'h\' for help): ")
        
        if cmd == 'h':
            print("""[INFO] All input data must be hexadecimal.
[INFO] Command list:
\th\t- show this message.
\tk\t- list client's and server's public keys.
\tg[+-]\t- generate new key pair for client (modulus greater or less than server's respectively).
\tu\t- update server public key.
\tq\t- terminate program.
\te\t- encrypt specified message.
\td\t- decrypt specified ciphertext.
\tsi\t- sign specified message.
\tv\t- verify server's signed message.
\tse\t- send encrypted signed key to server.
\tr\t- receive encrypted signed key from server and verify it.""")

        # Show client's and server's public keys.
        elif cmd == 'k':
            print(f"""\n=== CLIENT KEYS ===
Modulus:\t{to_hex(n_client)}
Public exponent:\t{to_hex(e_client)}
d:\t{to_hex(privkey_client[0])}
p:\t{to_hex(privkey_client[1])}
q:\t{to_hex(privkey_client[2])}
phi(n):\t{to_hex(privkey_client[3])}\n
=== SERVER PUBLIC KEY ===
Modulus:\t{to_hex(n_server)}
Public exponent:\t{to_hex(e_server)}""")

        # Generate new key pair for client.
        elif cmd[0] == 'g':
            # Case incorrect parameter.
            if len(cmd) < 2 or cmd[1] not in "+-":
                print(f"[ERROR] Incorrect command \'g[+-]\' syntax: {cmd}")
                continue
            # Case client's modulus should be less than server's.
            elif cmd[1] == '-':
                while n_client > n_server:
                    pubkey_client, privkey_client = generate_key_pair()
                    e_client, n_client = pubkey_client
            # Case client's modulus should be greater than server's.
            else:
                while n_client < n_server:
                    pubkey_client, privkey_client = generate_key_pair()
                    e_client, n_client = pubkey_client
            print("[INFO] Generated new key pair for client (\'k\' to show).")
                    
        # Update server public key (modulus and public exponent).
        elif cmd == 'u':
            n_server = int(input("Enter server's modulus: "), 16)
            e_server = int(input("Enter server's public exponent: "), 16)
            print("[INFO] Updated server's public key (\'k\' to show).")
            if n_client > n_server:
                print("[INFO] Client's modulus is greater than server's: " + \
                    "possible data loss during encryption and key transferring.")

        # Encrypt message on client to decrypt it on server.
        elif cmd == 'e':
            M = int(input("Enter message M: "), 16)
            C = encrypt(M, pubkey_server)
            print(f"Encrypted message C:\t{to_hex(C)}")
            
        # Decrypt encrypted message by server on client.
        elif cmd == 'd':
            C = int(input("Enter encrypted message C: "), 16)
            M = decrypt(C, privkey_client)
            print(f"Decrypted message M:\t{to_hex(M)}")
        
        # Sign a message for server.
        elif cmd == "si":
            M = int(input("Enter message M: "), 16)
            signed = sign(M, privkey_client)
            S = signed[1]
            print(f"Message:\t{to_hex(M)}\nSignature:\t{to_hex(S)}")
        
        # Verify a message signed by server.
        elif cmd == 'v':
            M = int(input("Enter message M: "), 16)
            S = int(input("Enter signature S: "), 16)
            signed = [M, S]
            result = verify(signed, pubkey_server)
            print(f"[INFO] {result}")
            
        # Send a key to server.
        elif cmd == "se":
            k = get_RSA_prime()
            while k >= n_client:
                k = get_RSA_prime()
            signed = send_key(k, privkey_client, pubkey_client, pubkey_server)
            k1, S1 = signed
            print(f"""Key k:\t{to_hex(k)}
Encrypted key k1:\t{to_hex(k1)}
Encrypted signature S1:\t{to_hex(S1)}""")
            
        # Receive and verify a key from server.
        elif cmd == 'r':
            k1 = int(input("Enter encrypted key k1: "), 16)
            S1 = int(input("Enter encrypted signature S1: "), 16)
            signed = [k1, S1]
            received = receive_key(signed, privkey_client, pubkey_server, pubkey_client)
            k, S = received
            result = verify(received, pubkey_server)
            print(f"""Decrypted key k:\t{to_hex(k)}
Decrypted signature S:\t{to_hex(S)}
[INFO] {result}""")
            
        # Quit program.
        elif cmd == 'q':
            print("[INFO] Finishing program...")
            break
            
        # Case incorrect command.
        else:
            print(f"[ERROR] Incorrect command passed: {command}")

if __name__ == "__main__":
    # Get server's modulus and public exponent as arguments.
    if len(sys.argv) == 3:
        n_server = int(sys.argv[1], 16)
        e_server = int(sys.argv[2], 16)
        pubkey_server = [e_server, n_server]
        print("[INFO] Starting RSA...")
        RSA(pubkey_server)
    # Run tests.
    elif len(sys.argv) > 1 and sys.argv[1] == 't':
        print("[INFO] Establishing tests...")
        tests()  
        sys.exit(0)
    else:
        print(f"""USAGE: {sys.argv[0]} MODULUS PUBEXP
\tMODULUS\t- server's modulus (hex).
\tPUBEXP\t- server's public exponent (hex).""")
