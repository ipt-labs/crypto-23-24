import re


def opening(filename):
    with open(filename, 'r', encoding='utf8') as file:
        text = file.read()
    return text


def first_text_formating(text):
    text = re.sub(r'[^а-яА-Я\s]', '', text)
    text = text.lower()
    text = ' '.join(text.split())
    text = text.replace('ё', 'е').replace('ъ', 'ь')
    return text


def second_text_no_whitespaces(text):
    text = first_text_formating(text)
    text = text.replace(' ', '')
    return text


def write_text_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)


def frequency_nonintersec_bigrams(text):
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

    sorted_bigrams = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    top_five_freq = [count for _, count in sorted_bigrams[:10]]

    for bigram, count in sorted_bigrams:
        if count in top_five_freq:
            freq = count / total_bigram_count
            print(f"Біграма 2 '{bigram}': {freq}")


if __name__ == "__main__":
    input_file = input("Введіть ім'я файлу для читання:")
    output_file_1 = "var12.txt"

    text = opening(input_file)
    clean_text = second_text_no_whitespaces(text)
    write_text_to_file(output_file_1, clean_text)
    frequency_nonintersec_bigrams(clean_text)
