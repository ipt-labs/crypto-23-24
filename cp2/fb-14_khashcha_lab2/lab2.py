import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
from collections import Counter
from re import sub

def clean_text(input_text):
    lower_text = input_text.lower()
    cleaned_text = sub("[^а-я]", " ", lower_text)
    cleaned_text = sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text.replace("ъ", "ь").replace("ё", "е")

def cipher_shift(s, k):
    result = []
    for i in range(len(s)):
        if s[i] in cipher:
            shift = (cipher.index(s[i]) + cipher.index(k[i % len(k)])) % len(cipher)
            result.append(cipher[shift])
        else:
            result.append(s[i])
    return ''.join(result)


def freq_analysis(s):
    letters_count = Counter(s)
    text_len = len(s)
    index = sum(count * (count - 1) for count in letters_count.values()) / (text_len * (text_len - 1))
    return index

def segment_text(s, segment_size):
    return [s[i::segment_size] for i in range(segment_size)]

def calculate_mean_index(s):
    mean_indices = {}
    for seg_size in range(2, 31):
        segments = segment_text(s, seg_size)
        mean_indices[seg_size] = np.mean([freq_analysis(segment) for segment in segments])
    return mean_indices

def identify_key(s, seg_size):
    segments = segment_text(s, seg_size)
    common_chars = 'оеаитнсрлвкпмдзяугьбыйчюжхшщцэф'
    for char in common_chars:
        potential_key = []
        for segment in segments:
            most_common = max(Counter(segment), key=Counter(segment).get)
            shift = (cipher.index(most_common) - cipher.index(char)) % len(cipher)
            potential_key.append(cipher[shift])
        print(''.join(potential_key))

def decode_text(input_text, key_sequence):
    decoded_chars = []
    for position, char in enumerate(input_text):
        if char in cipher:
            adjusted_index = (cipher.index(char) - cipher.index(key_sequence[position % len(key_sequence)])) % len(cipher)
            decoded_chars.append(cipher[adjusted_index])
        else:
            decoded_chars.append(char)
    return ''.join(decoded_chars)

def create_plot(lengths, indices, output_file):
    data_frame = pd.DataFrame({'Block_Length': lengths, 'Compliance_Index': indices})
    data_frame.to_csv(output_file, index=False)
    plt.figure(figsize=(12, 6))
    plt.bar(x=data_frame['Block_Length'], height=data_frame['Compliance_Index'], color='mediumvioletred')
    plt.xlabel('Text Blocks')
    plt.ylabel('Index Values')
    plt.title('Compliance Index Across Different Blocks')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file.replace('.csv', '.png'))
    plt.show()


cipher = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

encryption_keys = {'k2': 'йо', 'k3': 'гой', 'k4': 'хата', 'k5': 'вуста', 'k10': 'интеграция', 'k15': 'березеньтравень', 'k20': 'перемогаперемогабуде'}

with open('text_to_encrypt.txt', 'r', encoding='utf-8') as file:
    original_text = file.read()
    clean_text(original_text)

key_list = ['original']
index_list = [freq_analysis(original_text)]

for key_name, key_value in encryption_keys.items():
    ciphered_text = cipher_shift(original_text, key_value)
    with open(f'ciphered_{key_name}.txt', 'w', encoding='utf-8') as file:
        file.write(ciphered_text)

    key_list.append(key_name)
    index_list.append(freq_analysis(ciphered_text))

create_plot(key_list, index_list, 'freq_analysis.csv')

with open('text_to_decrypt.txt', 'r', encoding='utf-8') as file:
    text_to_uncipher = file.read()

block_count = calculate_mean_index(text_to_uncipher)
create_plot(list(block_count.keys()), list(block_count.values()), 'block_freq_analysis.csv')
identify_key(text_to_uncipher, 15)

decryption_key = 'арудазовархимаг'
decrypted_result = decode_text(text_to_uncipher, decryption_key)
with open('decrypted_text.txt', 'w', encoding='utf-8') as file:
    file.write(decrypted_result)
