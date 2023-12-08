import pandas as pd
import math

with open("text.txt", "r", encoding="utf-8") as file:
    text = file.read()

with open("text_no_spaces.txt", "r", encoding="utf-8") as file:
    text_no_spaces = file.read()

def letfreq(text, with_spaces=True):
    total_letters = len(text)
    letter_frequencies = {}
    if with_spaces:
        alphabet = 33
    else:
        alphabet = 32

    for letter in text:
        if letter in letter_frequencies:
            letter_frequencies[letter] += 1
        else:
            letter_frequencies[letter] = 1

    for letter in letter_frequencies:
        letter_frequencies[letter] /= total_letters

    sortedlet = sorted(letter_frequencies.items(), key=lambda x: x[1], reverse=True)
    entropy = -sum((freq * math.log2(freq) for letter, freq in sortedlet))
    redundancy = 1 - (entropy / math.log2(alphabet))

    return sortedlet, entropy, redundancy

def bigram_no_cross(text, with_spaces=True):
    total_bigrams = len(text) - 1
    bigram_frequencies = {}
    if with_spaces:
        alphabet = 33
    else:
        alphabet = 32

    for i in range(0, total_bigrams, 2):
        bigram = text[i:i+2]
        if bigram in bigram_frequencies:
            bigram_frequencies[bigram] += 1
        else:
            bigram_frequencies[bigram] = 1

    for bigram in bigram_frequencies:
        bigram_frequencies[bigram] /= (total_bigrams // 2)

    entropy = -(1/2)*sum((freq * math.log2(freq) for bigram, freq in bigram_frequencies.items()))
    redundancy = 1 - (entropy / math.log2(alphabet))

    return bigram_frequencies, entropy, redundancy

def bigram_cross(text, with_spaces=True):
    total_bigrams = len(text) - 1
    bigram_frequencies = {}
    if with_spaces:
        alphabet = 33
    else:
        alphabet = 32

    for i in range(total_bigrams):
        bigram = text[i:i+2]
        if bigram in bigram_frequencies:
            bigram_frequencies[bigram] += 1
        else:
            bigram_frequencies[bigram] = 1

    for bigram in bigram_frequencies:
        bigram_frequencies[bigram] /= total_bigrams

    entropy = -(1/2)*sum((freq * math.log2(freq) for bigram, freq in bigram_frequencies.items()))
    redundancy = 1 - (entropy / math.log2(alphabet))

    return bigram_frequencies, entropy, redundancy

def zero_format(value):
    return '{:.20f}'.format(value)

# 1 Текст з пробілами
result1, entropy1, redundancy1 = letfreq(text, with_spaces=True)
df1 = pd.DataFrame(result1, columns=['Символ', 'Частота'])
df1['Частота'] = df1['Частота'].apply(zero_format)
df1.to_csv('result1.txt', sep='\t', index=False, encoding='utf-8')
with open('result1.txt', 'a', encoding='utf-8') as f:
    f.write(f'Ентропія: {entropy1}\n')
    f.write(f'Надлишковість: {redundancy1}\n')

# 2 Текст без пробілів
result2, entropy2, redundancy2 = letfreq(text_no_spaces, with_spaces=False)
df2 = pd.DataFrame(result2, columns=['Символ', 'Частота'])
df2['Частота'] = df2['Частота'].apply(zero_format)
df2.to_csv('result2.txt', sep='\t', index=False, encoding='utf-8')
with open('result2.txt', 'a', encoding='utf-8') as f:
    f.write(f'Ентропія: {entropy2}\n')
    f.write(f'Надлишковість: {redundancy2}\n')

# 3 Біграми з перетином, текст з пробілами
result3, entropy3, redundancy3 = bigram_cross(text, with_spaces=True)
data3 = result3
unique_letters = sorted(set(''.join(data3.keys()))
)
df3 = pd.DataFrame(index=unique_letters, columns=unique_letters)
for letter1 in unique_letters:
    for letter2 in unique_letters:
        value = data3.get(letter1 + letter2, 0)
        df3.at[letter1, letter2] = zero_format(value)
df3.to_csv('result3.txt', sep='\t', encoding='utf-8')
with open('result3.txt', 'a', encoding='utf-8') as f:
    f.write(f'Ентропія: {entropy3}\n')
    f.write(f'Надлишковість: {redundancy3}\n')

# 4 Біграми без перетину, текст без пробілів
result4, entropy4, redundancy4 = bigram_no_cross(text_no_spaces, with_spaces=False)
data4 = result4
unique_letters = sorted(set(''.join(data4.keys()))
)
df4 = pd.DataFrame(index=unique_letters, columns=unique_letters)
for letter1 in unique_letters:
    for letter2 in unique_letters:
        value = data4.get(letter1 + letter2, 0)
        df4.at[letter1, letter2] = zero_format(value)
df4.to_csv('result4.txt', sep='\t', encoding='utf-8')
with open('result4.txt', 'a', encoding='utf-8') as f:
    f.write(f'Ентропія: {entropy4}\n')
    f.write(f'Надлишковість: {redundancy4}\n')

# 5 Біграми з перетином, текст без пробілів
result5, entropy5, redundancy5 = bigram_cross(text_no_spaces, with_spaces=False)
data5 = result5
unique_letters = sorted(set(''.join(data5.keys()))
)
df5 = pd.DataFrame(index=unique_letters, columns=unique_letters)
for letter1 in unique_letters:
    for letter2 in unique_letters:
        value = data5.get(letter1 + letter2, 0)
        df5.at[letter1, letter2] = zero_format(value)
df5.to_csv('result5.txt', sep='\t', encoding='utf-8')
with open('result5.txt', 'a', encoding='utf-8') as f:
    f.write(f'Ентропія: {entropy5}\n')
    f.write(f'Надлишковість: {redundancy5}\n')

# 6 Біграми без перетину, текст з пробілами
result6, entropy6, redundancy6 = bigram_no_cross(text, with_spaces=True)
data6 = result6
unique_letters = sorted(set(''.join(data6.keys()))
)
df6 = pd.DataFrame(index=unique_letters, columns=unique_letters)
for letter1 in unique_letters:
    for letter2 in unique_letters:
        value = data6.get(letter1 + letter2, 0)
        df6.at[letter1, letter2] = zero_format(value)
df6.to_csv('result6.txt', sep='\t', encoding='utf-8')
with open('result6.txt', 'a', encoding='utf-8') as f:
    f.write(f'Ентропія: {entropy6}\n')
    f.write(f'Надлишковість: {redundancy6}\n')