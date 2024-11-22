import os
import time
import hashlib
import random
import string
#hashcat -m 0 -a 3 -o cracked_hashes.txt hashes.txt 89\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d --potfile-disable
def clean(input_file, output_file):
    with open(input_file, "r") as infile:
        with open(output_file, "w") as outfile:
            for line in infile:
                cleaned_line = ''.join(ch for ch in line if ch.isprintable())
                outfile.write(cleaned_line + "\n")
def remove_duplicates(input_file, output_file):
    unique_lines = set()
    with open(input_file, "r") as infile:
        for line in infile:
            cleaned_line = ''.join(ch for ch in line if ch.isprintable())
            unique_lines.add(cleaned_line.strip())
    with open(output_file, "w") as outfile:
        for line in unique_lines:
            outfile.write(line + "\n")
def found_salt(phones, phones_with_salt):
    salt = 0
    for k in phones_with_salt:
        phones_set = set(phones)
        counter = 0
        salt = k-phones[2]
        for v in phones_with_salt:
            if v-salt in phones_set:
                counter +=1
        if counter == len(phones):
            break
    return salt
def test_salt_effectiveness(phones_wo_salt, salt):
    salt_types = ['numeric', 'alphabetic', 'mixed']
    salt_lengths = range(5, 7)

    times_per_salt = {}

    for salt_type in salt_types:
        for length in salt_lengths:
            test_salt = generate_salt(salt_type, length)

            with open("../data/laba3/sha1_test_hashes.txt", 'w') as sha1_file, \
                 open("../data/laba3/sha256_test_hashes.txt", 'w') as sha256_file, \
                 open("../data/laba3/sha3_test_hashes.txt", 'w') as sha3_file:

                for x in phones_wo_salt:
                    sha1_file.write(hashlib.sha1((str(x) + str(test_salt)).encode()).hexdigest() + "\n")
                    sha256_file.write(hashlib.sha256((str(x) + str(test_salt)).encode()).hexdigest() + "\n")
                    sha3_file.write(hashlib.sha3_256((str(x) + str(test_salt)).encode()).hexdigest() + "\n")

            sha1_start_time = time.time()
            os.system('hashcat -m 100 -a 3 -o ../data/laba3/cracked_sha1_test_hashes.txt ../data/laba3/sha1_test_hashes.txt 89\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d --potfile-disable')
            sha1_end_time = time.time()

            sha256_start_time = time.time()
            os.system('hashcat -m 1400 -a 3 -o ../data/laba3/cracked_sha256_test_hashes.txt ../data/laba3/sha256_test_hashes.txt 89\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d --potfile-disable')
            sha256_end_time = time.time()

            sha3_start_time = time.time()
            os.system('hashcat -m 17400 -a 3 -o ../data/laba3/cracked_sha3_test_hashes.txt ../data/laba3/sha3_test_hashes.txt 89\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d --potfile-disable')
            sha3_end_time = time.time()

            times_per_salt[f"{salt_type}_{length}"] = {
                "SHA-1": sha1_end_time - sha1_start_time,
                "SHA-256": sha256_end_time - sha256_start_time,
                "SHA-3": sha3_end_time - sha3_start_time
            }

    return times_per_salt
def display_test_results(results):
    print("\nРезультаты тестирования:\n")
    print(f"{'Тип соли':<15}{'Длина соли':<15}{'SHA-1 (сек.)':<15}{'SHA-256 (сек.)':<15}{'SHA-3 (сек.)':<15}")
    print("-" * 75)

    for salt_key, times in results.items():
        salt_type, salt_length = salt_key.split("_")
        sha1_time = times["SHA-1"]
        sha256_time = times["SHA-256"]
        sha3_time = times["SHA-3"]
        print(f"{salt_type:<15}{salt_length:<15}{sha1_time:<15.6f}{sha256_time:<15.6f}{sha3_time:<15.6f}")
