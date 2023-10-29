from lab3_math import compute_entropy
import csv


ALPHA = "абвгдежзийклмнопрстуфхцчшщьыэюя"
MOST_COMMON_BIGR_IN_LANG = ['ст', 'но', 'то', 'на', 'ен']


def get_lang_bigr_entropy() -> float:
    result = dict()
    with open("stats/lab1_bigram_with_interceptions_in_text_without_spaces.csv", "r", encoding="utf-8") as csv_f:
        for r in csv.reader(csv_f):
            if r[0] == "*":
                continue
            
            for a in ALPHA:
                if (r[ALPHA.index(a) + 1]) == '-':
                    continue

                result.update({r[0] + a: float(r[ALPHA.index(a) + 1])})
    
    return compute_entropy(2, result)


def freq_count(text: str, n: int, ngr_intercept=False) -> dict[str: float]:
    step = 1 if ngr_intercept else n
    ngr_dict = {}
    
    for i in range(0, len(text) - n, step):
        if not text[i: i + n]:
            continue

        if text[i: i + n] not in ngr_dict.keys():
            ngr_dict.update({text[i: i + n]: 1})
        else:
            ngr_dict[text[i: i + n]] += 1

    return {i: ngr_dict[i] / sum(ngr_dict.values()) for i in sorted(ngr_dict.keys())}


def text_analysis(text: str) -> tuple[float, float, float]:
    lang_bigr_entropy = get_lang_bigr_entropy()
    freq_dict = freq_count(text, 2, False)

    most_common = {k: v for k, v in sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[0:15]}

    entropy = compute_entropy(2, freq_dict)

    c_koef = len(set(most_common.keys()).intersection(set(MOST_COMMON_BIGR_IN_LANG)))/len(set(MOST_COMMON_BIGR_IN_LANG))

    return entropy, lang_bigr_entropy, c_koef
