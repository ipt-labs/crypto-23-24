import random
import secrets
import math
import string
import webbrowser

def open_webpage_with_web_browser(url):
    webbrowser.open(url)

def decimal_to_hex(decimal_num):
    decimal_num = int(decimal_num)
    res = hex(decimal_num)
    return res[2:].upper()

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def is_prime_miller_rabin(num, k=5):
    # Check for small numbers
    if num < 2:
        return False

    # Handle base cases
    if num == 2 or num == 3:
        return True

    # Check for even numbers (excluding 2)
    if num % 2 == 0:
        return False

    # Write num as 2^r * d + 1
    r, d = 0, num - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        # Choose a random base a in the range [2, num - 2]
        a = random.randint(2, num - 2)

        # Compute a^d % num
        x = pow(a, d, num)

        # Check if the result is 1 or num - 1
        if x == 1 or x == num - 1:
            continue  # Proceed to the next iteration

        # Repeat the square-and-multiply process r - 1 times
        for _ in range(r - 1):
            x = pow(x, 2, num)

            # If x becomes num - 1, it's not a witness
            if x == num - 1:
                break
        else:
            return False  # None of the bases were witnesses

    return True  # The number is probably prime


def GetPrime():
    random_number = secrets.randbits(256)
    while not is_prime_miller_rabin(random_number):
        random_number = secrets.randbits(256)
    return random_number
def _get_pq():
    num1 = GetPrime()
    num2 = GetPrime()
    return [num1, num2]

def get_pq():
    #a for p1 b for q2
    pq = _get_pq()
    p = pq[0]
    q = pq[1]
    pq1 = _get_pq()
    p1 = pq1[0]
    q1 = pq1[1]
    while p * q > p1 * q1:
        pq = _get_pq()
        p = pq[0]
        q = pq[1]
        pq1 = _get_pq()
        p1 = pq1[0]
        q1 = pq1[1]

    return [[p,q],[p1,q1]]


def generate_e(n):
    while True:
        candidate = random.randint(2, n-1)
        if math.gcd(n, candidate) == 1:
            return candidate

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def generate_d(p, q, e):
    phi_n = (p - 1) * (q - 1)
    d = modinv(e, phi_n)
    return d

def Generate_Keys():
    PQ_array = get_pq()
    e1 = generate_e((PQ_array[0][0]-1)*(PQ_array[0][1]-1))
    e2 = generate_e((PQ_array[1][0] - 1) * (PQ_array[1][1] - 1))
    d1 = generate_d(PQ_array[0][0], PQ_array[0][1], e1)
    d2 = generate_d(PQ_array[1][0], PQ_array[1][1], e2)
    n1 = PQ_array[0][0] * PQ_array[0][1]
    n2 = PQ_array[1][0] * PQ_array[1][1]
    return [[e1,n1,d1],[e2,n2,d2]]

def from_number_to_string(num):
    decoded_message_num = num
    decoded_message_num_without_first = str(decoded_message_num)[1:]
    decoded_message = ""
    i = 0
    while i < len(decoded_message_num_without_first) and decoded_message_num_without_first[i:i+3] != '':
        batch = int(decoded_message_num_without_first[i:i+3])
        char = chr(batch)
        decoded_message = decoded_message + char
        i = i + 3

    return decoded_message

def Encrypt(message, n, e): # n and e are public keys. Message will be a string without numbers. (n = p*q, e is coprime of (p-1)*(q-1))
    numbers = [ord(char) for char in message]
    message = ""
    temp = ""
    for num in numbers:
        if len(str(num)) == 2:
            temp = "0" + str(num)
            message = message + temp
        else:
            temp = str(num)
            message = message + temp
    message = str(1) + message
    #message = str(random.randint(1,9)) + message # to make possible 0XX code at first pos, delete first number when decode
    encoded_message = pow(int(message), e, n)
    return [encoded_message, int(message)]

def Decrypt(message, n, d):
    decoded_message_num = pow(message, d, n)
    decoded_message_num_without_first = str(decoded_message_num)[1:]
    decoded_message = ""
    i = 0
    while i < len(decoded_message_num_without_first) and decoded_message_num_without_first[i:i+3] != '':
        batch = int(decoded_message_num_without_first[i:i+3])
        char = chr(batch)
        decoded_message = decoded_message + char
        i = i + 3

    return decoded_message

#signatures
def generate_signature(message, n1, d1): #A needs his public part: n, and private part:d  to send somebody a signature
    signature = pow(message, d1, n1)
    return signature


