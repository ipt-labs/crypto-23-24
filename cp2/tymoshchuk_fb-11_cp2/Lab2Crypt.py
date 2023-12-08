import re
import random
import string
import openpyxl
import pandas as pd

# Define the alphabet, including "е" and excluding punctuation and capital letters
alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

def preprocess_text(text):
    # Заміна прописних літер на стрічні
    text = text.lower()

    # Вилучення всіх символів окрім текстових літер та пробілів
    text = re.sub(r'[^а-яё\s]', '', text)
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'ё', 'е', text)
    with open(f"text_edited.txt", 'w', encoding='utf-8') as file:
        file.write(text)
    return text

# Function to generate a random key of a given length
def generate_random_key(length):
    return ''.join(random.choice(alphabet) for _ in range(length))

# Function to encrypt plaintext with Vigenere cipher using a key
def vigenere_encrypt(plaintext, key):
    encrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char in alphabet:
            plaintext_idx = alphabet.index(char)
            key_char = key[i % key_length]
            key_idx = alphabet.index(key_char)
            encrypted_idx = (plaintext_idx + key_idx) % len(alphabet)
            encrypted_text += alphabet[encrypted_idx]
        else:
            encrypted_text += char
    return encrypted_text

# Function to decrypt ciphertext with Vigenere cipher using a key
def vigenere_decrypt(ciphertext, key):
    decrypted_text = ''
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char in alphabet:
            ciphertext_idx = alphabet.index(char)
            key_char = key[i % key_length]
            key_idx = alphabet.index(key_char)
            decrypted_idx = (ciphertext_idx - key_idx) % len(alphabet)
            decrypted_text += alphabet[decrypted_idx]
        else:
            decrypted_text += char
    return decrypted_text

# Function to calculate the matching index I_Y for a given text and alphabet
def calculate_IY(text, alphabet):
    n = len(text)
    if n <= 1:
        # Handle the case where the text length is zero or one
        return 0.0

    i_y_sum = 0
    for char in alphabet:
        n_i_y = text.count(char)
        i_y_sum += n_i_y * (n_i_y - 1)
    return i_y_sum / (n * (n - 1))

# Function to split text into blocks for I_Y calculation
def split_text_into_blocks(text, block_length):
    blocks = []
    for i in range(block_length):
        blocks.append(text[i::block_length])
    return blocks

# Function to find possible keys based on the most frequent letters
def find_possible_keys(text, key_length):
    frequent_letters = 'оеиантслвр'
    possible_keys = {}

    for frequent_letter in frequent_letters:
        block_list = split_text_into_blocks(text, key_length)
        key = ""
        for block in block_list:
            most_frequent_symbol = max(block, key=lambda symbol: block.count(symbol))
            key += alphabet[(alphabet.index(most_frequent_symbol) - alphabet.index(frequent_letter)) % len(alphabet)]
        possible_keys[frequent_letter] = key

    return possible_keys

# Function to calculate the average matching index for each key length
def key_length_indices(text):
    results = []
    for key_length in range(1, 31):
        key = generate_random_key(key_length)
        blocks_list = split_text_into_blocks(text, key_length)

        index_sum = 0
        for block in blocks_list:
            block_index = calculate_IY(block, alphabet)
            index_sum += block_index

        average_index = index_sum / len(blocks_list)
        print('Довжина ключа:', key_length, ' Значення ключа: ', key, ' Середнє значення індексу відповідності: ', round(average_index, 15))
        results.append({'Key Length': key_length, 'Key': key, 'Average I_Y': round(average_index, 15)})
    
    return results

# Calculate the average matching index for different key lengths and obtain the real key length from user input
def calculate_and_save_key_length_indices(encrypted_text):
    key_length_results = key_length_indices(encrypted_text)
    df_key_length = pd.DataFrame(key_length_results)
    df_key_length.to_excel("key_length_indices.xlsx", index=False)
    print("Key length indices calculated and saved to 'key_length_indices.xlsx'")

    real_key_length = int(input("Enter the real key length based on the experiment results: "))
    return real_key_length

# Find possible keys based on the most frequent letters and obtain the real key from user input
def find_possible_keys_based_on_frequent_letters(text, key_length):
    frequent_letters = 'оеиантслвр'
    possible_keys = find_possible_keys(text, key_length)

    for frequent_letter in frequent_letters:
        print(f"Most frequent letter: {frequent_letter}, Possible Key: {possible_keys[frequent_letter]}")

    real_key = input("Enter the real key based on the experiment results: ")
    return real_key

# Зчитуємо текст з файлу
with open('my_text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

plaintext = preprocess_text(text)

# Define the key lengths
key_lengths = [2, 3, 4, 5] + list(range(10, 21))

# Create a dictionary to store the results
results = {'Key Length': [], 'Key': [], 'I_Y (Encrypted)': [], 'I_Y (Plaintext)': []}

# Encrypt the plaintext with random keys, calculate I_Y for each, and also calculate I_Y for the plaintext
for key_length in key_lengths:
    key = generate_random_key(key_length)
    encrypted_text = vigenere_encrypt(plaintext, key)
    i_y_encrypted = calculate_IY(encrypted_text, alphabet)
    i_y_plaintext = calculate_IY(plaintext, alphabet)
    results['Key Length'].append(key_length)
    results['Key'].append(key)
    results['I_Y (Encrypted)'].append(i_y_encrypted)
    results['I_Y (Plaintext)'].append(i_y_plaintext)

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Save the results to an Excel file
df.to_excel("vigenere_matching_indices.xlsx", index=False)

print("Matching indices calculated and saved to 'vigenere_matching_indices.xlsx'")

# Load the encrypted text from task3.txt
with open("task.txt", "r", encoding="utf-8") as file:
    encrypted_text = file.read()

real_key_length = calculate_and_save_key_length_indices(encrypted_text)

real_key = find_possible_keys_based_on_frequent_letters(encrypted_text, real_key_length)

# Decrypt the text and save it to a file
decrypted_text = vigenere_decrypt(encrypted_text, real_key)
with open("decrypted_task.txt", "w", encoding="utf-8") as file:
    file.write(decrypted_text)

print("Decrypted text has been saved to 'decrypted_task.txt'.")
