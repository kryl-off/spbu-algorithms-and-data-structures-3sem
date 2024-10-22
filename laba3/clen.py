def remove_duplicates(input_file, output_file):
    unique_lines = set()
    with open(input_file, "r") as infile:
        for line in infile:
            unique_lines.add(line.strip())
    with open(output_file, "w") as outfile:
        for line in unique_lines:
            outfile.write(line + "\n")

input_file = "../data/laba3/orig_cracked_hashes.txt"
output_file = "../data/laba3/cracked_hashes.txt"

remove_duplicates(input_file, output_file)