import random
import secrets
import hashlib

def d_2s(p):
    s = 0
    while p % 2 == 0:
        s += 1
        p //= 2
    return s, p

def power_barrett(A, B, N):
    if N == 1:
        return 0
    result = 1
    A = A % N
    while B > 0:
        if B % 2 == 1:
            result = (result * A) % N
        B = B // 2
        A = (A * A) % N
    return result

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def find_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

def is_prime_miller_rabin(p, k):
    if(p == 2 or p == 3):
        return True
    elif(p == 1):
        return False
    s, d = d_2s(p - 1)
    for _ in range(k):
        x = random.randint(2, p - 2)
        gcd, _, _ = extended_gcd(x, p)
        if gcd > 1:
            return False
        else:
            l = power_barrett(x, d, p)
            if l != 1 and l != p - 1:
                for r in range(1, s):
                    xr = power_barrett(x, d * 2 ** r, p)
                    if xr == p - 1:
                        break
                else:
                    return False
    return True

def find_prime():
    while(True):
        prime = secrets.randbits(256)
        if(is_prime_miller_rabin(prime, 20)):
            return prime


def find_p1q1p2q2():
    while(True):
        p1 = find_prime()
        q1 = find_prime()
        p2 = find_prime()
        q2 = find_prime()
        if((p1*q1) < (p2*q2)):
            return p1, q1, p2, q2

def generate_key_pair(p, q):
    n = p*q
    euler = (p-1)*(q-1)
    e = 1
    while(True):
        e = random.randint(2, euler)
        if(extended_gcd(e, euler)[0] == 1):
            break
    d = find_inverse(e, euler)
    return e, n, d

def encrypt(public_key, message):
    e, n = public_key
    if type(message) == str:
        message = int.from_bytes(message.encode('utf-8'), 'big')
    return power_barrett(message, e, n)

def decrypt(private_key, message, check):
    d, n = private_key
    message = power_barrett(message, d, n)
    if check == "text":
        message = message.to_bytes((message.bit_length()+7) // 8, 'big').decode('utf-8')
    return message

def sign(private_key, message):
    hashed_data = message
    if type(message) == str:
        hashed_data = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    signature = encrypt(private_key, hashed_data)
    return hashed_data, signature

def verify(public_key, signature):
    e, n = public_key
    check_data = power_barrett(signature[1], e, n)
    if(check_data == signature[0]):
        return True
    return False

def send(private_key_A, public_key_B, k):
    k_1 = encrypt(public_key_B, k)
    s = sign(private_key_A, k)
    s_1 = encrypt(public_key_B, s[1])
    return k_1, s_1

def receive(private_key_B, public_key_A, message):
    k_1, s_1 = message
    k = decrypt(private_key_B, k_1, None)
    s = decrypt(private_key_B, s_1, None)
    signature = (k, s)
    if(verify(public_key_A, signature)):
        return "Received"
    return "Not received"

def generate_key_pair_web(p, q):
    n = p*q
    euler = (p-1)*(q-1)
    e = int("10001", 16)
    while(True):
        if(extended_gcd(e, euler)[0] == 1):
            break
    d = find_inverse(e, euler)
    return e, n, d

if __name__ == "__main__":
    p1q1p2q2 = find_p1q1p2q2()
    pairs2 = generate_key_pair(p1q1p2q2[2], p1q1p2q2[3])
    e, n, d = generate_key_pair(p1q1p2q2[0], p1q1p2q2[1])
    e1, n1, d1 = generate_key_pair(p1q1p2q2[2], p1q1p2q2[3])
    public_key_A = (e, n)
    private_key_A = (d, n)
    public_key_B = (e1, n1)
    private_key_B = (d1, n1)
    print(f"User A:\nPrivate key: d = {private_key_A[0]}\nPublic key: e = {public_key_A[0]} n = {public_key_A[1]}")
    print("-"*100)
    print(f"User B:\nPrivate key: d = {private_key_B[0]}\nPublic key: e = {public_key_B[0]} n = {public_key_B[1]}")
    print("-" * 100)
    message = "hello"
    print(f"Message to encrypt: {message}")
    encrypted = encrypt(public_key_A, message)
    print(f"Message after encryption: {encrypted}")
    decrypted = decrypt(private_key_A, encrypted, "text")
    print(f"Message after decryption: {decrypted}")
    print("-" * 100)
    signature = sign(private_key_A, message)
    print(f"Signaturing the message '{message}':\nHash:{signature[0]}\nSignature:{signature[1]}")
    print("-"*100)
    sending = send(private_key_A,public_key_B,4)
    print("Trying to send")
    if(receive(private_key_B, public_key_A, sending)):
        print("Message received")
    else:
        print("Message not received")
    print("-" * 100)

    #qwe = generate_key_pair_web(find_prime(), find_prime())
    #print(qwe)
    #Test on website
    print("Testing RSA on website")
    d_3 = 2030804600355989656815659171694724167096783934582712873616071780820613192418502922376992796103262865374617817094033046949352578385783699306075271865979441
    n_3 = 4820108688017184345166154394298027587245470401301870693835162114285112515990706668542359056152770218690569203160255850620642786051021824795390505063706113
    chiper = "19E0FC7C28A9B80940EB7750DAD0F39BFE9F0E104659B554FB30B023B5514CC5248F3DED79EDDAB474A3EC7A3750DDD89C7F62F048D73DD1DC050A0D54696F3F"
    chiper_int = int(chiper, 16)
    print(f"Encrypted message: {chiper}")
    print(f"Decryption...")
    print(f"Decrypted message: '{decrypt((d_3, n_3), chiper_int, "text")}'")
    test_message = "the last lab"
    print(f"Message to encrypt: '{test_message}'")
    n_web = int("A6105A98AEC232B99E09AF7A7E4E690698F83F7938F1262814304DB6E2683575", 16)
    e_web = int("10001", 16)
    encrypted_test_message = hex(encrypt((e_web, n_web), test_message))
    print(f"e on website = {e_web}\nn on website= {n_web}\nEncrypted message: {encrypted_test_message}")
    print("Result - 'the last lab'")
    print("-" * 100)
