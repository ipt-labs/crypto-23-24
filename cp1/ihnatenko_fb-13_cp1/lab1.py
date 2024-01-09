import math, csv

def rewrite(sourcefile, destfile):
    src = open(sourcefile, "r", encoding="utf-8")
    dest = open(destfile, "w+", encoding="utf-8")

    contents = src.read().lower().split()

    i = 0
    while i < len(contents):
        string = ""
        for j in range(len(contents[i])):
            if contents[i][j] == "ъ":
                string += "ь"
            elif contents[i][j] == "ё":
                string += "е"
            elif contents[i][j].isalpha() or contents[i] == " ":
                string += contents[i][j]
        if string == "":
            contents.pop(i)
        else:
            contents[i] = string
            i += 1
    
    dest.write(" ".join(contents))

    src.close()
    dest.close()

def no_spaces(sourcefile, destfile):
    open(destfile, "w+", encoding="utf-8").write("".join(open(sourcefile, "r", encoding="utf-8").read().split()))

def count_letter_fq(sourcefile):
    src = open(sourcefile, "r", encoding="utf-8")

    letter_fq = {}
    contents = src.read()

    for letter in contents:
        if letter in letter_fq.keys():
            letter_fq[letter] += 1
        else:
            letter_fq[letter] = 1
    
    for letter in letter_fq.keys():
        letter_fq[letter] /= len(contents)

    src.close()
    return letter_fq

def count_bigram_fq(sourcefile):
    src = open(sourcefile, "r", encoding="utf-8")
    
    bigram_fq_ovp = {}
    bigram_fq_no_ovp = {}
    contents = src.read()

    for i in range(len(contents) - 1):
        bigram_ovp = "".join((contents[i], contents[i+1]))

        if bigram_ovp in bigram_fq_ovp.keys():
            bigram_fq_ovp[bigram_ovp] += 1
        else:
            bigram_fq_ovp[bigram_ovp] = 1
    
    for i in range(len(contents) // 2):
        bigram_no_ovp = "".join((contents[i*2], contents[i*2 + 1]))

        if bigram_no_ovp in bigram_fq_no_ovp.keys():
            bigram_fq_no_ovp[bigram_no_ovp] += 1
        else:
            bigram_fq_no_ovp[bigram_no_ovp] = 1

    for bigram in bigram_fq_ovp.keys():
        bigram_fq_ovp[bigram] /= len(contents) - 1
    
    for bigram in bigram_fq_no_ovp.keys():
        bigram_fq_no_ovp[bigram] /= len(contents) // 2
    
    src.close()
    return bigram_fq_ovp, bigram_fq_no_ovp

def count_Hn(data_dict, n):
    Hn = 0
    for p in data_dict.values():
        Hn -= p * math.log2(p)
    return Hn / n

def count_r(entropy, alphabet_length):
    return 1 - (entropy / math.log2(alphabet_length))

def write_table(outfile, data_dict):
    with open(outfile, "w+", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerows(sorted(data_dict.items(), key = lambda x:x[1], reverse = True))

def write_matrix(outfile, data_dict):
    sorted_keys = sorted(data_dict.keys())
    matrix = []
    for key in sorted_keys:
        for i in range(2):
            if [key[i]] not in matrix:
                matrix.append([key[i]])

    matrix = sorted(matrix, key = lambda x:x[0])

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if (key := matrix[i][0] + matrix[j][0]) in sorted_keys:
                matrix[i].append(data_dict[key])
            else:
                matrix[i].append(0)

    with open(outfile, "w+", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow([""] + [line[0] for line in matrix])
        writer.writerows(matrix)


def main():
    rewrite("raw.txt", "format.txt")
    no_spaces("format.txt", "no_spaces.txt")
    letter_fq = count_letter_fq("format.txt")
    letter_fq_no_spaces = count_letter_fq("no_spaces.txt")
    bigram_fq_ovp, bigram_fq_no_ovp = count_bigram_fq("format.txt")
    bigram_fq_ovp_no_spaces, bigram_fq_no_ovp_no_spaces = count_bigram_fq("no_spaces.txt")

    print("Питома ентропія H1 тексту з пробілами: ", count_Hn(letter_fq, 1))
    print("Питома ентропія H1 тексту без пробілів: ", count_Hn(letter_fq_no_spaces, 1))
    print("Питома ентропія H2 тексту з пробілами та кроком 1: ", count_Hn(bigram_fq_ovp, 2))
    print("Питома ентропія H2 тексту без пробілів та кроком 1: ", count_Hn(bigram_fq_ovp_no_spaces, 2))
    print("Питома ентропія H2 тексту з пробілами та кроком 2: ", count_Hn(bigram_fq_no_ovp, 2))
    print("Питома ентропія H2 тексту без пробілів та кроком 2: ", count_Hn(bigram_fq_no_ovp_no_spaces, 2))
    print("Надлишковість при H(10) = 1.4856: ", count_r(1.4856, 32))
    print("Надлишковість при H(10) = 2.3290: ", count_r(2.3290, 32))
    print("Надлишковість при H(20) = 1.5130: ", count_r(1.5130, 32))
    print("Надлишковість при H(20) = 2.3614: ", count_r(2.3614, 32))
    print("Надлишковість при H(30) = 1.0627: ", count_r(1.0627, 32))
    print("Надлишковість при H(30) = 1.8410: ", count_r(1.8410, 32))

    write_table("letter_fq.csv", letter_fq)
    write_table("letter_fq_no_spaces.csv", letter_fq_no_spaces)
    write_matrix("bigram_fq_ovp.csv", bigram_fq_ovp)
    write_matrix("bigram_fq_ovp_no_spaces.csv", bigram_fq_ovp_no_spaces)
    write_matrix("bigram_fq_no_ovp.csv", bigram_fq_no_ovp)
    write_matrix("bigram_fq_no_ovp_no_spaces.csv", bigram_fq_no_ovp_no_spaces)

    return 0

if __name__ == "__main__":
    main()