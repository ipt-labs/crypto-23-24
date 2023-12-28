from lab4 import *

p,q,p1,q1 = generate_prime_pairs()
public_key_A, private_key_A = generate_key_pair(p,q)
public_key_B, private_key_B = generate_key_pair(p1,q1)
print(f"Keys for A: \nPublic key\nn: {public_key_A[0]}\ne: {public_key_A[1]}")
print(f"Private key\np: {private_key_A[0]}\nq: {private_key_A[1]}\nd: {private_key_A[2]}\n")
print(f"Keys for B: \nPublic key\nn1: {public_key_B[0]}\ne1: {public_key_B[1]}")
print(f"Private key\np1: {private_key_B[0]}\nq1: {private_key_B[1]}\nd1: {private_key_B[2]}\n")

message_A = random.randint(1, public_key_A[0] - 1)
cipher_text_A = encrypt(message_A, public_key_A)
decrypted_message_A = decrypt(cipher_text_A, private_key_A)
print(f"Test for A:\nrand message: {message_A}\ncipher message: {cipher_text_A}\ndecrypted: {decrypted_message_A}")
assert decrypted_message_A == message_A, "Encryption and decryption for A failed"
print("Encryption and decryption for A passed")

signature_A = sign(message_A, private_key_A)
verified_A = verify(signature_A, message_A, public_key_A)
print(f"signature: {signature_A}\nverification: {verified_A}")
assert verified_A, "Signature verification for A failed"
print("Signature verification for A passed\n")

message_B = random.randint(1, public_key_B[0] - 1)
cipher_text_B = encrypt(message_B, public_key_B)
decrypted_message_B = decrypt(cipher_text_B, private_key_B)
print(f"Test for B:\nrand message: {message_B}\ncipher message: {cipher_text_B}\ndecrypted: {decrypted_message_B}")
assert decrypted_message_B == message_B, "Encryption and decryption for B failed"
print("Encryption and decryption for B passed")

signature_B = sign(message_B, private_key_B)
verified_B = verify(signature_B, message_B, public_key_B)
print(f"signature: {signature_B}\nverification: {verified_B}")
assert verified_B, "Signature verification for B failed"
print("Signature verification for B passed\n")

message = random.randint(1, public_key_A[0] - 1)
k1, S1 = send_key(private_key_A, public_key_B, message)
k, S = receive_key(public_key_A, private_key_B, k1, S1)
print(f"Key exchange:\nmessage: {message}\nk1: {k1}\nS1: {S1}\nk: {k}\nS: {S}")
print("Key exchange test passed\n")

message = encoding('hello')
k1, S1 = send_key(private_key_A, public_key_B, message)
k, S = receive_key(public_key_A, private_key_B, k1, S1)
print(f"Key exchange:\nmessage: {message}\nk1: {k1}\nS1: {S1}\nk: {decoding(k)}\nS: {S}")
print("Key exchange test passed")

