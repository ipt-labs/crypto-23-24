
import random
import hashlib




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
    return keyp1, keyq1, keyp2, keyq2

def genKeyPair(x, y):
    n = x * y
    m = (x - 1) * (y - 1)
    e = 65537
    d = pow(e, -1, m)
    openk = (n, e)
    secretk = (d, n)
    return openk, secretk

def encrypt(text, okey):
    encrypted = pow(text, okey[1], okey[0])
    return encrypted

def decrypt(text, skey):
    decrypted = pow(text, skey[0], skey[1])
    return decrypted

def hash_message(message):
    message_hash = hashlib.sha256(str(message).encode()).hexdigest()
    return int(message_hash, 16)

def sign(message, skey):
    message_hash = hash_message(message)
    signature = decrypt(message_hash, skey)
    return signature

def verify(signature, message, okey):
    decrypted_hash = encrypt(signature, okey)
    message_hash = hash_message(message)
    return decrypted_hash == message_hash


test_results = []
for i in range(1):
    ap, aq, bp, bq = keyGen()
    aopen, asec = genKeyPair(ap, aq)
    bopen, bsec = genKeyPair(bp, bq)

    msga = random.randint(1, aopen[0] - 1)

    signature = sign(msga, asec)
    print(signature)
    print(msga)
    print(aopen)
    verification_result = verify(signature, msga, aopen)

    print("Test case:", i)
    print("Aopen, Asec:", aopen,asec)
    print("Bopen, Bsec:", bopen,bsec)
    print("msa:", msga)
    print("signature:", signature)
    print("verification:", verify(signature, msga, aopen))
    print("------------------------------------------------------------------------------")



import requests

def get_server_public_key(key_size):
    url = f"http://asymcryptwebservice.appspot.com/rsa/serverKey?keySize={key_size}"
    response = requests.get(url)
    if response.status_code == 200:
        key_data = response.json()
        modulus = int(key_data["modulus"], 16)
        public_exponent = int(key_data["publicExponent"], 16)
        return (modulus, public_exponent)
    else:
        raise Exception("Failed to get public key from server")

# API to verify signature with server
def verify_signature_with_server(modulus_hex, public_exponent_hex, message_hex, signature_hex):
    url = "http://asymcryptwebservice.appspot.com/rsa/verify"
    params = {
        "modulus": modulus_hex,
        "publicExponent": public_exponent_hex,
        "message": message_hex,
        "signature": signature_hex,
        "type": "BYTES"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["verified"]
    else:
        print("Server Response Code:", response.status_code)
        print("Server Response Content:", response.content)
        raise Exception("Failed to verify signature with server")


def confidential_key_exchange(sender_open_key, sender_secret_key, receiver_open_key, secret_value):
    k = secret_value


    k1 = encrypt(k, receiver_open_key)
    S = decrypt(k, sender_secret_key)
    S1 = encrypt(S, receiver_open_key)



    message = (k1, S1)
    return message


ap, aq, bp, bq = keyGen()
local_public_key, local_private_key = genKeyPair(ap, aq)

server_public_key = get_server_public_key(256)

new_modulus = 92141270580744000810977490017493106605452358113833347418360012790615092846163
new_public_exponent = server_public_key[1]


server_public_key_custom = (new_modulus, new_public_exponent)


secret_value = random.randint(1, 1000)


encrypted_message = encrypt(secret_value, server_public_key_custom)
signature = sign(secret_value, local_private_key)
print(local_public_key, local_private_key)
print(server_public_key_custom)
print(secret_value)
print(hex(encrypted_message))

a,b = server_public_key_custom

a_hex = hex(a)[2:].lower()
b_hex = hex(b)[2:].lower()
hex_message = hex(encrypted_message)[2:].lower()
hex_signature = hex(signature)[2:].lower()


print("Modulus:", a_hex)
print("Public Exponent:", b_hex)
print("Message:", hex_message)
print("Signature:", hex_signature)


verification_result = verify_signature_with_server(a, b, hex_message, hex_signature)


response = requests.get(url, params=params)
if response.status_code == 200:
    try:
        verification_result = verify_signature_with_server(a_hex, b_hex, hex_message_hash, hex_signature)
        print("Verification Result:", verification_result)
    except Exception as e:
        print(e)


else:
    print("Server Response Code:", response.status_code)
    print("Server Response Content:", response.content)
    raise Exception("Failed to verify signature with server")




