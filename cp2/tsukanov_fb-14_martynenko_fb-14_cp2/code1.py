def calculate_index_of_coincidence(text, r):
    blocks = [text[i::r] for i in range(r)]
    #print(blocks)
    ic_values = []

    for block in blocks:
        frequencies = {}

        for char in block:
            if char in frequencies:
                frequencies[char] += 1
            else:
                frequencies[char] = 1

        ic_value = sum([(count * (count - 1)) for count in frequencies.values()]) / (len(block) * (len(block) - 1))
        ic_values.append(ic_value)

    return sum(ic_values) / r
with open("text_4var.txt", "r", encoding="utf-8") as f:
    text=f.read()

max_key_length = 40

for r in range(2, max_key_length+1):
    ic = calculate_index_of_coincidence(text, r)
    print(f"Для r={r}, індекс відповідності: {ic}")


r=13
blocks = [text[i::r] for i in range(r)]

def vigenere_decrypt(text, key):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    result = []
    key_length = len(key)
    key_indexes = [alphabet.index(letter) for letter in key]

    for i, char in enumerate(text):
        if char in alphabet:
            shift = key_indexes[i % key_length]
            index = (alphabet.index(char) - shift) % len(alphabet)
            result.append(alphabet[index])

    return ''.join(result)

letter = 'о'
alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

key=""
for block in blocks:
    character_count = {}
    for char in block:
        if char in character_count:
            character_count[char] += 1
        else:
            character_count[char] = 1

# Знаходимо символ, який найчастіше повторюється
    most_common_char = max(character_count.values())  
    for k, v in character_count.items():
            if v == most_common_char:
                most_common_char=k 
    y=alphabet.index(most_common_char)
    k = ''
    x = alphabet.index(letter)
    k = k + (alphabet[y-x])
    key+=k
print(key)
print(vigenere_decrypt(text, "громыковедьма")) #громнкавьдума
with open("decrypted_var4_text.txt", "w", encoding="utf-8") as f:
    f.write(vigenere_decrypt(text, "громыковедьма")) #громнкавьдума