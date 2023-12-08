import re

ALPHABET = "абвгдежзийклмнопрстуфхцчшщьыэюя"

class AffineCipher:
    def __init__(self) -> None:
        self.alphabet = ALPHABET
        self.r_frequent_bigrams = "стнотонаен"  # ст-545; но-417; то-572; на-403; ен-168
        self.impossible_bigrams = [
            "аь",
            "еь",
            "иь",
            "оь",
            "уь",
            "ыь",
            "ьь",
            "эь",
            "юь",
            "яь",
            "аы",
            "еы",
            "иы",
            "оы",
            "уы",
            "ыы",
            "эы",
            "юы",
            "яы",
        ]

    def filter(self, text):
        text = text.lower()
        text = re.sub(r"[^\sа-я]", "", text)
        text = re.sub(r"\s+", "", text)
        if len(text) % 2 != 0:
            text = text[:-1]
        return text

    def encrypt(self, text, a, b):
        pt = self.filter(text)
        if len(pt) % 2 != 0:
            pt += pt[-1]
        bigrams_intConv = self.convert_text_to_ints(pt)
        ct_intConv = [(bg * a + b) % len(ALPHABET) ** 2 for bg in bigrams_intConv]
        ct = self.convert_ints_to_text(ct_intConv)
        return ct

    def decrypt(self, text, a, b):
        _, a_inv, _ = self.extended_gcd(a, len(ALPHABET) ** 2)
        bigrams_intConv = self.convert_text_to_ints(text)
        pt_intConv = [((bg - b) * a_inv) % len(ALPHABET) ** 2 for bg in bigrams_intConv]
        pt = self.convert_ints_to_text(pt_intConv)
        return pt

    def convert_text_to_ints(self, text):
        res = []
        text = self.filter(text)
        for i in range(0, len(text), 2):
            x0 = ALPHABET.index(text[i])
            x1 = ALPHABET.index(text[i + 1])
            X = x0 * len(ALPHABET) + x1
            res += [X]
        return res

    def convert_ints_to_text(self, bigrams):
        text = ""
        for bg in bigrams:
            x1 = ALPHABET[bg % len(ALPHABET)]
            x0 = ALPHABET[bg // len(ALPHABET)]
            text += x0 + x1
        return text

    def get_combinations(self, list):
        res = []
        n = len(list)
        for i in range(n):
            for j in range(i + 1, n):
                if list[i] != list[j]:
                    res.append([list[i], list[j]])
        return res

    def find_tmp_key(self, X, Y):
        x0, x1 = X
        y0, y1 = Y
        y_sub = y0 - y1
        x_sub = x0 - x1
        g, x_sub_inv, _ = self.extended_gcd(x_sub, len(ALPHABET) ** 2)
        a = (y_sub * x_sub_inv) % len(ALPHABET) ** 2
        b = (y0 - a * x0) % len(ALPHABET) ** 2

        return [a, b]

    def find_keys(self, encrypted_text):
        freq_bigrams = list(self.bigram_frequency(encrypted_text))[:5]
        en_combinations = self.get_combinations(
            self.convert_text_to_ints("".join(freq_bigrams))
        )
        most_fre_combinations = self.get_combinations(
            self.convert_text_to_ints(self.r_frequent_bigrams)
        )

        keys = []
        for i in en_combinations:
            for j in most_fre_combinations:
                a_tmp, b_tmp = self.find_tmp_key(j, i)
                tmp_text = self.decrypt(encrypted_text, a_tmp, b_tmp)

                if self.check_impossible_bigrams(tmp_text):
                    if [a_tmp, b_tmp] not in keys:
                        keys.append([a_tmp, b_tmp])

        return keys

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def bigram_frequency(self, text):
        dictionary = {}
        array = []

        for i in range(0, len(text), 2):
            bigram = text[i : i + 2]
            if len(bigram) == 2:
                array.append(bigram)

        for i in array:
            if i in dictionary:
                dictionary[i] += 1
            else:
                dictionary[i] = 1

        sorted_dictionary = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
        sorted_dictionary = dict(sorted_dictionary)

        return sorted_dictionary.keys()

    def check_impossible_bigrams(self, text: str):
        for b in self.impossible_bigrams:
            if text.find(b) != -1:
                return False
        return True


with open("02.txt", "r", encoding="utf-8") as file:
    ct_text = file.read()
ap = AffineCipher()
text = "Привет мир"
ct = ap.encrypt(text, 2, 3)
print("Open plain text: "+text+"\nAfter encription:"+ct+"\nAfter decryption:"+ap.decrypt(ct,2,3))
keys = ap.find_keys(ct_text)
print("Possible keys: ", ap.find_keys(ct_text))
print(f"Decrypted text: "+ap.decrypt(ct_text,keys[0][0],keys[0][1]))
