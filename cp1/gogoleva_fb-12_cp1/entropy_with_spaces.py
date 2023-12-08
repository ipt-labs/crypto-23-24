import re
import math


file_path = r"C:\Users\Polya\Desktop\KPI\crypto\crypto-23-24\cp1\gogoleva_fb-12_cp1\bible.txt"

with open(file_path, "r") as file:
    cleaned_text = ''
    for line in file: 
        line = re.sub(r'[^а-яА-ЯёЁ]', ' ', line)
        # Видалення зайвих пробілів
        line = ' '.join(line.split())
        cleaned_text += line.lower()

# Підрахунок частоти літер
letter_counts = {}

for letter in cleaned_text:
    if letter in letter_counts:
        letter_counts[letter] += 1
    else:
        letter_counts[letter] = 1
sorted_letter_counts = dict(sorted(letter_counts.items(), key=lambda item: item[1], reverse=True))

bigram_with_overlap_counts = {}
bigram_without_overlap_counts = {}

for i in range(len(cleaned_text) - 1):
    #Підрахуємо частоту біграм з перетином
    bigram_with_overlap = cleaned_text[i:i + 2]
    if bigram_with_overlap in bigram_with_overlap_counts:
        bigram_with_overlap_counts[bigram_with_overlap] += 1
    else:
        bigram_with_overlap_counts[bigram_with_overlap] = 1

    if i % 2 == 0:
        #І без перетину
        bigram_without_overlap = cleaned_text[i:i + 2]
        if bigram_without_overlap in bigram_without_overlap_counts:
            bigram_without_overlap_counts[bigram_without_overlap] += 1\
            
        else:
            bigram_without_overlap_counts[bigram_without_overlap] = 1

sorted_bigram_with_overlap_counts = dict(sorted(bigram_with_overlap_counts.items(), key=lambda item: item[1], reverse=True))
sorted_bigram_without_overlap_counts = dict(sorted(bigram_without_overlap_counts.items(), key=lambda item: item[1], reverse=True))

# Підрахунок ентропії для літер (Н1)
entropy_letter = 0.0
total_letters = len(cleaned_text)

for count in sorted_letter_counts.values():
    probability = count / total_letters
    entropy_letter -= probability * math.log2(probability)

print("H1 у тексті з пробілами:", entropy_letter)

# Ентропія для біграм з перетином (H2)
entropy_bigram_with_overlap = 0.0
total_bigrams_with_overlap = len(cleaned_text) - 1

for count in sorted_bigram_with_overlap_counts.values():
    probability = count / total_bigrams_with_overlap
    entropy_bigram_with_overlap -=(probability * math.log2(probability))/2

print("H2 з перетином у тексті з пробілами:", entropy_bigram_with_overlap)

# Ентропія для біграм без перетину (H2)
entropy_bigram_without_overlap = 0.0
total_bigrams_without_overlap = len(cleaned_text) // 2

for count in sorted_bigram_without_overlap_counts.values():
    probability = count / total_bigrams_without_overlap
    entropy_bigram_without_overlap -= (probability * math.log2(probability))/2

print("H2 без перетину у тексті з пробілами:", entropy_bigram_without_overlap)

r_for_monograms = 1 - (entropy_letter/math.log2(34))
r_for_bigram_with_overlap = 1 - (entropy_bigram_with_overlap/math.log2(34))
r_for_bigram_without_overlap = 1 - (entropy_bigram_without_overlap/math.log2(34))

print("Надлишковість для монограм:",r_for_monograms)
print("Надлишковість для біграм з перетином:",r_for_bigram_with_overlap)
print("Надлишковість для біграм без перетину: ",r_for_bigram_without_overlap)

