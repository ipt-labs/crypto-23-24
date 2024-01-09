from random import randint


class RSA_SCHEMA:
    def __init__(self) -> None:
        # Init necessary properties
        self.math = Math()
        self.p = 0
        self.q = 0
        self.n = 0
        self.euler = 0
        self.e = 2**16 + 1
        self.d = 0

    def GenerateKeyPair(self):
        self.p = self.math.generate_random_prime()
        self.q = self.math.generate_random_prime()
        self.n = self.p * self.q
        self.euler = (self.p - 1) * (self.q - 1)
        self.d = pow(self.e, -1, self.euler)

    def getPublicKey(self) -> tuple:
        return (self.n, self.e)

    def getPrivateKey(self) -> tuple:
        return (self.d, self.p, self.q)


class Math:
    def __init__(self) -> None:
        self.first_20_primes = self.generate_small_primes(20)
        pass

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def is_prime(self, p, k) -> bool:
        for i in self.first_20_primes:
            if p % i == 0:
                return False

        if p <= 1 or p % 2 == 0:
            return False
        if p <= 3:
            return True

        # p - 1 = 2^s * d step 0
        s = 0
        d = p - 1
        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(k):
            x = randint(2, p - 1)  # 1 < x < p  #step 1
            gcd, *_ = self.extended_gcd(x, p)

            if gcd > 1:
                return False

            # step 2.1
            x_d = pow(x, d, p)
            if x_d == p - 1 or x_d == 1:
                continue

            # step 2.2
            x_r = x_d
            for _ in range(1, s):
                x_r = pow(x_r, 2, p)

                if x_r == p - 1:
                    break
            else:
                return False
        return True

    def generate_random_prime(self, size=256):
        while True:
            # set range of min and max values
            min_v = 1 << (size - 1)
            max_v = (1 << size) - 1
            numb = randint(min_v, max_v)

            if self.is_prime(numb, 25):
                return numb

    def generate_small_primes(self, count):
        primes = []
        num = 2

        while len(primes) < count:
            is_prime = True
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break

            if is_prime:
                primes.append(num)
            num += 1

        return primes


class Abonent:
    def __init__(self, name: str, rsa: RSA_SCHEMA) -> None:
        self.name = name
        self.rsa = rsa

    def setRsa(self, rsa: RSA_SCHEMA):
        self.rsa = rsa

    def checkRsaKey(self, rsa_b: RSA_SCHEMA) -> bool:
        return self.rsa.n < rsa_b.n

    def Encrypt(self, message, key):
        return pow(message, key[1], key[0])

    def Decrypt(self, encrypted):
        return pow(encrypted, self.rsa.d, self.rsa.n)

    def Sign(self, message):
        return message, pow(message, self.rsa.d, self.rsa.n)

    def Verify(self, message, sign, key):
        if message == pow(sign, key[1], key[0]):
            print("Sign is correct.\n")
        else:
            print("Sign is incorrect!.\n")

    def SendKey(self, k, key):
        _, S = self.Sign(k)
        S1 = self.Encrypt(S, key)
        k1 = self.Encrypt(k, key)

        print(f"Sent........\n" f"S1 = {S1}\n" f"k1 = {k1}" f"\nS = {S}\n")

        return k1, S1

    def ReceiveKey(self, k1, S1, key):
        k = self.Decrypt(k1)
        S = self.Decrypt(S1)

        print(f"Received.......\n" f"k = {k}\n" f"S = {S}")

        self.Verify(k, S, key)
        if k == self.Encrypt(S, key):
            print("You were Authenticated")
        else:
            print("Authentication failed")

    def printRSAInfo(self):
        print(
            f"\nUser: {self.name}\nPrivateKey:{self.rsa.getPrivateKey()}\nPublicKey:{self.rsa.getPublicKey()}\nq:{self.rsa.q}\np:{self.rsa.p}"
        )


userA = Abonent("UserA", RSA_SCHEMA())
userB = Abonent("UserB", RSA_SCHEMA())
keysAreValid = False

while not keysAreValid:
    userA.rsa.GenerateKeyPair()
    userB.rsa.GenerateKeyPair()
    keysAreValid = userA.checkRsaKey(userB.rsa)


# Print all info about generated keys

userA.printRSAInfo()
userB.printRSAInfo()

# Get random message, encrypt and decrypt

message = randint(1, 100000)
enctyptedMessage = userB.Encrypt(message, userA.rsa.getPublicKey())
decryptedMessage = userA.Decrypt(enctyptedMessage)
_, sign = userA.Sign(message)
print(
    f"\nOriginal message:{message}\nEncrypted by B:{enctyptedMessage}\nDecrypted by A:{decryptedMessage}\nSign:{sign}"
)

# Check if sign is correct
userB.Verify(message, sign, userA.rsa.getPublicKey())

# Test sending key
k = randint(1, userA.rsa.n - 1)
print(f"\nOriginal k = {k}")

k1, S1 = userA.SendKey(k, userB.rsa.getPublicKey())
userB.ReceiveKey(k1, S1, userA.rsa.getPublicKey())


# Test when it should fail
k = randint(1, userA.rsa.n - 1)
print(f"\nOriginal k = {k}")

k1, S1 = userA.SendKey(k, userB.rsa.getPublicKey())
userB.ReceiveKey(k1 + 2805, S1, userA.rsa.getPublicKey())