def generate_salt(salt_type, length):
    if salt_type == 'numeric':
        return ''.join(random.choices(string.digits, k=length))
    elif salt_type == 'alphabetic':
        return ''.join(random.choices(string.ascii_letters, k=length))
    elif salt_type == 'mixed':
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



f = open("../data/laba3/phones.txt")
phones = []
for i in f.read().split():
    phones.append(int(i))
f.close()

with open("../data/laba3/cracked_sha1_hashes.txt", 'w') as file:
    pass
with open("../data/laba3/cracked_sha256_hashes.txt", 'w') as file:
    pass
with open("../data/laba3/cracked_sha3_hashes.txt", 'w') as file:
    pass
with open("../data/laba3/cracked_hashes.txt", 'w') as file:
    pass



main_start_time = time.time()
os.system('hashcat -m 0 -a 3 -o ../data/laba3/cracked_hashes.txt ../data/laba3/hashes.txt 89\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d --potfile-disable')
main_end_time = time.time()

phones_with_salt_a = open("../data/laba3/cracked_hashes.txt").read().split()
phones_with_salt = [int(i[-11:]) for i in phones_with_salt_a]
salt = found_salt(phones, phones_with_salt)
main2_end_time = time.time()
phones_wo_salt = [x - salt for x in phones_with_salt]
with open("../data/laba3/phones_out.txt", 'w') as file:
    lines = []
    for i in range (len(phones_with_salt_a)):
        i_sliced = str(phones_with_salt_a[i])[0:-11]
        lines.append(f"{i_sliced}{phones_wo_salt[i]}\n") #запись соответствующих хешей и соответствующих им деобезличеннх номеров
    file.writelines(lines)
main3_end_time = time.time()




with open("../data/laba3/sha1_hashes.txt", 'w') as file:
    pass
    for x in phones_wo_salt:
        hash = hashlib.sha1((str(x+salt)).encode()).hexdigest()
        file.write(hash + "\n")

with open("../data/laba3/sha256_hashes.txt", 'w') as file:
    pass
    for x in phones_wo_salt:
        hash = hashlib.sha256((str(x+salt)).encode()).hexdigest()
        file.write(hash + "\n")

with open("../data/laba3/sha3_hashes.txt", 'w') as file:
    pass
    for x in phones_wo_salt:
        hash = hashlib.sha3_256((str(x+salt)).encode()).hexdigest()
        file.write(hash + "\n")


sha1_start_time = time.time()
os.system('hashcat -m 100 -a 3 -o ../data/laba3/cracked_sha1_hashes.txt ../data/laba3/sha1_hashes.txt 89\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d --potfile-disable')
sha1_end_time = time.time()

sha256_start_time = time.time()
os.system('hashcat -m 1400 -a 3 -o ../data/laba3/cracked_sha256_hashes.txt ../data/laba3/sha256_hashes.txt 89\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d --potfile-disable')
sha256_end_time = time.time()

sha3_start_time = time.time()
os.system('hashcat -m 17400 -a 3 -o ../data/laba3/cracked_sha3_hashes.txt ../data/laba3/sha3_hashes.txt 89\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d\\?d --potfile-disable')
sha3_end_time = time.time()




test_results = test_salt_effectiveness(phones_wo_salt, salt)
print("Найденная соль: " + str(salt))
print(f"Время расшифровки исходного датасета: {main_end_time - main_start_time:.6f} секунд")
print(f"Время расшифровки исходного датасета и вычисления соли: {main2_end_time - main_start_time:.6f} секунд")
print(f"Время вычисления соли: {main2_end_time - main_end_time:.6f} секунд")
print(f"Время нахождения деобезличенного датасета: {main3_end_time - main2_end_time:.6f} секунд")

print(f"Время расшифровки sha1 датасета и вычисления соли: {sha1_end_time - sha1_start_time:.6f} секунд")
print(f"Время расшифровки sha256 датасета и вычисления соли: {sha256_end_time - sha256_start_time:.6f} секунд")
print(f"Время расшифровки sha3 датасета и вычисления соли: {sha3_end_time - sha3_start_time:.6f} секунд")
display_test_results(test_results)