import random
import math


def horner_scheme(a, exp, modulo):
    bin_exp = bin(exp)[2:]
    result = 1
    for bit in bin_exp:
        result **= 2
        result %= modulo
        if bit == '1':
            result *= a
            result %= modulo
    return result


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)


def modular_inverse(a, m):
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        return None
    else:
        return (x % m + m) % m


# Проверка на простоту методом Миллера-Рабина
def is_prime_miller_rabin(n, k=20):  # при к = 20 ошибка составляет 1/4^20
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Выражаем n - 1 = 2^s * d (d - непарное)
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # k итераций теста Миллера-Рабина
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Генерируем случайное число заданной длины
def generate_prime_of_bit_length(bit_length):
    start_range = 2 ** (bit_length - 1)  # найменьшее возможное число заданной длины
    end_range = 2 ** bit_length - 1      # найбольшее возможное число заданной длины

    while True:
        candidate = random.randint(start_range, end_range)
        if is_prime_miller_rabin(candidate):
            return candidate


# Генерируем пары чисел (p, q)
def generate_prime_pair(bit_length):
    p = generate_prime_of_bit_length(bit_length)
    q = generate_prime_of_bit_length(bit_length)
    return p, q


# Проверка условия pq <= p1q1
def check(p, q, p1, q1):
    return p * q <= p1 * q1


# Генерируем публичные и секретные ключи для абонентов
def generate_key_pair(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    while True:
        e = random.randint(2, phi_n - 1)
        if math.gcd(e, phi_n) == 1:
            break
    d = modular_inverse(e, phi_n)
    public_key = (n, e)
    private_key = (n, d)
    return public_key, private_key


# Шифруем сообщение для абонента
def encrypt(message, public_key):
    n, e = public_key
    encrypted_message = horner_scheme(a=message, exp=e, modulo=n)
    return encrypted_message


# Расшифровываем сообщение для абонента
def decrypt(encrypted_message, private_key):
    n, d = private_key
    decrypted_message = horner_scheme(a=encrypted_message, exp=d, modulo=n)
    return decrypted_message


# Создаем цифровую подпись для абонента
def sign(message, private_key):
    n, d = private_key
    signature = horner_scheme(a=message, exp=d, modulo=n)
    return signature


# Проверяем цифровую подпись абонента
def verify(signature, message, public_key):
    n, e = public_key
    decrypted_signature = horner_scheme(a=signature, exp=e, modulo=n)
    original_message = decrypted_signature
    return original_message == message


def send_key(public_key_receiver, private_key_sender):
    message = random.randint(0, 2**(256 - 1))  # генерируем сообщение
    encrypted_message = encrypt(message, public_key_receiver)  # шифруем сообщение
    signature = sign(message, private_key_sender)  # подписываем сообщение
    signature_encrypted = encrypt(signature, public_key_receiver) # шифруем подпись
    return message, encrypted_message, signature_encrypted


def receive_key(encrypted_message, signature_encrypted, private_key_receiver, public_key_sender):
    decrypted_message = decrypt(encrypted_message, private_key_receiver)  # расшифровываем сообщение
    signature_decrypted = decrypt(signature_encrypted, private_key_receiver) # расшифровываем подпись
    verification_result = verify(signature_decrypted, decrypted_message, public_key_sender)  # проверяем подпись
    return decrypted_message, verification_result


# Пара простых чисел для абонентов А и B (доп. проверка: https://www.dcode.fr/primality-test)
p_A, q_A = generate_prime_pair(256)
p_B, q_B = generate_prime_pair(256)
while not check(p_A, q_A, p_B, q_B):
    p_A, q_A = generate_prime_pair(256)
    p_B, q_B = generate_prime_pair(256)
print("Абонент А:")
print("p_A =", p_A)
print("q_A =", q_A)
print("Абонент B:")
print("p_B =", p_B)
print("q_B =", q_B)

# number =
# bit_count = math.floor(math.log2(number)) + 1
# print(f"Бит в числе {number}: {bit_count}")

# Пара ключей для абонентов А и B
public_key_A, private_key_A = generate_key_pair(p_A, q_A)
public_key_B, private_key_B = generate_key_pair(p_B, q_B)
print("\nКлючи")
print("Открытый ключ А (n, e):", public_key_A)
print("Секретный ключ А (n, d):", private_key_A)
print("Открытый ключ B (n, e):", public_key_B)
print("Секретный ключ B (n, d):", private_key_B)

message_A, encrypted_message_A, signature_A = send_key(public_key_B, private_key_A)
decrypted_message_A, verification_result_A = receive_key(encrypted_message_A, signature_A, private_key_B, public_key_A)

print("\nАбонент A")
print("Сообщение:", message_A)
print("Зашифрованное сообщение:", encrypted_message_A)
print("Подпись:", signature_A)

print("\nАбонент B")
print("Расшифрованное сообщение:", decrypted_message_A)
print("Проверка цифровой подписи:", verification_result_A)


'''Старая версия'''
# # Шифруем и расшифровываем сообщение для абонента A
# message_A = random.randint(0, 2**(256 - 1))
# encrypted_message_A = encrypt(message_A, public_key_B)
# decrypted_message_A = decrypt(encrypted_message_A, private_key_B)
#
# # Абонент B проверяет подпись абонента A
# signature_A = sign(message_A, private_key_A)
# verification_result_A = verify(signature_A, message_A, public_key_A)
# print("\nАбонент A:")
# print("Сообщение:", message_A)
# print("Зашифрованное сообщение:", encrypted_message_A)
# print("Подпись:", signature_A)
# print("\nАбонент B:")
# print("Разшифрованное сообщение:", decrypted_message_A)
# print("Проверка цифровой подписи:", verification_result_A)



