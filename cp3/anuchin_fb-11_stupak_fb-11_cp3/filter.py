# Открываем файл на чтение
with open('keys.txt', 'r') as file:
    # Создаем список для хранения отфильтрованных строк
    filtered_lines = []

    # Идем по строкам файла
    for line in file:
        # Используем регулярные выражения для поиска чисел в строке
        import re

        a_match = re.search(r'a=\[(\d+)\]', line)
        b_match = re.search(r'b=\[(\d+)\]', line)

        # Проверяем, что удалось извлечь значения a и b из строки
        if a_match and b_match:
            a_value = int(a_match.group(1))
            b_value = int(b_match.group(1))

            # Проверяем условие фильтрации (например, a > 500 и b > 500)
            if a_value < 1000 and b_value < 1000:
                filtered_lines.append(line)

# Открываем файл на запись и записываем отфильтрованные строки
with open('filtered.txt', 'w') as output_file:
    output_file.writelines(filtered_lines)

print("Файл успешно отфильтрован.")
