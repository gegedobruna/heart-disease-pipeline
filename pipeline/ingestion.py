import csv
import os

def load_csv(filepath):
    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}")
        return

    with open(filepath, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            clean_row = {}
            for key, value in row.items():
                clean_row[key] = value.strip()
            count += 1
            yield clean_row
        file.close()
        print(f"Loaded {count} rows from {filepath}")

        