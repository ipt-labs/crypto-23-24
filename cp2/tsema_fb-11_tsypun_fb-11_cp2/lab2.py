# 5 var Tsema Tsypun


alpha = "абвгдежзийклмнопрстуфхцчшщъыьэюя"

ind0 = 1/len(alpha)

def get_lang_p() -> dict:
    res = {}
    with open("lab1_stats/lab1_monogram_in_text_without_spaces.csv", "r") as freq:
        while l := freq.readline():
            res.update({l.split(",")[0]: float(l.split(",")[1][:-1])})

    return res


def ind_of_c_theor() -> float:
    result = 0

    with open("lab1_stats/lab1_monogram_in_text_without_spaces.csv", "r") as freq:
        while l := freq.readline():
            result += float(l.split(",")[1][:-1]) ** 2 

    return result


alpha_sorted_by_freq = "".join(tuple(dict(sorted(dict(get_lang_p()).items(), key=lambda x: x[1], reverse=True)).keys()))
ind_theor = ind_of_c_theor()


def text_purification(fLine: str, isnlp=False, save_space=False) -> (bool, str):
    isSpacePresent = False
    isNewLineCPresent = isnlp
    isBegining = True

    substitutions = {"ё": "е"}
    output = ""
    for s in fLine:
        if s == " " and not isSpacePresent and not isBegining:
            isSpacePresent = True
            if save_space:
                output += s
            continue

        if s == '\n' and not isNewLineCPresent:
            isNewLineCPresent = True
            if save_space and not isSpacePresent:
                output += " "
                isSpacePresent = True
            continue

        if s in substitutions.keys():
            output += substitutions[s]

        elif s.lower() in alpha:
            output += s.lower()

        else:
            continue

        isSpacePresent = False
        isNewLineCPresent = False
        isBegining = False

    return isNewLineCPresent, output


def line_gen(path: str):
    with open(path, "r", encoding="utf-8") as f:
        while (l := f.readline()):
            yield l


def kron_delta(text: str, thr: int) -> None:
    t_len = len(text)

    for r in range(1, 100):
        Dr = 0
        for i in range(1, t_len - r):
            Dr += int(text[i] == text[i + r])

        if Dr > thr: 
            print(f"{Dr:<6}|{r}")


def c_count(text: str) -> dict[str, int]:
    res = {k: 0 for k in alpha}

    for c in alpha:
        res[c] = text.count(c)

    return res
    

def vigenere(key: str, text: str, decrypt=False) -> str:
    key = key.lower()
    r = len(key)
    m = len(alpha)
    result = ""

    for i in range(len(text)):
        result += alpha[(alpha.index(text[i]) + ((-1) ** int(decrypt))*alpha.index(key[i % r])) % m]

    return result


def ind_of_coincidence(c_dict: dict, text_len: int) -> float:
    result = 0
    for c in c_dict.values():
        result += c * (c - 1)

    return result / (text_len * (text_len - 1))
    

def get_key(freq_chars_per_block: str, n: int) -> str:
    key = ""
    for c in freq_chars_per_block:
        key += alpha[(alpha.index(c) - alpha.index(alpha_sorted_by_freq[n])) % len(alpha)]

    return key


def decrypter(text: str, delta: float, r_max: int) -> str:
    blocks = {}

    print(f"\nClosest to ind_of_c_theor indices of coincidence:\n\n{'Index':^22}|Key length") 
    for r in range(2, r_max):
        avg_ind = 0
        coinc_per_block = {}

        for i in range(0, r):
            block_len = len(text[i::r])

            if block_len == 1:
                continue

            inblock_coinc = c_count(text[i::r])
            avg_ind += ind_of_coincidence(inblock_coinc, block_len)

            coinc_per_block.update({i: inblock_coinc})

        if abs(avg_ind/r - ind_theor) < delta:
            blocks.update({r: coinc_per_block})
            print(f"{avg_ind/r:<22}|{r:^10}")

    key_len = list(blocks.keys())[0]

    c_blocks = dict(blocks[key_len])
    
    freq_chars_per_block = ""
    for i in range(0, key_len):
        c_block = tuple(dict(sorted(dict(c_blocks[i]).items(), key=lambda x: x[1], reverse=True)).keys())
        freq_chars_per_block += c_block[0]

    return freq_chars_per_block


if __name__ == "__main__":
    isnlp = False
    p_text = ""
    for l in line_gen("text_to_encrypt.txt"):
        isnlp, pt = text_purification(l, isnlp)
        p_text += pt

    ind = ind_of_coincidence(c_count(p_text), len(p_text))
    print(f"\n\nI: {ind}\n\nO: {p_text}")

    keys = ("бе", "чай", "пиво", "кефир", "пиццасананасами")

    for k in keys:
        ct = vigenere(k, p_text)
        ind = ind_of_coincidence(c_count(ct), len(ct))
        print(f"\n\n{'Key length:':<15}{len(k)}\n{'Index:':<15}{ind}\n{'Key:':<15}{k}\n{'CT Fragment:':<15}{ct[:100]}")

    text = ""
    isnlp = False
    for l in line_gen("text_to_decrypt.txt"):
        isnlp, pt = text_purification(l, isnlp)
        text += pt 

    print(f"\nKronecker symbol results:\n\n{'Delta':^6}|Key length")
    kron_delta(text, 250)
    fcpb = decrypter(text, 0.01, 100)

    for i in range(len(alpha_sorted_by_freq)):
        pkey = get_key(fcpb, i)
        print(f"\n{'Key:':<20}{pkey}\n{'CT fragment:':<20}{text[0:len(pkey)*2]}\n{'Vigenere result:':<20}{vigenere(pkey, text[0:len(pkey)*2], True)}\n")
    
    while True:
        k = input("Enter possible key: ")
        print(f"\n{'Key:':<20}{k}\n{'CT fragment:':<20}{text[0:len(k)*2]}\n{'Vigenere result:':<20}{vigenere(k, text[0:len(k)*2], True)}\n")

        yo = input("Was the key correct? (y/n): ")
        if yo in ("y", "Y"):
            break
