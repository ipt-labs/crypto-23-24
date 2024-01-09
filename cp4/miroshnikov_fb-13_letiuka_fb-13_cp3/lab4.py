import random
class RSA():
    def __init__(self, name : str):
        self.name = name
        self.p = None
        self.q = None
        self.d = None
        self.e = 2**16 + 1
        self.n = None
        self.k = None

    def generate_key(self):
        self.p, self.q = gen_keys()
        self.n = self.p * self.q
        fn = (self.p-1)*(self.q-1)
        self.d = pow(self.e, -1, fn)

        
def to_hex(n:int):
    return hex(n)[2:].upper()
def to_decimal(hex):
    return int(hex, 16)
def decimal_to_binary(n):
    binary = bin(n)[2:]
    return binary
def horner_scheme(x, power, module):
    binary_representation = decimal_to_binary(power)
    result = 1
    for i in binary_representation:
        result = (result * result) % module
        if i == '1':
            result = (result * x) % module
    return result
def division(n):
    for i in range(2,50):
        if n % i == 0:
            return False
    return True
def test_miller_rabin(n, k):
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    
    r, d = 0, n - 1

    while d % 2 == 0:
        r += 1
        d //= 2
    
    for _ in range(k):
        a = random.randint(2, n-1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_number():
    while True:
        number = random.getrandbits(256)
        if division(number):
            if test_miller_rabin(number, 15):
                return number
            else:
                print(f'Не пройшло - {number}')
        else: print(f'Не пройшло - {number}')

def generate_msg(n):
    M = random.randint(0, n-1)
    return M

def gen_keys():
    p = generate_number()
    q = generate_number()
    return p, q

def Encrypt(M, received):
    return pow(M, received.e, received.n)

def Decrypt(C, received):
    return pow(C, received.d, received.n)

def send_msg(received):
    M = generate_msg(received.n)
    print(f"Повідомлення - {(to_hex(M))}")
    encrypt_msg = Encrypt(M, received)
    print(f'Зашифроване повідомлення - {(to_hex(encrypt_msg))}')
    decrypt_msg = Decrypt(encrypt_msg, received)
    print(f'Розшифроване повідомлення - {to_hex(decrypt_msg)}')

def sign(sender, M):
    signature = pow(M, sender.d, sender.n)
    return [M, signature]

def verify(M, sign, sender):
    if M == pow(sign, sender.e, sender.n):
        return True
    return False

def send_key(user1, user2):
    while user1.n > user2.n:
        user1.generate_key()
    if not user1.k:
        user1.k = random.randint(1, user1.n)
    k1 = Encrypt(user1.k, user2)
    S = sign(user1, user1.k)[1]
    print(f'k - {to_hex(user1.k)}\nS - {to_hex(S)}')
    S1 = Encrypt(S, user2)
    return [k1, S1]

def receive_key(user1, user2, signed):
    k1, S1 = signed
    k = Decrypt(k1, user2)
    S = Decrypt(S1, user2)
    return verify(k, S, user1)




def main():
    temp = True
    msg = None
    encrypt = None
    crypt_user = None
    users = []

    while temp:
        print('1. Створити нового користувача з парою p,q')
        print('2. Переглянути інформацію')
        print('3. Надіслати повідомлення')
        print('3.1 Зашифрувати')
        print('3.2 Розшифрувати')
        print('4. Цифровий підпис')
        print('5. Конфіденційне розсилання ключів')
        action = input('Оберіть команду:')
        if action == '1':
            name = input("Введіть ім'я:")
            user = RSA(name=name)
            user.generate_key()
            users.append(user)
        elif action == '2':
            for u in users:
                print(f'Коритсувач:{u.name}\nВідкритий ключ:(n = {to_hex(u.n)}, e = {to_hex(u.e)})\nЗакритий ключ:(p - {to_hex(u.p)}, q - {to_hex(u.q)}, d - {to_hex(u.d)})')
        elif action == '3':
            print('Хто отримує?')
            name = input("Ім'я користувача:")
            for u in users:
                if u.name == name:
                    received = u
            send_msg(received)
        elif action == '3.1':
            crypt_user = input("Введіть користувача:")
            for u in users:
                if u.name == crypt_user:
                    crypt_user = u
            msg = generate_msg(crypt_user.n)
            encrypt = Encrypt(msg, crypt_user)
            print(f'Повідомлення - {to_hex(msg)}\nЗашифроване повідомлення - {to_hex(encrypt)}')
        elif action == '3.2':
            encrypt1 = input("[Не обов'язково]\nВведіть зашифроване повідомлення(hex):")
            if encrypt1:
                crypt_user1 = input("Введіть того, кому надійшло повідомлення:")
                for u in users:
                    if u.name == crypt_user1:
                        crypt_user1 = u
                encrypt1 = to_decimal(encrypt1)
                decrypt = to_hex(Decrypt(encrypt1, crypt_user1))
            else: decrypt = to_hex(Decrypt(encrypt, crypt_user))
            print(f'Розшифроване повідомлення - {decrypt}')
        elif action == '4':
            print('Хто підписує?')
            name = input("Ім'я користувача:")
            for u in users:
                if u.name == name:
                    sender = u
            msg = generate_msg(u.n)
            M, signature = sign(sender, msg)
            print(f'Повідомлення - {to_hex(M)}\nПідпис - {to_hex(signature)}')
            if verify(M, signature, sender):
                print('Підпис успішно перевірено')
            else:
                print('Повідомлення спотворене')
        elif action == '5':
            name1 = input("Перший користувач:")
            for u in users:
                if u.name == name1:
                    a = u
            name2 = input("Другий користувач:")
            for u in users:
                if u.name == name2:
                    b = u
            temp = send_key(a,b)
            print(f"k1 - {to_hex(temp[0])}\nS1 - {to_hex(temp[1])}")
            if receive_key(a, b, temp):
                print('Секретний ключ підтверджено')
            else:
                print('Спробуйте ще раз...')
        else:
            temp = False       

if __name__ == '__main__':
    main()
