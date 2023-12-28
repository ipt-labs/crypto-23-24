import random
import main


#############################
# 5 task


# створення списку символів
letters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + list(range(10))
# print(letters)


# генератор повідомлень
def get_message(length):
    message = ''
    for _ in range(length):
        message += str(random.choice(letters))

    return message


# print(get_message(10))


# ініціалізуємо двох абонентів
user_A = main.user_A
user_B = main.user_B


# симуляція переписки


# "розпакуємо" ключі користувачів для зручності
public_key_A, private_key_A = user_A
public_key_B, private_key_B = user_B


# процес відправки повідомлення абонентом А абоненту В

# абонент А створює повідомлення
message_A = get_message(100)

print(f"Відкрите повідомлення А    : {message_A}")

# абонент А шифрує його за допомогою відкритого ключа
enc_message_A = main.encrypt(message_A, public_key_B)

# абонент B отримує повідомлення та розшифровує його
dec_message_A = main.decrypt(enc_message_A, private_key_B)

print(f"Розшифроване повідомлення А: {dec_message_A}")

print()


# процес відправки повідомлення абонентом B абоненту A

# абонент B створює повідомлення
message_B = get_message(100)

print(f"Відкрите повідомлення B    : {message_B}")

# абонент B шифрує його за допомогою відкритого ключа
enc_message_B = main.encrypt(message_B, public_key_A)

# абонент A отримує повідомлення та розшифровує його
dec_message_B = main.decrypt(enc_message_B, private_key_A)

print(f"Розшифроване повідомлення B: {dec_message_B}")

print()


# створення підпису

# для А

signature_A = main.create_signature(message_A, private_key_A)
print("Підпис від A:", signature_A)

verified_A = main.verify_signature(signature_A, public_key_A, message_A)
print("Перевірка підпису A:", verified_A)

print()

# для B

signature_B = main.create_signature(message_B, private_key_B)
print("Підпис від B:", signature_B)

verified_B = main.verify_signature(signature_B, public_key_B, message_B)
print("Перевірка підпису B:", verified_B)



