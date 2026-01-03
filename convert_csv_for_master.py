import csv
import sys
import os

# Usage: python convert_csv_for_master.py aires.csv > aires_for_master.txt
def convert_csv_for_master(input_csv, output_txt=None):
    source_file = os.path.basename(input_csv)
    with open(input_csv, encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        lines = []
        for row in reader:
            # Remove quotes, join with commas, add source file
            line = ','.join(row) + ',' + source_file
            lines.append(line)
    # Output to file or print
    if output_txt:
        with open(output_txt, 'w', encoding='utf-8') as out:
            for line in lines:
                out.write(line + '\n')
    else:
        for line in lines:
            print(line)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_csv_for_master.py <input_csv> [output_txt]")
    else:
        convert_csv_for_master(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
