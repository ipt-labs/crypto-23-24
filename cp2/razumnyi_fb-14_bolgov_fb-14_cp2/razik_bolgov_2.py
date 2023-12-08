import matplotlib.pyplot as plt

allowed_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'  # m = 32


def remove_spaces(text_to_filter):
    """ Remove spaces from the text 2-3kb to encode """

    return text_to_filter.replace(' ', '')


def vigenere(text, key_, mode='en'):
    """ Encrypt or Decrypt text by using Vigenere Cipher """

    global allowed_letters

    encrypted_text = ''
    key_size = len(key_)

    for i, j in enumerate(text):
        key_char = key_[i % key_size]
        b = allowed_letters.index(key_char)

        if mode == 'en':
            letter_ind = (allowed_letters.index(j) + b) % 32
        else:
            letter_ind = (allowed_letters.index(j) - b) % 32

        encrypted_char = allowed_letters[letter_ind]

        encrypted_text += encrypted_char

    return encrypted_text


def coincidence_index(text):
    """ Find coincidence index of text """

    global allowed_letters

    n = len(text)
    summ = 0
    for i in allowed_letters:
        N = text.count(i)
        summ += N * (N-1)
    I = summ / (n*(n-1))

    return I


def graph_coinc(indexes_):
    """ Show graphic of length and Coincidence Index """

    global keys
    r_values = [len(key) for key in keys]

    plt.plot(r_values, indexes_, marker='o', linestyle='-')
    plt.title('Coincidence index / r')
    plt.xlabel('r')
    plt.ylabel('I(Y)')
    plt.grid(True)
    plt.show()
    plt.close()


def block_division(text, size):
    """ Divide text in blocks of the specific range """

    blocks_list = []
    for i in range(size):
        block_str = ''

        for j in range(i, len(text), size):
            block_str += text[j]

        blocks_list.append(block_str)

    return blocks_list


def length_index(text):
    """ Find coincidence indexes of sizes 2-30 """

    d = {}
    for i in range(2, 31):

        block_list = block_division(text, i)

        coinc_block = 0
        for j in block_list:
            coinc_block += coincidence_index(j)

        coinc_block = coinc_block / len(block_list)
        print(f"r = {i} | {coinc_block}")
        d[i] = coinc_block

    plt.bar(d.keys(), d.values())
    plt.xlabel("r")
    plt.ylabel("Coincidence index")
    plt.show()

    print()


def find_key(text, size):
    """ Find possible key with known period """

    most_freq_letters = {'о': 14, 'а': 0, 'е': 5, 'и': 8, 'н': 13, 'т': 18}  # from lab 1 (indexes start from 0)
    block = block_division(text, size)

    for i in most_freq_letters:
        key = ''
        for j in block:
            block_freq_letter = letter_frequency(j)
            key += allowed_letters[((allowed_letters.index(block_freq_letter) - most_freq_letters[i]) % 32)]
        print(key)


def letter_frequency(text_to_freq):
    """ Count the frequencies of letters and return the most frequent one """

    global allowed_letters

    letter_freq_dict = {}

    for i in allowed_letters:
        letter_freq_dict[i] = text_to_freq.count(i)

    for i in letter_freq_dict:
        letter_freq_dict[i] = letter_freq_dict[i] / len(text_to_freq)

    d = {k: v for k, v in sorted(letter_freq_dict.items(), key=lambda item: item[1], reverse=True)}

    return list(d.keys())[0]


if __name__ == '__main__':

    # Open chosen text and remove spaces
    with open('text_lab2.txt', 'r', encoding='utf8') as f1:
        chosen_text = remove_spaces(f1.read())

    # Encode with different keys and output coincidence indexes
    #         2     3       4       5          10             13                 18                     20
    keys = ['ва', 'кпи', 'лабы', 'щакал', 'разикболго', 'патрикбейтман', 'зловещийпеньтайлер', 'поставьтевосемьбалов']

    print(f'Initial text: {chosen_text}')
    print(f'Initial coincidence index: {coincidence_index(chosen_text)}\n')

    indexes = []
    for i in keys:
        encoded = vigenere(chosen_text, i)
        print(f'Key: *{i}* with len of {len(i)}\nEncrypted text: {encoded}')
        coinc = coincidence_index(encoded)
        indexes.append(coinc)
        print(f'Coincidence index: {coinc}\n')

    print(f'Initial coincidence index: {coincidence_index(chosen_text)}')

    for i in range(len(keys)):
        print(f' r = {len(keys[i])}  | coincidence index: {indexes[i]}')
    print()

    # Build graph to show dependencies
    graph_coinc(indexes)

    #
    # Open encrypted text
    with open('text_to_decode_var1.txt', 'r', encoding='utf8') as f2:
        ecnr_text = f2.read()

    print(f'Coincidence index of the ecnrypted text: {coincidence_index(ecnr_text)}')

    # Output possible key length of 2-30 with coincidence indexes
    length_index(ecnr_text)

    # Based on found length find some possible keys
    find_key(ecnr_text, 12)

    # Got real keys
    key_original = 'вшебспирбуря'
    key_edited = 'вшекспирбуря'
    print()

    # Decrypt text with original key
    print(vigenere(ecnr_text, key_original, mode='dec'))

    # Decrypt text with modified key and write to a file
    shakespeare = vigenere(ecnr_text, key_edited, mode='dec')
    print(shakespeare)
    with open('text_decoded_shake.txt', 'w', encoding='utf8') as phack:
        phack.write(shakespeare)


