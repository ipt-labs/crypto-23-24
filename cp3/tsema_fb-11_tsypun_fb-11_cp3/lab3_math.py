class InverseDoesNotExist(Exception):
    def __init__(self, expression: str, message: str) -> None:
        self.expression = expression
        self.message = message

    def __str__(self) -> str:
        return f"{self.message} ({self.expression})"


def ext_euclid(a: int, b: int) -> tuple:
    prev_r, r = a, b
    prev_u, u = 1, 0
    prev_v, v = 0, 1

    while r:
        q = prev_r // r
        prev_r, r = r, prev_r - q * r
        prev_u, u = u, prev_u - q * u
        prev_v, v = v, prev_v - q * v

    return prev_r, prev_u, prev_v


def get_modulo_inverse(a: int, mod: int):
    gcd, inverse, _ = ext_euclid(a, mod)

    if gcd == 1:
        return inverse % mod
    raise InverseDoesNotExist(f"{a}^-1 mod {mod}", "Inverse doesn't exist")
