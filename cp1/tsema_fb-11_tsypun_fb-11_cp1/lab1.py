from math import log2

alpha = "абвгдежзийклмнопрстуфхцчшщыьэюя"


def freq_count(text: str, n: int, ngr_intercept=False) -> dict[str, float]:
    step = 1 if ngr_intercept else n
    ngr_dict = {}
    
    for i in range(0, len(text) - n, step):
        if not text[i: i + n]:
            continue

        if text[i: i + n] not in ngr_dict.keys():
            ngr_dict.update({text[i: i + n]: 1})
        else:
            ngr_dict[text[i: i + n]] += 1

    return {i: ngr_dict[i] / sum(ngr_dict.values()) for i in sorted(ngr_dict.keys())}


def bigram_freq_csv_table(bgr_dict: dict, w_spaces=False):
    output = "*," + ",".join(alpha + int(w_spaces) * " ")
    for w in alpha + int(w_spaces) * " ":
        output += "\n" + w + "," + ",".join([str(bgr_dict[w + j]) if (w + j) in bgr_dict.keys() else '-' for j in alpha + int(w_spaces) * " "]) 

    return output


def monogr_freq_csv_table(monogr_dict: dict):
    output = ""
    for item in monogr_dict.items():
        output += ",".join([str(i) for i in item]) + "\n"

    return output


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

        elif s.lower() in alpha:
            output += s.lower()

        else:
            continue

        isSpacePresent = False
        isNewLineCPresent = False
        isBegining = False
    
    return isNewLineCPresent, output


def compute_entropy(n: int, freq_dict: dict):
    entropy = 0
    for freq in freq_dict.values():
        entropy -= freq * log2(freq)

    return entropy / n


def compute_redudancy(n: int, freq_dict: dict):
    entropy = compute_entropy(n, freq_dict)

    return 1 - (entropy/log2(len(alpha)))


def fLine_gen(fPath: str):
    with open(fPath, "r", encoding="utf8") as hFile:
        while fLine := hFile.readline():
            yield fLine


if __name__ == "__main__":
    with open("purified_text_w_s.txt", "w", encoding="utf8") as hFile:
        isnlp = False
        for fLine in fLine_gen("lab_text.txt"):
            isnlp, pur_line = text_purification(fLine, isnlp, True)
            hFile.writelines(pur_line)

    hFile.close()

    with open("purified_text_w_null.txt", "w", encoding="utf8") as hFile:
        isnlp = False
        for fLine in fLine_gen("lab_text.txt"):
            isnlp, pur_line = text_purification(fLine, isnlp)
            hFile.writelines(pur_line)

    hFile.close()

    with open("purified_text_w_s.txt", "r", encoding="utf8") as hFile:
        text_w_s = hFile.read()
    hFile.close()

    bigr_wo_int_dict = freq_count(text_w_s, 2)          # w/o ngram interceptions
    bigr_w_int_dict = freq_count(text_w_s, 2, True)     # w ngram interceptions
    monogr_dict = freq_count(text_w_s, 1, True)         # w ngram interceptions

    with open("lab1_bigram_with_interceptions_in_text_with_spaces.csv", "w", encoding="utf8") as csv_write:
        csv_write.write(bigram_freq_csv_table(bigr_w_int_dict, True))

    csv_write.close()

    with open("lab1_bigram_without_interceptions_in_text_with_spaces.csv", "w", encoding="utf8") as csv_write:
        csv_write.write(bigram_freq_csv_table(bigr_wo_int_dict, True))

    csv_write.close()

    with open("lab1_monogram_in_text_with_spaces.csv", "w", encoding="utf8") as csv_write:
        csv_write.write(monogr_freq_csv_table(monogr_dict))

    csv_write.close()

    print(10*"=" + "\nText with spaces\n" + 10*"=")

    print("H2 in text, with interceptions: " + str(compute_entropy(2, bigr_w_int_dict)) + '\n' +
          "R2 in text, with interceptions: " + str(compute_redudancy(2, bigr_w_int_dict)) + '\n' + 
          "H2 in text, w/o interceptions: " + str(compute_entropy(2, bigr_wo_int_dict)) + '\n' +
          "R2 in text, w/o interceptions: " + str(compute_redudancy(2, bigr_wo_int_dict)) + '\n' + 
          "H1 in text: " + str(compute_entropy(1, monogr_dict)) + '\n' + 
          "R1 in text: " + str(compute_redudancy(1, monogr_dict)))
    
    with open("purified_text_w_null.txt", "r", encoding="utf8") as hFile:
        text_wo_s = hFile.read()
    hFile.close()
    
    bigr_wo_int_dict = freq_count(text_wo_s, 2)          # w/o ngram interceptions
    bigr_w_int_dict = freq_count(text_wo_s, 2, True)     # w ngram interceptions
    monogr_dict = freq_count(text_wo_s, 1, True)         # w ngram interceptions

    with open("lab1_bigram_with_interceptions_in_text_without_spaces.csv", "w", encoding="utf8") as csv_write:
        csv_write.write(bigram_freq_csv_table(bigr_w_int_dict))

    csv_write.close()

    with open("lab1_bigram_without_interceptions_in_text_without_spaces.csv", "w", encoding="utf8") as csv_write:
        csv_write.write(bigram_freq_csv_table(bigr_wo_int_dict))

    csv_write.close()

    with open("lab1_monogram_in_text_without_spaces.csv", "w", encoding="utf8") as csv_write:
        csv_write.write(monogr_freq_csv_table(monogr_dict))

    csv_write.close()
    
    print(10*"=" + "\nText w/o spaces\n" + 10*"=")

    print("H2 in text, with interceptions: " + str(compute_entropy(2, bigr_w_int_dict)) + '\n' +
          "R2 in text, with interceptions: " + str(compute_redudancy(2, bigr_w_int_dict)) + '\n' + 
          "H2 in text, w/o interceptions: " + str(compute_entropy(2, bigr_wo_int_dict)) + '\n' +
          "R2 in text, w/o interceptions: " + str(compute_redudancy(2, bigr_wo_int_dict)) + '\n' + 
          "H1 in text: " + str(compute_entropy(1, monogr_dict)) + '\n' + 
          "R1 in text: " + str(compute_redudancy(1, monogr_dict)))
