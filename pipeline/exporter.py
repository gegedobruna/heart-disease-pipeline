import csv
import os

from pipeline.schema import SCHEMA


def clean_headers():
    headers = []
    for field, rules in SCHEMA.items():
        headers.append(field)
        if "decode" in rules:
            headers.append(f"{field}_label")
    return headers


def export_clean(records, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "clean.csv")
    headers = clean_headers()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in records:
            writer.writerow(row)


def export_rejected(records, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "rejected.csv")
    headers = list(SCHEMA.keys()) + ["rejection_reasons"]

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for item in records:
            row = dict(item.get("record", {}))
            reasons = item.get("reasons", [])
            row["rejection_reasons"] = " / ".join(str(r) for r in reasons)
            writer.writerow(row)