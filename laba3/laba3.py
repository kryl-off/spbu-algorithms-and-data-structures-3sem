import itertools
import string



def clean_wordlist(input_file, output_file):
    with open(input_file, 'r', encoding='utf-16') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Удаляем лишние пробелы и не отображаемые символы
            cleaned_line = line.strip()  # Убираем пробелы и символы новой строки в начале и конце
            if cleaned_line:  # Если строка не пустая после очистки
                outfile.write(cleaned_line + '\n')  # Записываем её в файл

# Пример использования
clean_wordlist('../data/laba3/hashes.txt', '../data/laba3/clean_hashes.txt')
print("Очистка завершена.")