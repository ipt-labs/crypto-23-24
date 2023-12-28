import re

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

def read_text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def write_text_to_file(filename, text):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == "__main__":
    input_file = input("Введіть ім'я файлу для читання:")
    output_file_1 = "clear_text_with_whitespaces.txt"
    output_file_2 = "clear_text_without_whitespaces.txt"

    text = read_text_from_file(input_file)
    formated_text = first_text_formating(text)
    no_whitespaces_text = second_text_no_whitespaces(text)
    write_text_to_file(output_file_1, formated_text)
    write_text_to_file(output_file_2, no_whitespaces_text)



