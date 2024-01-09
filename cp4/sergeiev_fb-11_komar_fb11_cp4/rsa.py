from random import randint


class RSA:
    def __init__(self):
        self.p = 0
        self.q = 0
        self.n = 0
        self.euler = 0
        self.e = 2**16 + 1
        self.d = 0

    # Завдання 1
    def ExtendedEuclidean(self, a, m):
        if m == 0:
            return a, 1, 0
        gcd_num, x, y = self.ExtendedEuclidean(m, a % m)
        x, y = y, x - (a // m) * y
        return gcd_num, x, y

    def IsPrime(self, p, k):
        if p <= 1 or p % 2 == 0:
            return False
        if p <= 3:
            return True
    
        # p - 1 = 2^s * d
        s = 0
        d = p - 1
        while d % 2 == 0:
            d //= 2
            s += 1
    
        for _ in range(k):
            x = randint(2, p - 1)
            gcd, *_ = self.ExtendedEuclidean(x, p)
    
            if gcd > 1:
                return False
    
            # x^d mod p = +-1
            x_d = pow(x, d, p)
            if x_d == p - 1 or x_d == 1:
                continue
    
            # x_r = x^(d*2^r) mod p   |   x_r = (x_r-1)^2 mod p
            x_r = x_d
            for _ in range(1, s):
                x_r = pow(x_r, 2, p)
    
                if x_r == p - 1:
                    break
            else:
                return False
        return True

    def GeneratePrime(self, length=256):
        while True:
            min_v = 1 << (length - 1)
            max_v = (1 << length) - 1
            numb = randint(min_v, max_v)

            with open('not_prime.txt', 'a', encoding='utf-8') as f:
                f.write(f'{numb}\n')

            if self.IsPrime(numb, 20):
                return numb

    # Завдання 2-3
    def GenerateKeyPair(self):
        self.p = self.GeneratePrime()
        self.q = self.GeneratePrime()
        self.n = self.p * self.q
        self.euler = (self.p - 1) * (self.q - 1)
        self.d = pow(self.e, -1, self.euler)
        public_key = (self.n, self.e)
        private_key = (self.d, self.p, self.q)
        return public_key, private_key
    
    # Завдання 4
    def Encrypt(self, message, key):
        return pow(message, key[1], key[0])
    
    def Decrypt(self, encrypted):
        return pow(encrypted, self.d, self.n)
     
    def Sign(self, message):
        return message, pow(message, self.d, self.n)
    
    def Verify(self, message, sign, key):
        if message == pow(sign, key[1], key[0]):
            print('Цифровий підпис підтверджено, повідомлення не спотворено.\n')
        else:
            print('Цифровий підпис не підтверджено.\n')

    # Завдвння 5
    def SendKey(self, k, key):
        _, S = self.Sign(k)
        S1 = self.Encrypt(S, key)
        k1 = self.Encrypt(k, key)

        print(f'S = {S}\n'
              f'S1 = {S1}\n'
              f'k1 = {k1}')

        return k1, S1
    
    def ReceiveKey(self, k1, S1, key):
        k = self.Decrypt(k1)
        S = self.Decrypt(S1)

        print(f'k = {k}\n'
              f'S = {S}')

        self.Verify(k, S, key)
        # if k == self.Encrypt(S, key):
        #     print('Автентифікація пройдена.')
        # else:
        #     print('Автентифікація не пройдена.')


if __name__ == '__main__':
    A, B = RSA(), RSA()    
    pub_a, pr_a = A.GenerateKeyPair()
    pub_b, pr_b = B.GenerateKeyPair()

    while A.n > B.n:
        pub_a, pr_a = A.GenerateKeyPair()
        pub_b, pr_b = B.GenerateKeyPair()

    print(f'Користувач А\n'
          f'----- p = {A.p}\n'
          f'----- q = {A.q}\n'
          f'----- публічний ключ: {A.n, A.e}\n'
          f'----- секретний ключ: {A.d}\n')

    print(f'Користувач B\n'
          f'----- p = {B.p}\n'
          f'----- q = {B.q}\n'
          f'----- публічний ключ: {B.n, B.e}\n'
          f'----- секретний ключ: {B.d}\n')

    message = randint(0, A.n - 1)
    encr_msg = B.Encrypt(message, pub_a)
    decr_msg = A.Decrypt(encr_msg)
    _, sign = A.Sign(message)

    print(f'Повідомлення: {message}\n\n'
          f'Зашифроване повідомлення за допомогою відкритого ключа А: {encr_msg}\n\n'
          f'Розшифроване повідомлення за допомогою секретного ключа А: {decr_msg}\n\n'
          f'Повідомлення з цифровим підписом: {(message, sign)}\n')

    B.Verify(message, sign, pub_a)

    k = randint(1, A.n - 1)
    print(f'k = {k}')

    k1, S1 = A.SendKey(k, pub_b)
    B.ReceiveKey(k1+10, S1, pub_a)
