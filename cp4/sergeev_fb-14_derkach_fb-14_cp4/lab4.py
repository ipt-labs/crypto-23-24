import random
die = random.SystemRandom()

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(e, phi):
    gcd, x, _ = egcd(e, phi)
    if gcd == 1:
        return x % phi

def miller_rabin_test(num, a):
  exp = num-1
  while not exp & 1:
    exp >>= 1
  if pow(a, exp, num) == 1:
    return True
  while exp < num -1:
    if pow(a, exp, num) == num - 1:
      return True
    exp <<= 1
  return False

def is_prime(num, k=200):
  for _ in range(k):
    a = die.randrange(2, num-1)
    if not miller_rabin_test(num, a):
      return False
  return True

def generate_prime_nums(bit_length=256):
  bit_length -= 1
  while True:
    a = ((die.randrange(1 << bit_length - 1, 1 << bit_length)) << 1)+1
    if is_prime(a):
      return a

def generate_key_pair(p, q):
  n = p * q
  phi = (p-1)*(q-1)
  e = 65537
  d = mod_inverse(e, phi)
  return (e, d, n, phi)

def encrypt(m, key, n):
  return pow(m, key, n)

def decrypt(c, key, n):
  return pow(c, key, n)

def verify(nonce, priv_key, n):
  return decrypt(nonce, priv_key, n)

def sign(nonce, pub_key, n):
  return encrypt(nonce, pub_key, n)

def send_key(nonce, key, n, sender, receiver):
  print(f'sent nonce {nonce} from {sender} to {receiver}')
  return sign(nonce, key, n)

def rcv_key(nonce, key, n, sender, receiver):
  print(f'received nonce {nonce} from {sender} to {receiver}')
  return verify(nonce, key, n)

def main():
  p, q, p1, q1 = ( generate_prime_nums() for _ in range(4) )
  e, d, n, phi = generate_key_pair(p, q)
  pub, priv, n1, phi1 = generate_key_pair(p1, q1)
  print(f'\nAlice {e=}\n{d=}\n{n=}\n{p=}\n{q=}\n{phi=}')
  print(f'\nBob {pub=}\n{priv=}\n{n1=}\n{p1=}\n{q1=}\n{phi1=}\n')
  c = encrypt(73253297, pub, n1)
  nonce = die.randrange(99999999999999)
  print(f'{nonce=}')
  # client sends server his public key, server sends nonce (d is not sent over the network, it is for simplisity sake)
  signed_msg = send_key(nonce, d, n, 'Bob', 'Alice')
  # client sends back signed msg if nonce is decrypted successfully - connection established
  rcved_key = rcv_key(signed_msg, e, n, 'Alice', 'Bob')
  print(rcved_key, nonce)
  if rcved_key == nonce:
    print('[*] Client is verified!')
  else:
    raise Exception('Client is unverified')
  # the same process to verify server identity
  nonce2 = die.randrange(99999999999999)
  print(f'{nonce2=}')
  signed_msg = send_key(nonce2, priv, n1, 'Alice', 'Bob')
  rcved_key2 = rcv_key(signed_msg, pub, n1, 'Bob', 'Alice')
  if rcved_key2 == nonce2:
    print('[*] Server is verified!')
    print('[*] Connection established successfully!')
  else:
      raise Exception('Server is unverified')

if __name__ == '__main__':
  main()
