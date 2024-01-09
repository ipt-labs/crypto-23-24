import random

def is_prime(n, k=5):
    """Тест Міллера-Рабіна"""
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    r, s= 0, n - 1
    while s% 2 == 0:
        r += 1
        s//= 2

    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for i in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def prime_generate(length):
    while True:
        num = random.getrandbits(length)
        if is_prime(num):
            return num

def prime_generate_pairs(length=256):
    p = prime_generate(length)
    q = prime_generate(length)
    p1 = prime_generate(length)
    q1 = prime_generate(length)
    while p*q>p1*q1 or p==q or p1==q1:
            p = prime_generate(length)
            q = prime_generate(length)
            p1 = prime_generate(length)
            q1 = prime_generate(length)
    return p, q, p1, q1

def generate_key_pair(p,q):
    n = p*q
    phi = (p-1)*(q-1)
    e = 65537
    d = pow(e, -1, phi)
    public_key = (n, e)
    private_key = (p, q, d)
    return public_key, private_key

def encrypt(message, public_key):
    n, e = public_key
    encrypted_text = pow(message, e, n)
    return encrypted_text

def decrypt(encrypted_text, private_key):
    p, q, d = private_key
    original_text = pow(encrypted_text, d, p*q)
    return original_text

def sign(message, private_key):
    signature = decrypt(message, private_key)
    return signature

def verify(signature, message, public_key):
    decrypted_signature = encrypt(signature, public_key)
    return decrypted_signature == message

def send_key(A_private_key, B_public_key, message):
    key1 = encrypt(message, B_public_key)
    signat= sign(message, A_private_key)
    signat1 = encrypt(signat, B_public_key)
    return key1,signat1

def receive_key(A_public_key, B_private_key, key1, signat1):
    key = decrypt(key1, B_private_key)
    signat = decrypt(signat1, B_private_key)
    if not verify(signat, key, A_public_key):
        raise ValueError("Отриманий ключ невірний")
    return key,signat

def encode(text):
    return int.from_bytes(text.encode("utf-8"), "big")

def decode(integ):
    return integ.to_bytes((integ.bit_length()+7) // 8, "big").decode("utf-8")



p, q, p1, q1 = prime_generate_pairs()
A_public_key, A_private_key = generate_key_pair(p, q)
B_public_key, B_private_key = generate_key_pair(p1, q1)
print(f"Ключі для A: \nПублічний ключ\nn: {A_public_key[0]}\ne: {A_public_key[1]}")
print(f"Приватний ключ\np: {A_private_key[0]}\nq: {A_private_key[1]}\nd: {A_private_key[2]}\n")
print(f"Ключі для B: \nПублічний ключ\nn1: {B_public_key[0]}\ne1: {B_public_key[1]}")
print(f"Приватний ключ\np1: {B_private_key[0]}\nq1: {B_private_key[1]}\nd1: {B_private_key[2]}\n")

message_A = random.randint(1, A_public_key[0] - 1)
encrypted_text_A = encrypt(message_A, A_public_key)
decrypted_message_A = decrypt(encrypted_text_A, A_private_key)
print(f"Тест для A:\nвипадкове повідомлення: {message_A}\nшифроване повідомлення: {encrypted_text_A}\nрозшифроване: {decrypted_message_A}")
assert decrypted_message_A == message_A, "Шифрування та розшифрування для A не пройшли"
print("Шифрування та розшифрування для A пройшли успішно")

signature_A = sign(message_A, A_private_key)
verified_A = verify(signature_A, message_A, A_public_key)
print(f"підпис: {signature_A}\nперевірка: {verified_A}")
assert verified_A, "Перевірка підпису для A не пройшла"
print("Перевірка підпису для A пройшла успішно\n")

message_B = random.randint(1, B_public_key[0] - 1)
encrypted_text_B = encrypt(message_B, B_public_key)
decrypted_message_B = decrypt(encrypted_text_B, B_private_key)
print(f"Тест для B:\nвипадкове повідомлення: {message_B}\nшифроване повідомлення: {encrypted_text_B}\nрозшифроване: {decrypted_message_B}")
assert decrypted_message_B == message_B, "Шифрування та розшифрування для B не пройшли"
print("Шифрування та розшифрування для B пройшли успішно")

signature_B = sign(message_B, B_private_key)
verified_B = verify(signature_B, message_B, B_public_key)
print(f"підпис: {signature_B}\nперевірка: {verified_B}")
assert verified_B, "Перевірка підпису для B не пройшла"
print("Перевірка підпису для B пройшла успішно\n")

message = random.randint(1, A_public_key[0] - 1)
key1, signat1 = send_key(A_private_key, B_public_key, message)
key, signat= receive_key(A_public_key, B_private_key, key1, signat1)
print(f"Обмін ключами:\nпідпис: {message}\nключ1: {key1}\nпідпис1: {signat1}\nключ: {key}\nпідпис: {signat}")
print("Тест обміну ключами пройшов успішно\n")

message = encode("message")
key1, signat1 = send_key(A_private_key, B_public_key, message)
k, s= receive_key(A_public_key, B_private_key, key1, signat1)
print(f"Обмін ключами:\nпідпис: {message}\nключ1: {key1}\nпідпис1: {signat1}\nключ: {decode(k)}\nпідпис: {s}")
print("Тест обміну ключами пройшов успішно")


"""print(decode(decrypt(int(0xB5365BEA4E56AC2C7E96DA7C166B8796F3E1BBCB0ECCDC8A002A9977200C0D3DE22E1320264FA9637486D6ED741C209643A59156B5B99DE6F00B39A5BE5E5B), (4835022568567016675703666136244359194605652339567602571304767314189459746513, 27682111353061048507642170403125566640443418292324064649347027760001991019107, 33580891094834047191681774302930838134463348542406185695553162095654443989930029120861493813958941318625025268559238609723340356875562501347176779034081))))
print(hex(encrypt(encode("secret"), (int(0x8C497BAE6CC578B79F7C66C70B6C2E2C7A557D9BC2ACFDADB58E2D224BD821CF), 65537))))
print(verify(int(0x11C13D6C957F563CF389979496B8BA38A23072412881D47B9FB16A4826FB205F), encode("SomeText"), (int(0x8C497BAE6CC578B79F7C66C70B6C2E2C7A557D9BC2ACFDADB58E2D224BD821CF), 65537)))
print(hex(sign(encode("SomeText"), A_private_key)))"""