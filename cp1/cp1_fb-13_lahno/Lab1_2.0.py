import math

def opening(filename):
    with open(filename, 'r', encoding='utf8') as file:
        text = file.read()
    return text

def frequency_letter(text, output_file):
    counter = {}
    total_letters = 0

    for char in text:
        if char.isalpha() or char.isspace():
            total_letters += 1
            if char in counter:
                counter[char] += 1
            else:
                counter[char] = 1
    with open(output_file, 'w', encoding='utf8') as file:
        for letter, count in counter.items():
            freq = count / total_letters
            file.write(f"Літера '{letter}': {freq}\n")

    entropy = entropy_calc(counter)
    print(f'Ентропія тексту : {entropy} ')
    if text == text1:
        r = redundancy(entropy, 32)
        print(f'Надлишковість тексту : {r}')
    else:
        r = redundancy(entropy, 31)
        print(f'Надлишковість тексту : {r}' )

def frequency_bigrams(text, output_file):
    counter = {}
    total_bigram_count = 0

    if len(text) < 2:
        print("Текст має недостатньо символів для підрахунку біграм.")
        return
    for i in range(len(text) - 1):
        bigram = text[i:i + 2]
        total_bigram_count += 1

        if bigram in counter:
            counter[bigram] += 1
        else:
            counter[bigram] = 1
    with open(output_file, 'w', encoding='utf8') as file:
        for bigram, count in counter.items():
            freq = count / total_bigram_count
            file.write(f"Біграма '{bigram}': {freq}\n")

    entropy = entropy_calc(counter)
    print(f'Ентропія тексту : {entropy} біт')
    if text == text1:
        r = redundancy(entropy, 32)
        print(f'Надлишковість тексту : {r}')
    else:
        r = redundancy(entropy, 31)
        print(f'Надлишковість тексту : {r}' )


def frequency_nonintersec_bigrams(text, output_file):
    counter = {}
    total_bigram_count = 0

    if len(text) < 2:
        print("Текст має недостатньо символів для підрахунку біграм.")
        return
    for i in range(0, len(text) - 1, 2):
        bigram = text[i:i + 2]
        total_bigram_count += 1

        if bigram in counter:
            counter[bigram] += 1
        else:
            counter[bigram] = 1
    with open(output_file, 'w', encoding='utf8') as file:
        for bigram, count in counter.items():
            freq = count / total_bigram_count
            file.write(f"Біграма 2 '{bigram}': {freq}\n")

    entropy = entropy_calc(counter)
    print(f'Ентропія тексту : {entropy} біт')
    if text == text1:
        r = redundancy(entropy, 32)
        print(f'Надлишковість тексту : {r}')
    else:
        r = redundancy(entropy, 31)
        print(f'Надлишковість тексту : {r}' )

def entropy_calc(counter):
    total_count = sum(counter.values())
    entropy = []
    for c in counter.values():
        if c != 0:
            freq = c / total_count
            entropy.append(-(freq * math.log2(freq)))
    for k in counter.keys():
        if len(k) > 1:
            entropy_num = 0.5 * sum(entropy)
        else:
            entropy_num = sum(entropy)
    return entropy_num

def redundancy(entropy, num_of_letters):
    redundancy = 1 - (entropy / math.log2(num_of_letters))
    return redundancy

filename1 = 'clear_text_with_whitespaces.txt'
filename2 = 'clear_text_without_whitespaces.txt'
text1 = opening(filename1)
text2 = opening(filename2)

output_file1 = 'output_text1.txt'
output_file2 = 'output_text2.txt'
output_file3 = 'output_text3.txt'
output_file4 = 'output_text4.txt'
output_file5 = 'output_text5.txt'
output_file6 = 'output_text6.txt'

print("="*100)
frequency_letter(text1, output_file1)
print("="*100)
frequency_letter(text2, output_file2)
print("="*100)
frequency_bigrams(text1, output_file3)
print("="*100)
frequency_bigrams(text2, output_file4)
print("="*100)
frequency_nonintersec_bigrams(text1, output_file5)
print("="*100)
frequency_nonintersec_bigrams(text2, output_file6)