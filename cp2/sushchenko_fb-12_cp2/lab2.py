alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
alph_len = len(alphabet)


def encrypt(text, key):
    result = ""
    for i in range(len(text)):
        i_index = alphabet.index(text[i])
        k_index = alphabet.index(key[i % len(key)])
        result += alphabet[(i_index + k_index) % alph_len]
    return result


def decrypt(text, key):
    result = ""
    for i in range(len(text)):
        i_index = alphabet.index(text[i])
        k_index = alphabet.index(key[i % len(key)])
        result += alphabet[(i_index - k_index) % alph_len]
    return result


def index_vidpov(text):
    text_length = len(text)
    amounts = {}
    sum = 0
    if text_length - 1 > 0:
        for i in text:
            if i in amounts:
                amounts[i] += 1
            else:
                amounts[i] = 1

        for i in alphabet:
            if i in amounts:
                sum += amounts[i] * (amounts[i] - 1)

        return sum/(text_length*(text_length-1))
    else:
        return 0


def find_blocks(text, r):
    result = []
    for i in range(r):
        block = ""
        for j in range(i, len(text), r):
            block += text[j]
        result.append(block)
    return result


def find_key_len(en_text):
    for i in range(2, 31):
        blocks = find_blocks(en_text, i)
        ind_vid = 0
        for block in blocks:
            ind_vid += index_vidpov(block)
        print(i, round(ind_vid/len(blocks), 3))


def find_keys(blocks_text):
    freq_decr = list("оеаинтслрв")
    freqs_encr = {}
    key = ""
    for i in freq_decr:
        for block in blocks_text:
            for c in block:
                if c in freqs_encr:
                    freqs_encr[c] += 1
                else:
                    freqs_encr[c] = 1

            y_i = alphabet.index(max(freqs_encr, key=freqs_encr.get))
            x_i = alphabet.index(i)
            key += alphabet[(y_i-x_i)%alph_len]
            freqs_encr = {}
        print("key:", key)
        key = ""


if __name__ == '__main__':
    with open("text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    print("ВТ:", text)
    print("index_vidpov:", round(index_vidpov(text), 3))

    keys = ["шо", "бру", "крип", "мячик", "безпонятияк"]

    for key in keys:
        r_key = encrypt(text, key)
        index_v = index_vidpov(r_key)
        print("ШТ:", r_key)
        print("index_vidpov:", round(index_v, 3))

    with open("text2.txt", "r", encoding="utf-8") as f:
        en_text = f.read()

    find_key_len(en_text)
    find_keys(find_blocks(en_text, 19))
    print("ВТ:", decrypt(en_text, "конкистадорыгермеса"))
