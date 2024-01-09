from  random import randint
#Задамо змінні корситувачів через словники
A = B ={
    'p':0,
    'q':0,
    'n':0,
    'euler':65537,
    'e':0,
    'd':0
}

#Ініціалізуємо розширений алгоритм Евкліда
def Euclid_extended(a, b):
    if b == 0:
        return (a, 1, 0)
    gcd, x, y = Euclid_extended(b, a % b)
    return (gcd, y, x - (a // b) * y)

#Ініціалізація функції тесту Міллера-Рабіна 
def Miller_check(n, k):
    if n <= 1 or (n % 2 == 0 and n > 2):
        return False

    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = randint(2, n - 2)
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

#Ініціалізуємо функцію
def generate_prime_numbers(num_primes, lower, upper=None):
    ks = [3, 5, 7]
    primes = []

    for _ in range(num_primes):
        while True:
            if upper:
                candidate = randint(lower, upper)
            else:
                candidate = randint(10**(lower-1), 10**lower - 1)
            
            if all(Miller_check(candidate, k) for k in ks):
                primes.append(candidate)
                break

    with open('numbers.txt', 'a', encoding='utf-8') as file:
        for prime in primes:
            file.write(f"{prime}\n")

    return primes

#generate_prime_numbers(10, 256)


#Почнемо реалізацію функцій RSA
def PrimeGenerator(num_digits):
    primes = generate_prime_numbers(1, num_digits)
    return primes[0]  # Return the first (and only) prime in the list


#Функція генерації ключів
def GenerateKeyPair(dictionary):
    dictionary['p'] = PrimeGenerator(256)
    dictionary['q'] = PrimeGenerator(256)
    dictionary['n'] = dictionary['p'] * dictionary['q']
    dictionary['euler'] = (dictionary['p'] - 1) * (dictionary['q'] - 1)

    gcd, _, _ = Euclid_extended(dictionary['euler'], 65537)
    if gcd != 1:
        raise ValueError("e is not coprime with euler")

    dictionary['d'] = pow(65537, -1, dictionary['euler'])
    
    public_key = (dictionary['n'], 65537)
    private_key = (dictionary['d'], dictionary['p'], dictionary['q'])
    return public_key, private_key


#Функція шифрування 
def Encrypt(message, public_key):
    n, e = public_key
    return pow(message, e, n)

#Функція де-шифрування
def Decrypt(encrypted, private_key):
    d, p, q = private_key
    n = p * q
    return pow(encrypted, d, n)

#Функція підпису
def Sign(message, private_key):
    d, p, q = private_key
    n = p * q
    signature = pow(message, d, n)
    return message, signature

#Функція підтвердження підпису
def Verify(message, signature, public_key):
    n, e = public_key
    if message == pow(signature, e, n):
        print('Підпис підтверджено.\n')
    else:
        print('Підпис не підтверджено.\n')

#Функція отримання ключа
def SendKey(k, sender_private_key, receiver_public_key):
    _, signature = Sign(k, sender_private_key)
    encrypted_signature = Encrypt(signature, receiver_public_key)
    encrypted_key = Encrypt(k, receiver_public_key)

    print(f'Підпис = {signature}\n'
          f'Зашифрований підпис = {encrypted_signature}\n'
          f'Зашифрований ключ = {encrypted_key}')

    return encrypted_key, encrypted_signature


def ReceiveKey(encrypted_key, encrypted_signature, receiver_private_key, sender_public_key):
    decrypted_key = Decrypt(encrypted_key, receiver_private_key)
    decrypted_signature = Decrypt(encrypted_signature, receiver_private_key)

    print(f'Розшифрований ключ = {decrypted_key}\n'
          f'Розшифрований підпис = {decrypted_signature}')

    Verify(decrypted_key, decrypted_signature, sender_public_key)
    
#Перейдемо до фінальної частини - реалізації протоколу RSA на основі написаних функція
# public_key_A, private_key_A = GenerateKeyPair(A)
# public_key_B, private_key_B = GenerateKeyPair(B)


# print(f'Користувач А\n'
#         f'p = {A["p"]}\n'
#         f'q = {A["q"]}\n'
#         f'Public key: {public_key_A}\n'
#         f'Private key: {private_key_A[0]}\n')

# print(f'Користувач B\n'
#         f'q = {B["q"]}\n'
#         f'p = {B["p"]}\n'
#         f'Public Key: {public_key_B}\n'
#         f'PrivateKey: {private_key_B[0]}\n')

# message = randint(0, A['n'] - 1)
# encr_msg = Encrypt(message, public_key_A)
# decr_msg = Decrypt(encr_msg, private_key_A)
# _, sign = Sign(message, private_key_A)
# print(f'Повідомлення: {message}\n\n'
#         f'Зашифроване повідомлення за допомогою відкритого ключа А: {encr_msg}\n\n'
#         f'Розшифроване повідомлення за допомогою секретного ключа А: {decr_msg}\n\n'
#         f'Повідомлення з цифровим підписом: {(message, sign)}\n')

# Verify(message, sign, public_key_A)

# k = randint(1, A['n'] - 1)
# print(f'k = {k}')

# k1, S1 = SendKey(k, private_key_A, public_key_B)
# ReceiveKey(k1+10, S1, private_key_B, public_key_A)


#check_task

pubkey_serv = (int('B147F36F350E32B82562545E92A9D82F5C86A1F02F908C93CD928BAD171647B9', 16), int('10001', 16))
message = 'KittyKitty'

ciphertext_serv = (int('8D0207343313143C514681B7BCA9561458FCAE5CAB04B7777555FF8353C2D95E', 16))

def Encrypt(message, pubkey):
    # Конвертуємо повідомлення у числове представлення
    m_int = int.from_bytes(message.encode('utf-8'), 'big')
    # Шифруємо повідомлення використовуючи відкритий ключ
    c_int = pow(m_int, pubkey[1], pubkey[0])
    return c_int

ciphertext_our = Encrypt(message, pubkey_serv)

print(f"ciphertext encrypted by server: {ciphertext_serv}\nciphertext encrypted by us: {ciphertext_our}")

signed = (message, int("1ACFD7926878FC613A99166C69190373A008EE772BD6218EB3EC2C24B7642661", 16))

def Verify(signed, pubkey):
    # Розбиваємо підпис на повідомлення та цифровий підпис
    message, signature = signed
    # Конвертуємо повідомлення у числове представлення
    m_int = int.from_bytes(message.encode('utf-8'), 'big')
    # Верифікуємо цифровий підпис
    verified_signature = pow(signature, pubkey[1], pubkey[0])
    # Якщо числове представлення повідомлення відповідає верифікованому підпису, підпис дійсний
    return m_int == verified_signature

verified = Verify(signed, pubkey_serv)

print(verified)
