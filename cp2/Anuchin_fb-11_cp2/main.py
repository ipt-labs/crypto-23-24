from collections import Counter
import matplotlib.pyplot as plt

# Constants
ALPHABET = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'



def clean_text(text: str) -> str:
    return ''.join([char for char in text.lower().replace('ё', 'е') if char in ALPHABET])


def index(text: str) -> float:
    """Calculates the index of coincidence for the text"""
    n = len(text)
    return sum(value * (value - 1) for value in Counter(text).values()) / (n * (n - 1))


def kroneker(a: str, b: str) -> int:
    return 1 if a == b else 0


def D(text: str, key_len: int) -> int:
    return sum(kroneker(text[i], text[i + key_len]) for i in range(len(text) - key_len))


def vegener_crypt(text: str, key: str, decrypt: bool = False) -> str:
    alphabet_len = len(ALPHABET)
    return ''.join(
        ALPHABET[(ALPHABET.index(char) + (-1 if decrypt else 1) * ALPHABET.index(key[i % len(key)])) % alphabet_len]
        for i, char in enumerate(text)
    )


def determine_possible_keys(ciphertext: str, r: int, assumed_plaintext_chars: set) -> list:
    return [
        ''.join(probable_key_char(Counter(ciphertext[i::r]).most_common(1)[0][0], assumed_char)
                for i in range(r))
        for assumed_char in assumed_plaintext_chars
    ]


def probable_key_char(ciphertext_char: str, assumed_plaintext_char: str) -> str:
    return ALPHABET[(ALPHABET.index(ciphertext_char) - ALPHABET.index(assumed_plaintext_char)) % len(ALPHABET)]


def main():
    with open('task1.TXT', 'r', encoding='utf-8') as f:
        original_text = clean_text(f.read())

    KEYS = ['да', 'нет', 'крик', 'пудра', 'шахматы', 'прикладной', 'молекулярный']
    encrypted_texts = [vegener_crypt(original_text, key) for key in KEYS]

    for key, etext in zip(KEYS, encrypted_texts):
        with open(f'encrypted_{key}.TXT', 'w', encoding='utf-8') as f:
            f.write(etext)

    indices = [index(original_text)] + [index(etext) for etext in encrypted_texts]

    with open('encrypted_task3.TXT', 'r', encoding='utf-8') as f:
        text_encrypted = clean_text(f.read())

    Ds = {i: D(text_encrypted, i) for i in range(2, 33)}
    r = 15
    assumed_chars = {'о', 'е', 'а', 'и'}
    possible_keys = determine_possible_keys(text_encrypted, r, assumed_chars)
    #possible_keys_12 = determine_possible_keys(text_encrypted, 15, assumed_chars)
    #possible_keys_24 = determine_possible_keys(text_encrypted, 30, assumed_chars)
    print(indices)
    print(Ds)
    # print(possible_keys_12)
    # print(possible_keys_24)
    print(possible_keys)

    key = 'крадущийсявтени'
    decrypted_result = vegener_crypt(text_encrypted, key, decrypt=True)
    with open('decrypted_result.TXT', 'w', encoding='utf-8') as f:
        f.write(decrypted_result)

    plot_indices(indices, KEYS)
    plot_Ds(Ds)


def plot_indices(indices, KEYS):
    plt.figure(figsize=(12, 6))
    key_lengths = [0] + [len(key) for key in KEYS]
    plt.bar(key_lengths, indices, color='skyblue')
    plt.xlabel('Key Length')
    plt.ylabel('Index of Coincidence')
    plt.title('Indices of Coincidence for Different Key Lengths')
    plt.xticks(key_lengths)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def plot_Ds(Ds):
    plt.figure(figsize=(12, 6))
    r_values, D_values = zip(*Ds.items())
    plt.plot(r_values, D_values, marker='o', color='coral', linestyle='-')
    plt.xlabel('r Value')
    plt.ylabel('D Value')
    plt.title('D Values for Different r')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
