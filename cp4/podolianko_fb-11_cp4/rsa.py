import utils
from typing import Tuple

type PublicKey = Tuple[int, int]  # e, n
type SecretKey = Tuple[int, int, int]  # d, p, q
type SignedMessage = Tuple[int, int]  # m, s
type Message = int
type Cyphertext = int
type Signature = int
type SignedMessage = Tuple[Message, Signature]
type ProtectedKey = Tuple[int, int]  # k1, S1


def GenerateKeyPair(bits: int = 256) -> Tuple[PublicKey, SecretKey]:
    # we will use a constant exponent2**16 + 1
    E = 65537

    # generate suitable p, q
    p = q = 0
    phi = 0
    while p == q or E >= phi:
        p, q = utils.get_prime(bits), utils.get_prime(bits)
        phi = (p - 1) * (q - 1)

    d = pow(E, -1, phi)
    n = p * q

    return (E, n), (d, p, q)


def Encrypt(message: Message, public_key: PublicKey) -> Cyphertext:
    if not 0 < message < public_key[1]:
        raise ValueError(f"message not in range [0, {public_key[1] - 1}]")

    return pow(message, public_key[0], public_key[1])


def Decrypt(cyphertext: Cyphertext, secret_key: SecretKey) -> Message:
    if not 0 < cyphertext < secret_key[1] * secret_key[2]:
        raise ValueError(f"cyphertext not in range [0, {secret_key[1] * secret_key[2] - 1}]")

    return pow(cyphertext, secret_key[0], secret_key[1] * secret_key[2])


def Sign(message: Message, secret_key: SecretKey) -> SignedMessage:
    if not 0 < message < secret_key[1] * secret_key[2]:
        raise ValueError(f"message not in range [0, {secret_key[1] * secret_key[2] - 1}]")

    s = pow(message, secret_key[0], secret_key[1] * secret_key[2])
    return message, s


def Verify(signed_message: SignedMessage, public_key: PublicKey) -> bool:
    return signed_message[0] == pow(signed_message[1], public_key[0], public_key[1])


def SendKey(session_key: int, sender_sk: SecretKey, rec_pk: PublicKey) -> ProtectedKey:
    n = sender_sk[1] * sender_sk[2]
    n1 = rec_pk[1]
    if n > n1:
        raise ValueError(f"sender's public key is not suitable for the protocol")

    if not 0 < session_key < n:
        raise ValueError(f"session key is not in range [0, {n}]")

    k1 = pow(session_key, rec_pk[0], n1)
    S = pow(session_key, sender_sk[0], n)
    S1 = pow(S, rec_pk[0], n1)

    return k1, S1


def ReceiveKey(protected_key: ProtectedKey, rec_sk: SecretKey, sender_pk: PublicKey) -> int:
    k = pow(protected_key[0], rec_sk[0], rec_sk[1] * rec_sk[2])
    S = pow(protected_key[1], rec_sk[0], rec_sk[1] * rec_sk[2])

    if k != pow(S, sender_pk[0], sender_pk[1]):
        raise ValueError(f"key signature verification failed")

    return k
