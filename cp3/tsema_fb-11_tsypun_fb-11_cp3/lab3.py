from typing import Optional
from itertools import permutations
from lab3_math import linear_comparsion, get_modulo_inverse
from lab3_text_recognizer import text_analysis, freq_count, ALPHA, MOST_COMMON_BIGR_IN_LANG


def text_purification(fLine: str, isnlp=False, save_space=False) -> (bool, str):
    isSpacePresent = False
    isNewLineCPresent = isnlp
    isBegining = True

    substitutions = {"ъ": "ь", "ё": "е"}
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

        elif s.lower() in ALPHA:
            output += s.lower()

        else:
            continue

        isSpacePresent = False
        isNewLineCPresent = False
        isBegining = False
    
    return isNewLineCPresent, output


def fLine_gen(fPath: str):
    with open(fPath, "r", encoding="utf8") as hFile:
        while fLine := hFile.readline():
            yield fLine
    hFile.close()


def find_key(text: str) -> list[Optional[tuple]]:
    good_candidates = list()

    m = len(ALPHA)
    eps = 0.3

    cypt_freq = {k: v for k, v in sorted(freq_count(text, 2).items(), key=lambda x: x[1], reverse=True)[0: 5]}

    most_common_in_cypt = list(cypt_freq.keys())

    for i, freq in enumerate(permutations(MOST_COMMON_BIGR_IN_LANG, 2)):
        x1 = ALPHA.index(freq[0][0]) * m + ALPHA.index(freq[0][1])
        y1 = ALPHA.index(most_common_in_cypt[0][0]) * m + ALPHA.index(most_common_in_cypt[0][1])

        x2 = ALPHA.index(freq[1][0]) * m + ALPHA.index(freq[1][1])
        y2 = ALPHA.index(most_common_in_cypt[1][0]) * m + ALPHA.index(most_common_in_cypt[1][1])

        a = linear_comparsion(x1 - x2, y1 - y2, m ** 2)

        if type(a) == list:
            for j, ai in enumerate(a):
                bi = (y1 - ai * x1) % (m ** 2)

                try:
                    entropy, lang_monogr_entropy, c_koef = text_analysis(decrypt(text, ai, bi))
                except TypeError:
                    print(f"No candidates for #{i}.{j}")
                    continue

                isgoodcandidate = True if (abs(entropy - lang_monogr_entropy) < eps and c_koef > 0.5) else False
                print(f"\tSubcandidate #{i}.{j} ({ai}, {bi}): {isgoodcandidate}")
                print(f"\n\t\t->Ent: {entropy}\n\t\t->c_koef: {c_koef}\n")

                if isgoodcandidate:
                    good_candidates.append((ai, bi))


        elif type(a) == int:
            b = (y1 - a * x1) % (m ** 2)

            try:
                entropy, lang_monogr_entropy, c_koef = text_analysis(decrypt(text, a, b))
            except TypeError:
                print(f"No candidates for #{i}")
                continue

            isgoodcandidate = True if (abs(entropy - lang_monogr_entropy) < eps and c_koef > 0.5) else False
            print(f"Candidate #{i} ({a}, {b}): {isgoodcandidate}")
            print(f"\t\t->Ent: {entropy}\n\t\t->c_koef: {c_koef}\n")

            if isgoodcandidate:
                good_candidates.append((a, b))
        else:
            print(f"No candidates for #{i}")

    print("\nGood candidates:\n" + "\n".join([f"Key: ({key[0]}, {key[1]})" for key in good_candidates]) + "\n")

    return good_candidates


def decrypt(text: str, a: int, b: int) -> str:
    m = len(ALPHA)
    result = ""
    for i in range(0, len(text), 2):
        y = ALPHA.index(text[i]) * m + ALPHA.index(text[i + 1])
        x = get_modulo_inverse(a, m ** 2)[0] * (y - b) % (m ** 2)
        result += ALPHA[x // m] + ALPHA[x % m]

    return result


def encrypt(text: str, a: int, b: int) -> str:
    m = len(ALPHA)
    result = ""

    for i in range(0, len(text), 2):
        x = ALPHA.index(text[i]) * m + ALPHA.index(text[i + 1])
        y = (a * x + b) % (m ** 2)
        result += ALPHA[y // m] + ALPHA[y % m]

    return result


if __name__ == "__main__":
    text = ""
    for l in fLine_gen("texts/v5_text"):
        isnlp, pur_line = text_purification(l)    
        text += pur_line 

    candidates = find_key(text)
    for candidate in candidates:
        print(f"Candidate {candidate}\n\n{decrypt(text, *candidate)}\n")
