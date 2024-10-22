
#hashcat -m 0 -a 3 -o cracked_hashes.txt hashes.txt 89\?d\?d\?d\?d\?d\?d\?d\?d\?d --potfile-disable
#получаем расшифрованные первично номера

f = open("../data/laba3/phones.txt")
phones = []
for i in f.read().split():
    phones.append(int(i))

phones_set = set(phones)

phones_with_salt_a = open("../data/laba3/cracked_hashes.txt").read().split()
phones_with_salt = [int(i[-11:]) for i in phones_with_salt_a]

for k in phones_with_salt:
    counter = 0
    salt = k-phones[4]
    for v in phones_with_salt:
        if v-salt in phones_set:
            counter +=1
    if counter == len(phones):
        break
print(salt)

#87893892

phones_wo_salt = [x - salt for x in phones_with_salt]
with open("../data/laba3/phones_out.txt", 'w') as file:
    lines = []
    for i in range (len(phones_with_salt_a)):
        i_sliced = str(phones_with_salt_a[i])[0:-11]
        lines.append(f"{i_sliced}{phones_wo_salt[i]}\n")
    file.writelines(lines)