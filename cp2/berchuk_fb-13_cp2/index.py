def calculate_index_of_coincidence(text):
    n = len(text)
    sum = 0
    for char in set(text):
        encoded_text_count = text.count(char)
        sum += (encoded_text_count * (encoded_text_count - 1))
    result = (1 / (n * (n - 1))) * sum
    return result

with open("9var.txt", "r", encoding="utf-8") as file:
    encrypted_text = file.read()

key_lengths = list(range(1, 31))
indexes = []

for key_length in key_lengths:
    substrings = [encrypted_text[i::key_length] for i in range(key_length)]
    total_index = 0
    for substring in substrings:
        total_index += calculate_index_of_coincidence(substring)
    average_index = total_index / key_length
    indexes.append(average_index)

for i, index in enumerate(indexes):
    print(f"Довжина ключа {i+1}: Індекс відповідності = {index:.6f}")