def check_signature(message, signature, n1, e1):  #B needs A's public parts: n, e, to check signature
    return message == pow(signature, e1, n1)


def send_key(n2, e2, n1, d1):  #A needs B's public parts: e,n and A's private part: d and A's public part: n, to send a key
    key_init = random.randint(1,5087)
    key = pow(key_init, e2, n2)
    sign = generate_signature(key, n1, d1)
    sign = pow(sign, e2, n2)
    return [key, sign]

def receive_key(key, sign, n2, d2, e1, n1): #B needs B's private part: d and B's public part: n,
    key_check = pow(key, d2, n2)
    sign_check = pow(sign, d2, n2)
    return check_signature(key, sign_check, n1, e1)







def Routine():
    open_webpage_with_web_browser("http://asymcryptwebservice.appspot.com/?section=rsa")
    print("Enter 256 in 'Key size' space")
    server_modulus = input("Insert generated modulus here: ")
    server_exponent = input("Insert generated exponent here: ")
    server_modulus = int(server_modulus, 16)
    server_exponent = int(server_exponent, 16)
    print("*"*200)
    print("Press 'Encryption' button on the right side")
    print("Test message will be : 'Test message RSA'")
    print("Insert a server given modulus into 'Modulus' space")
    print("Insert a server given exponent into 'Public exponent' space")
    print(f"Insert this translated test message into 'Message': {decimal_to_hex(Encrypt('Test message RSA', server_modulus, server_exponent)[1])}")
    encoded_message_hex = input("Insert here generated encrypted message: ")
    encoded_message = int(encoded_message_hex, 16)
    print(f"Message encrypted locally: {decimal_to_hex(Encrypt('Test message RSA', server_modulus, server_exponent)[0])}")
    print(f"Are locally encrypted and server encrypted the same: {decimal_to_hex(Encrypt('Test message RSA', server_modulus, server_exponent)[0]) == encoded_message_hex[1:]}")
    print("*" * 200)
    print("Press 'Decryption' button on the left side")
    print("Insert into 'Ciphertext' message that was encrypted locally")
    server_decoded = input("Insert here from 'Message' space: ")
    print(f"Are locally decoded and server decoded messages the same: {decimal_to_hex(Encrypt('Test message RSA', server_modulus, server_exponent)[1]) == server_decoded}")
    print("*" * 200)
    print("Press 'Signature' button on the left side")
    print("Insert this translated test message into 'Message': BDE4C67958FC0264B93FC871F4A84B5132FE8CF9")
    server_generated_signature = input("Insert from 'Signature' space here: ")
    print(f"Locally checked signature result: {check_signature(int('BDE4C67958FC0264B93FC871F4A84B5132FE8CF9', 16), int(server_generated_signature, 16), server_modulus, server_exponent)}")
    print("*" * 200)
    print("Press 'Verification' button on the left side")
    print("Locally generated keys:")
    keys = Generate_Keys()
    print(f"Modulus : {decimal_to_hex(keys[0][1])}")
    print(f"Public exponent: {decimal_to_hex(keys[0][0])}")
    print(f"Private key: {decimal_to_hex(keys[0][2])}")
    message = Encrypt('Test message RSA', keys[0][1], keys[0][0])[1]
    print(f"Translated message: {decimal_to_hex(Encrypt('Test message RSA', keys[0][1], keys[0][0])[1])}")
    print("Generating a signature...")
    print(f"Locally generated Signature: {decimal_to_hex(generate_signature(message, keys[0][1], keys[0][2]))}")
    print("Insert Translated message into 'Message' space")
    print("Insert Locally generated Signature into 'Signature' space")
    print("Insert Modulus into 'Modulus' space")
    print("Insert Public exponent into 'Public exponent' space")
    print("*" * 200)
    print("Press 'Send key' button on the left side")
    print(f"Insert this modulus into 'Modulus' space: {decimal_to_hex(keys[0][1])}")
    print(f"Insert this public exponent into 'Public exponent': {decimal_to_hex(keys[0][0])}")
    server_key_hex = input(f"Insert here from 'Key' space: ")
    server_signature_hex = input(f"Insert here from 'Signature' space: ")
    server_key = int(server_key_hex, 16)
    server_signature = int(server_signature_hex, 16)
    result = receive_key(server_key, server_signature, keys[0][1], keys[0][2], server_exponent, server_modulus) #Maybe used wrong parameters??
    print(f"Is key received succ: {result}")
Routine()

