import collections
import math


def compute_frequencies(text):
    total = len(text)
    freqs = collections.Counter(text)
    for key in freqs:
        freqs[key] /= total
    return freqs


def compute_bigram_frequencies(text, allow_repeats=True):
    bigrams = [text[i:i+2] for i in range(len(text) - 1) if allow_repeats or text[i] != text[i+1]]
    total = len(bigrams)
    freqs = collections.Counter(bigrams)
    for key in freqs:
        freqs[key] /= total
    return freqs


def compute_entropy(freqs):
    return -sum([p * math.log2(p) for p in freqs.values()])


def save_to_txt(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")


def compute_redundancy(H, m):
    H0 = math.log2(m)
    return 1 - H/H0


def main():
    with open("avidreaders.ru__kobzar.txt", "r", encoding="utf-8") as f:
        text = f.read().lower().replace(" ", "_")  # Replacing spaces with "_"

    filtered_text = ''.join([char for char in text if 'а' <= char <= 'я' or char == "_"])

    # Compute letter frequencies
    letter_freqs = compute_frequencies(filtered_text)
    save_to_txt("letter_frequencies.txt", letter_freqs)

    # Compute bigram frequencies (with and without repeats)
    bigram_freqs = compute_bigram_frequencies(filtered_text)
    save_to_txt("bigram_frequencies_with_repeats.txt", bigram_freqs)

    bigram_freqs_no_repeats = compute_bigram_frequencies(filtered_text, allow_repeats=False)
    save_to_txt("bigram_frequencies_without_repeats.txt", bigram_freqs_no_repeats)

    # Compute H values
    H1 = compute_entropy(letter_freqs)
    H2 = compute_entropy(bigram_freqs) / 2
    H2_no_repeats = compute_entropy(bigram_freqs_no_repeats) / 2

    # Remove underscores (previously spaces) and repeat
    text_without_underscores = filtered_text.replace("_", "")

    letter_freqs_no_underscores = compute_frequencies(text_without_underscores)
    save_to_txt("letter_frequencies_no_underscores.txt", letter_freqs_no_underscores)

    bigram_freqs_no_underscores = compute_bigram_frequencies(text_without_underscores)
    save_to_txt("bigram_frequencies_with_repeats_no_underscores.txt", bigram_freqs_no_underscores)

    bigram_freqs_no_repeats_no_underscores = compute_bigram_frequencies(text_without_underscores, allow_repeats=False)
    save_to_txt("bigram_frequencies_without_repeats_no_underscores.txt", bigram_freqs_no_repeats_no_underscores)

    H1_no_underscores = compute_entropy(letter_freqs_no_underscores)
    H2_no_underscores = compute_entropy(bigram_freqs_no_underscores) / 2
    H2_no_repeats_no_underscores = compute_entropy(bigram_freqs_no_repeats_no_underscores) / 2

    # Calculate redundancies
    m = len(set(filtered_text))
    R1 = compute_redundancy(H1, m)
    R2 = compute_redundancy(H2, m)
    R2_no_repeats = compute_redundancy(H2_no_repeats, m)

    m_no_underscores = len(set(text_without_underscores))
    R1_no_underscores = compute_redundancy(H1_no_underscores, m_no_underscores)
    R2_no_underscores = compute_redundancy(H2_no_underscores, m_no_underscores)
    R2_no_repeats_no_underscores = compute_redundancy(H2_no_repeats_no_underscores, m_no_underscores)

    # Save the entropy and redundancy values to a txt file
    with open("entropy_and_redundancy_values.txt", "w", encoding="utf-8") as f:
        f.write(f"H1: {H1}\n")
        f.write(f"H2: {H2}\n")
        f.write(f"H2 (no repeats): {H2_no_repeats}\n")
        f.write(f"H1 (no underscores): {H1_no_underscores}\n")
        f.write(f"H2 (no underscores): {H2_no_underscores}\n")
        f.write(f"H2 (no repeats, no underscores): {H2_no_repeats_no_underscores}\n")
        f.write(f"R1: {R1}\n")
        f.write(f"R2: {R2}\n")
        f.write(f"R2 (no repeats): {R2_no_repeats}\n")
        f.write(f"R1 (no underscores): {R1_no_underscores}\n")
        f.write(f"R2 (no underscores): {R2_no_underscores}\n")
        f.write(f"R2 (no repeats, no underscores): {R2_no_repeats_no_underscores}\n")

    # Print the values
    print(f"H1: {H1}")
    print(f"H2: {H2}")
    print(f"H2 (no repeats): {H2_no_repeats}")
    print(f"H1 (no underscores): {H1_no_underscores}")
    print(f"H2 (no underscores): {H2_no_underscores}")
    print(f"H2 (no repeats, no underscores): {H2_no_repeats_no_underscores}")
    print(f"R1: {R1}")
    print(f"R2: {R2}")
    print(f"R2 (no repeats): {R2_no_repeats}")
    print(f"R1 (no underscores): {R1_no_underscores}")
    print(f"R2 (no underscores): {R2_no_underscores}")
    print(f"R2 (no repeats, no underscores): {R2_no_repeats_no_underscores}")

if __name__ == "__main__":
    main()
