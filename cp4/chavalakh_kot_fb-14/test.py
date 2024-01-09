from main import Encrypt_text, Decrypt_text, hex_to_decimal, decimal_to_hex, GenerateKeyPair, Verify_text, Sign_text, SendKey, ReceiveKey

print("Tests:")

Public_key_Server = hex_to_decimal('9243D6935568B1235E32E79F38B4F525'), hex_to_decimal('10001')
message = 'Kot1337'
print(f"Encrypted by us: {decimal_to_hex(Encrypt_text(message, Public_key_Server))}")
print('Encrypted by site: 159BD70FAED20CF710DF3A807EA4843A')

p = 160974941335832298448894538799832754593
q = 219940465870775757011659172596898530451
print(f'p = {p}')
print(f'q = {q}')
Public_key, Private_key = GenerateKeyPair(p, q)
print(f'Шифруємо на сервері з нашим Public Key: {decimal_to_hex(Public_key[0]), decimal_to_hex(Public_key[1])}')


encrypted_by_server_message = '2CF14C680D79F3B268C82F13562C1E9ACF94D2C017858911AE99C4439D5A5195'
print(f'Розшифровуємо локально: {Decrypt_text(hex_to_decimal(encrypted_by_server_message), Private_key)}')


signed_by_server = (message, hex_to_decimal('4172B95B8B26239FCA0049D133B9FFDA'))
if Verify_text(signed_by_server, Public_key_Server):
    print('Verified\n')
else:
    print('Not verified\n')
    
signed_by_us = Sign_text(message, Private_key)
print(f'Signed by us: {decimal_to_hex(signed_by_us[1])}')
