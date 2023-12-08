def calculate_coincidence_index(text, key_length):
    text = text.upper()  # Перетворюємо весь текст у верхній регістр
    text_len = len(text)
    coincidence_sum = 0

    for shift in range(key_length):
        text_segment = text[shift::key_length]  # Вибираємо літери з однаковою позицією в ключі
        alphabet_counts = [text_segment.count(chr(letter)) for letter in range(1040, 1072)]  # Російський алфавіт

        # Розраховуємо індекс співпадінь для цього сегмента
        segment_length = len(text_segment)
        segment_coincidence = sum(count * (count - 1) for count in alphabet_counts) / (segment_length * (segment_length - 1))

        coincidence_sum += segment_coincidence

    return coincidence_sum / key_length

def main():
    with open(r'C:\Users\Polya\Desktop\KPI\crypto\crypto-23-24\cp2\gogoleva_fb-12_cp2\decode.txt', 'r', encoding='cp1251') as file:
        ciphertext = file.read()

    for key_length in range(1, 36):
        ic = calculate_coincidence_index(ciphertext, key_length)
        print(f"Key Length: {key_length}, Index of Coincidence: {ic}")

if __name__ == '__main__':
    main()
