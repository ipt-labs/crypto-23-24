from collections import Counter
import re
import matplotlib.pyplot as plt

def vigenere_encrypt(text, key):
    alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    result = []
    key_length = len(key)
    key_indexes = [alphabet.index(letter) for letter in key]

    for i, char in enumerate(text):
        if char in alphabet:
            shift = key_indexes[i % key_length]
            index = (alphabet.index(char) + shift) % len(alphabet)
            result.append(alphabet[index])

    return ''.join(result)

def read_file(t):
    with open(t, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Function to delete spaces from a text file
def filter_text(t):
    # Remove all spaces
    t = read_file(t).lower()
    t = re.sub(r'[^\sабвгґдеєжзиіїйклмнопрстуфхцчшщьюя]', '', t)
    return re.sub(r'\s+', '', t)

def IOC(text):
    n = len(text)
    freqs = Counter(text)
    ioc = sum(freq * (freq - 1) for freq in freqs.values()) / (n * (n - 1))
    return ioc

def plot_IOC_histogram(iocs, labels):
    plt.bar(labels, iocs, color='purple')
    plt.xlabel('Ключ')
    plt.ylabel('Індекс відповідності')
    plt.title('Порівняння Індексів Відповідності')
    plt.show()


def guess_vigenere_key_length(ciphertext, max_key_length):
    ciphertext = ciphertext.lower()

    # Ініціалізуємо словник для зберігання індексів відповідності для кожної довжини ключа
    key_length_ic = {}

    # Пробуємо різні довжини ключа (2, 3, ...)
    for key_length in range(2, max_key_length + 1):
        # Розділяємо шифртекст на блоки довжиною key_length
        blocks = [ciphertext[i::key_length] for i in range(key_length)]

        # Обчислюємо індекс відповідності для кожного блоку
        block_ics = [IOC(block) for block in blocks]

        # Обчислюємо середній індекс відповідності для цієї довжини ключа
        avg_ic = sum(block_ics) / len(block_ics)

        # Зберігаємо індекс відповідності для даної довжини ключа
        key_length_ic[key_length] = avg_ic

    return key_length_ic

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

# Press the green but"ton in the gutter to run the script.
if __name__ == '__main__':
    case = input('1 - Зашифрувати текст\n'
                 '2 - Вгадати довжину\n'
                 '3 - Вгадати ключ\n'
                 '4 - Розшифрувати своїм ключем\n'
                 'Введіть число: ')
    if case == '1':

        input_text = filter_text('source.txt')

        # Ключі різної довжини
        keys = ["ор", "сон", "пари", "відіо", "слованегоробці"]

        # Шифруємо текст з використанням кожного ключа
        for key in keys:
            encrypted_text = vigenere_encrypt(input_text, key)
            with open(f'encrypted_{len(key)}_key.txt', 'w', encoding='utf-8') as file:
                file.write(encrypted_text)

        # Розрахунок IOC для відкритого тексту
        open_text_IOC = IOC(input_text)
        print(f"IOC for Open Text: {open_text_IOC}")

        iocs = [open_text_IOC]
        labels = ['OT']

        for key in keys:
            with open(f'encrypted_{len(key)}_key.txt', 'r', encoding='utf-8') as file:
                encrypted_text = file.read()
            # Розрахунок IOC для кожного шифротексту
            ioc = IOC(encrypted_text)

            iocs.append(ioc)
            labels.append(f"{len(key)}-key")

            print(f"IOC for {len(key)}-key ciphertext: {ioc}")

        plot_IOC_histogram(iocs, labels)

    if case == '2':

        text = read_file('encrypted_var_5.txt')

        max_key_length = 32  # Максимальна можлива довжина ключа
        key_length_ioc = guess_vigenere_key_length(text, max_key_length)

        # Виводимо індекс відповідності для кожної довжини ключа
        for key_length, ioc in key_length_ioc.items():
            print(f"Довжина ключа {key_length}: Індекс відповідності = {ioc}")

        # Побудова гістограми
        plt.bar(key_length_ioc.keys(), key_length_ioc.values())
        plt.xlabel("Довжина ключа")
        plt.ylabel("Індекс відповідності")
        plt.title("Гістограма індексів відповідності")
        plt.show()

    if case == '3':
        r = int(input("Введіть довжину ключа: "))
        text = read_file('encrypted_var_5.txt')
        blocks = [text[i::r] for i in range(r)]

        letter = 'о'
        alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

        k = ''
        for block in blocks:
            y = alphabet.index(Counter(block).most_common()[0][0])
            x = alphabet.index(letter)
            k = k + (alphabet[y-x])
        print(k)
        print(vigenere_decrypt(text, k))

    if case == '4':
        k = input("Введіть ключ: ")
        text = read_file('encrypted_var_5.txt')
        print(vigenere_decrypt(text, k))

