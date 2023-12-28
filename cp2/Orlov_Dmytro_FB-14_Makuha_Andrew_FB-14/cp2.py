from collections import Counter
import pandas as pd
from matplotlib import pyplot as plt
import re


class vigenere_analys:
    def __init__(self) -> None:
        self.alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
        self.language_index = 0.0553
        pass

    def filter_input(self, text):
        # lowercase input for filtering
        text = text.lower()

        # drop non russian symbols via regex
        text = re.sub("[^а-я]", " ", text)

        text = re.sub(r'\s+', '', text)

        # Replace letters which not included in task alphabet
        text = text.replace("ё", "е")

        return text

    def split_on_blocks(self, text, r):
        blocks = []
        index = 0
        for letter in text:
            if r != len(blocks):
                blocks.append("")
            else:
                blocks[index] += letter
            if index + 1 > r - 1:
                index = 0
            else:
                index += 1
        return blocks

    def count_indexes_by_y_blocks(self, text) -> dict:
        blocks_dict = {}
        for r in range(2, 31):
            blocks = self.split_on_blocks(text, r)
            index = sum(self.index_of_coincidence(block) for block in blocks) / r
            blocks_dict["r" + str(r)] = index
        return blocks_dict

    def find_possible_keys(self, text, r):
        blocks = self.split_on_blocks(text, r)
        letters = [
            "о",
            "е",
            "а",
            "и",
            "т",
            "н",
            "с",
        ]
        for letter in letters:
            key = []
            for block in blocks:
                blocks_num = Counter(list(block))
                max_num = sorted(blocks_num.items(), key=lambda x: x[1], reverse=True)[
                     0
                ][0]
                key_letter = self.alphabet[
                    (self.alphabet.index(max_num) - self.alphabet.index(letter))
                    % len(self.alphabet)
                ]
                key.append(key_letter)
            print("".join(key))

    def index_of_coincidence(self, text):
        letters_count = Counter(text)
        text_len = len(text)
        index = sum(count * (count - 1) for count in letters_count.values()) / (
            text_len * (text_len - 1)
        )
        return index

    def encrypt(self, text, key):
        index = 0
        text_y = ""
        for x_letter in text:
            text_y += self.alphabet[
                (self.alphabet.index(x_letter) + self.alphabet.index(key[index]))
                % len(self.alphabet)
            ]
            if index + 1 > len(key) - 1:
                index = 0
            else:
                index += 1

        return text_y
    
    def decrypt1(self, text, key):
        index = 0
        text_x = ""
        for y_letter in text:
            text_x += self.alphabet[
                (self.alphabet.index(y_letter) - self.alphabet.index(key[index]))
                % len(self.alphabet)
            ]
            if index + 1 > len(key) - 1:
                index = 0
            else:
                index += 1

        return text_x
    
    def decrypt(self,text, key):
        decrypted_text = [self.alphabet[(self.alphabet.find(text[i]) - self.alphabet.find(key[i % len(key)])) % len(self.alphabet)]
                        for i in range(len(text))]
        return ''.join(decrypted_text)

    def save_period_calculations(self, dict: dict, filename: str):
        df = pd.DataFrame({"Довжина": dict.keys(), "Індекс": dict.values()})
        df.to_csv(filename)
        plt.figure(figsize=(10, 5))
        plt.bar(df["Довжина"], df["Індекс"], color="c")
        plt.xticks(df["Довжина"])
        plt.show()


analysis = vigenere_analys()

# task with encryption
with open("input_text.txt", "r", encoding="utf-8") as file:
    input_text = file.read()

input_text = analysis.filter_input(input_text)
keys = {"r2": "ок", "r3": "хей", "r4": "втек", "r5": "сивик", "r14": "турбокомпресор"}

Ir = analysis.index_of_coincidence(input_text)
print('Ir: '+str(Ir))
indexes = {"original": Ir}

for rkey,key in keys.items():
    encrytped_text = analysis.encrypt(input_text, key)
    file_enctypted_prefix = "r_" + str(len(key))
    f = open(file_enctypted_prefix + "_encrytped.txt", "a")
    f.write(encrytped_text)
    f.close()
    indexes[rkey] = analysis.index_of_coincidence(encrytped_text)

analysis.save_period_calculations(indexes, "indexes_for_task_2.csv")

with open("text_to_decrypt.txt", "r", encoding="utf-8") as file:
    text_to_decrypt = file.read()

indexes = analysis.count_indexes_by_y_blocks(text_to_decrypt)
analysis.save_period_calculations(indexes, "indexes_for_task_3.csv")

r = int(input('Enter possible r(1): '))

analysis.find_possible_keys(text_to_decrypt, r)

r = int(input('Enter possible r(2): '))

analysis.find_possible_keys(text_to_decrypt, r)

key = input('Enter valid key: ')

with open('decrypted_text.txt', 'w', encoding='utf-8') as file:
    file.write(analysis.decrypt(text_to_decrypt,key))
