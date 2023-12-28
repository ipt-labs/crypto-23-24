import re
import csv


# function for formatting text without spaces
def cleaning_without_spaces(path):
    with open(path, 'r', encoding="UTF-8") as reader:
        cleaned_text = re.sub(r'[^а-яА-ЯёЁ]', '', reader.read()).replace('\n', '').replace('ё', 'е').replace('Ё', 'Е').lower()
        return cleaned_text


# funtion for creating valid text without spaces
def creating_valid_text_without_spaces(input_path, output_path):
    with open(output_path, 'w', encoding="UTF-8") as writer:
        writer.write(cleaning_without_spaces(input_path))


# function for returning valid text as string
def get_text(path):
    with open(path, 'r', encoding="UTF-8") as reader:
        return reader.read()


# get frequency dict
def get_frequency(input_path):
    res_dict = {}
    with open(input_path, mode='r', newline='', encoding="UTF-8") as file:
        reader = csv.reader(file)
        for row in reader:
            res_dict[row[0]] = row[1]

    return res_dict


if __name__ == '__main__':
    # creating valid text examples
    # valid text without spaces
    creating_valid_text_without_spaces('text.txt', 'valid_text_without_spaces.txt')
