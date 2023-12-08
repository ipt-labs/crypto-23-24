from collections import defaultdict

letter_number = {"а" : 0, "б" : 1, "в" : 2, "г" : 3, "д" : 4, "е" : 5, "ё" : 6, "ж" : 7, "з" : 8, "и" : 9, "й" : 10, "к" : 11, "л" : 12,
                 "м" : 13, "н" : 14, "о" : 15, "п" : 16, "р" : 17, "с" : 18, "т" : 19, "у" : 20, "ф" : 21, "х" : 22, "ц" : 23, "ч" : 24, "ш" : 25, "щ" : 26, "ъ" : 27, "ы" : 28, "ь" : 29, 
                 "э" : 30, "ю" : 31, "я" : 32}

alphabet = {"а" : 0, "б" : 1, "в" : 2, "г" : 3, "д" : 4, "е" : 5, "ж" : 6, "з" : 7, "и" : 8, "й" : 9, "к" : 10, "л" : 11,
                 "м" : 12, "н" : 13, "о" : 14, "п" : 15, "р" : 16, "с" : 17, "т" : 18, "у" : 19, "ф" : 20, "х" : 21, "ц" : 22, "ч" : 23, "ш" : 24, "щ" : 25, "ъ" : 26, "ы" : 27, "ь" : 28, 
                 "э" : 29, "ю" : 30, "я" : 31}


#encodes text with Vigenere cypher
def encode(text, key):

    encode_text = ""
    for i in range(0, len(text)):
        number = (letter_number[text[i]] + letter_number[key[i % len(key)]]) % 33
        for char, index in letter_number.items():
            if index == number:
                encode_text += char
                break

    return encode_text

#counts compliance index of the given text
def index_count(text):

    letter_count = 0
    letter_pair = defaultdict(float)

    for i in text:
        letter_pair[i] += 1
        letter_count += 1

    sum = 0
    for key in letter_pair:
        sum += letter_pair[key] * (letter_pair[key] - 1)

    return sum/(letter_count * (letter_count - 1))

#creates array with blocks of text
def split_text(text, key_size):

    chunks = []
    for i in range(0, key_size):
        temp = ""
        for j in range(i, len(text), key_size):
            temp += text[j]
        chunks.append(temp)

    return chunks

#finds most frequent letter in given string
def most_freq(line):
    letter_freq = defaultdict(int)
    for i in line:
        letter_freq[i] += 1

    max = 0
    for key in letter_freq:
        if letter_freq[key] > max :
            max = letter_freq[key]
            char = key
    
    return char


#decodes given text that was encyphered with Vigener cypher
def decoder(text, r):

    key = ""

    for i in range(0, r):
        number = (alphabet[text[i]] - alphabet["о"]) % 32
        for char, index in alphabet.items():
            if index == number:
                key += char
                break

    return key

#count compliance inxed for blocks of size k
def index_count_blocks(blocks, key_size):

    index = 0
    for i in range(0, key_size):
        index += index_count(blocks[i])
    
    return index/len(blocks)

#final decoder
def full_decoder(text, key):

    decoded_text = ""
    for i in range(0, len(text)):
        number = (alphabet[text[i]] - alphabet[key[i % len(key)]]) % 32
        for char, index in alphabet.items():
            if index == number:
                decoded_text += char
                break

    return decoded_text


#encode text with different keys
with open("/home/kali/Desktop/cryptolab2/text_to_encode.txt", "r") as file_input, open("/home/kali/Desktop/cryptolab2/encoded_text_out.txt", "w") as file_output:

    for line in file_input:
        text = line

    key_2 = "цк"
    key_3 = "моб"
    key_4 = "дюна"
    key_5 = "чужой"
    key_10 = "актинограф"
    key_11 = "бактериолог"
    key_12 = "вариантность"
    key_13 = "гидатогенезис"
    key_14 = "неадаптивность"
    key_15 = "бензолсульфонат"
    key_16 = "картографический"
    key_17 = "гармонизированный"
    key_18 = "неуравновешенность"
    key_19 = "фрагментированность"
    key_20 = "электролюминисценция"

    encoded_text_2 = encode(text, key_2)
    encoded_text_3 = encode(text, key_3)
    encoded_text_4 = encode(text, key_4)
    encoded_text_5 = encode(text, key_5)
    encoded_text_10 = encode(text, key_10)
    encoded_text_11 = encode(text, key_11)
    encoded_text_12 = encode(text, key_12)
    encoded_text_13 = encode(text, key_13)
    encoded_text_14 = encode(text, key_14)
    encoded_text_15 = encode(text, key_15)
    encoded_text_16 = encode(text, key_16)
    encoded_text_17 = encode(text, key_17)
    encoded_text_18 = encode(text, key_18)
    encoded_text_19 = encode(text, key_19)
    encoded_text_20 = encode(text, key_20)


    # print("Index for open text:", index_count(text))
    # for i in range(2, 6):
    #     var_name = f"encoded_text_{i}"
    #     var_value = locals()[var_name]
    #     print(f"Index for key {i}:", index_count(var_value))

    # for i in range(10, 21):
    #     var_name = f"encoded_text_{i}"
    #     var_value = locals()[var_name]
    #     print(f"Index for key {i}:", index_count(var_value))

    for i in range(2, 6):
        file_output.write(f"\nEncoded text with key {i}\n")
        var_name = f"encoded_text_{i}"
        var_value = locals()[var_name]
        file_output.write(var_value)

    for i in range(10, 21):
        file_output.write(f"\nEncoded text with key {i}\n")
        var_name = f"encoded_text_{i}"
        var_value = locals()[var_name]
        file_output.write(var_value)
    

#text decoding
with open("/home/kali/Desktop/cryptolab2/encoded_text.txt", "r") as file_input_en:

    encoded_text = ""
    for enline in file_input_en:
        encoded_text += enline.lower()

    #print(decoder(encoded_text, 15))

    # for i in range(2, 31):
    #     print(f"Index of key size {i}:", index_count_blocks(split_text(encoded_text, i), i))            #now we know that the key length is 15 letters
    
    keys = split_text(encoded_text, 15)


    #selects most frequent letter from each block
    key_str = ""
    for i in range(0, 15):
        key_str += most_freq(keys[i])

    # print(decoder(key_str, 15))

    #decoded key
    decoded_key = decoder(key_str, 15)
    # print(full_decoder(encoded_text, decoded_key))

    #final key
    final_key = "арудазовархимаг"
    # print(decoded_key)
    print(full_decoder(encoded_text, final_key))