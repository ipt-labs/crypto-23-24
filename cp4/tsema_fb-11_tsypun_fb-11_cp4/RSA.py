from lab4_math import generatePrime, getModuloInverse, HornerPow


class RSA:
    def __init__(self, e: int, length: int, name: str) -> None:
        self.name = name
        self.e = e
        self.length = length
        self.n = None
        self._p = None
        self._q = None
        self._d = None


    def encrypt(self, m: int, pubKey: tuple[int, int]) -> int:
        return HornerPow(m, pubKey[1], pubKey[0])


    def decrypt(self, c: int) -> int:
        if self._d and self.n:
            return HornerPow(c, self._d, self.n)
        raise Exception("Need to generate a key")


    def generateKeyPair(self) -> None:
        self._p = generatePrime(self.length // 2 - 1)
        self._q = generatePrime(self.length // 2 - 1)

        phi = (self._p - 1) * (self._q - 1)
        self._d = getModuloInverse(self.e, phi)
        self.n = self._p * self._q


    def sign(self, m: int) -> tuple[int, int]:
        if self._d and self.n:
            return (m, HornerPow(m, self._d, self.n))
        raise Exception("Need to generate a key")


    def verify(self, signature: tuple[int, int], pubKey: tuple[int, int]) -> bool:
        m, s = signature
        return m == HornerPow(s, pubKey[1], pubKey[0])


    def getPubKey(self) -> tuple[int, int]:
        return self.n, self.e
