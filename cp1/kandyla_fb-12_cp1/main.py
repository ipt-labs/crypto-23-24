import math

def main():

    unfiltered = "unfiltered.txt"
    filtered = "filtered.txt"
    text_filter(unfiltered, filtered)
    h1 = entropy_h1(filtered)
    h2 = entropy_h2(filtered)
    print(h1)
    print(h2)
    print(math.log(34,2))
    return 0

def text_filter(unfiltered_file, filtered_file):

    with open(unfiltered_file, 'r', encoding="utf8") as file:
        text = file.read().lower()
    new_string = ""
    allowed = "абвгдежзийклмнопрстуфхцчшщъыьэюя "
    for symbol in text:
        if symbol in allowed :
            new_string += symbol
    final_text = ' '.join(new_string.split())
    with open(filtered_file, 'w', encoding="utf-8") as file:
        file.write(final_text)

def entropy_h1(file):
    with open(file, 'r', encoding="utf8") as f:
        text = f.read().lower()
    text_no_space = ''.join(text.split())
    text_with_space = ' '.join(text.split())

    dict_no_space = letter_count(text_no_space)
    dict_with_space = letter_count(text_with_space)
    h1 = [entropy_h1_calc(dict_no_space, "no"), entropy_h1_calc(dict_with_space, "with")]
    return h1

def entropy_h2(file):
    with open(file, 'r', encoding="utf8") as f:
        text = f.read().lower()
    text_no_space = ''.join(text.split())
    text_with_space = ' '.join(text.split())

    bigram_no_cross_no_space = no_cross(text_no_space)
    bigram_with_cross_no_space = with_cross(text_no_space)
    bigram_no_cross_with_space = no_cross(text_with_space)
    bigram_with_cross_with_space = with_cross(text_with_space)

    h2 = [entropy_h2_calc(bigram_no_cross_no_space, "no"),
          entropy_h2_calc(bigram_with_cross_no_space, "no"),
          entropy_h2_calc(bigram_no_cross_with_space, "with"),
          entropy_h2_calc(bigram_with_cross_with_space, "with")]

    return h2

def letter_count(text:str):
    dictionary = {"total" : 0}
    for symbol in text:
        dictionary["total"] += 1
        if symbol not in dictionary:
            dictionary[symbol] = 1
        else:
            dictionary[symbol] += 1
    return dictionary

def no_cross(text:str):
    bigram_no_cross = {"total" : 0}
    for i in range(0, len(text) - 1, 2):
        pair = text[i: i+2]
        if pair != '':
            bigram_no_cross["total"] += 1
            if pair not in bigram_no_cross:
                bigram_no_cross[pair] = 1
            else:
                bigram_no_cross[pair] += 1
    return bigram_no_cross

def with_cross(text:str):
    bigram_with_cross = {"total" : 0}
    for i in range(len(text) - 1):
        pair = text[i: i + 2]
        if pair != '':
            bigram_with_cross["total"] += 1
            if pair not in bigram_with_cross:
                bigram_with_cross[pair] = 1
            else:
                bigram_with_cross[pair] += 1
    return bigram_with_cross

def entropy_h1_calc(dictionary:dict, indicator): #temp - надлишковість
    result = 0
    for key in dictionary.keys():
        if key != "total":
            p = dictionary[key] / dictionary["total"]
            result += p*math.log(p, 2)
    result = -result
    if indicator == "with":
        temp = 1 - result/math.log(33, 2)
        return [result, temp]
    elif indicator == "no":
        temp = 1 - result / math.log(32, 2)
        return [result, temp]

def entropy_h2_calc(bigram:dict, indicator): #temp - надлишковість
    result = 0
    for key in bigram.keys():
        if key != "total":
            p = bigram[key] / bigram["total"]
            result += p*math.log(p, 2)
    result = -result/2
    if indicator == "with":
        temp = 1 - result / math.log(33, 2)
        return [result, temp]
    elif indicator == "no":
        temp = 1 - result / math.log(32, 2)
        return [result, temp]

if __name__ == "__main__":
    main()