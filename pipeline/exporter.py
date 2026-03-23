import csv
import os
from datetime import datetime
from pipeline.schema import SCHEMA
from pipeline.analysis import field_summary, value_distribution


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


def write_report(insights, records, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, "report.txt")

    with open(filepath, "w", encoding="utf-8") as f:

    # timestamp
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 50 + "\n\n")
    
        # section 1: pipeline summary
        f.write("SECTION 1: PIPELINE SUMMARY\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total rows processed: {insights['total_rows']}\n")
        f.write(f"Clean rows: {insights['clean_rows']}\n")
        f.write(f"Rejected rows: {insights['rejected_rows']}\n")
        f.write("\n")
    
        # section 2: field summaries
        f.write("SECTION 2: FIELD SUMMARIES\n")
        f.write("-" * 50 + "\n")
    
        numeric_fields = ["Age", "BP", "Cholesterol", "Max HR", "ST depression"]
        for field in numeric_fields:
            summary = field_summary(records, field)
            mean_value = "n/a" if summary["mean"] is None else round(summary["mean"], 2)
            median_value = "n/a" if summary["median"] is None else round(summary["median"], 2)
            std_value = "n/a" if summary["std_dev"] is None else round(summary["std_dev"], 2)
            f.write(f"{field}:\n")
            f.write(f"  mean:    {mean_value}\n")
            f.write(f"  median:  {median_value}\n")
            f.write(f"  std_dev: {std_value}\n")
            f.write("\n")
    
        categorical_fields = ["Sex", "Chest pain type", "Heart Disease"]
        for field in categorical_fields:
            values = [row.get(field) for row in records]
            dist = value_distribution(values)
            f.write(f"{field} distribution:\n")
            for value, stats in dist.items():
                f.write(f"  {value}: {stats['count']} ({stats['pct']}%)\n")
            f.write("\n")
    
        # section 3: patterns
        f.write("SECTION 3: PATTERNS\n")
        f.write("-" * 50 + "\n")
    
        sex_data = insights.get("disease_by_sex", {})
        sex_decode = SCHEMA.get("Sex", {}).get("decode", {})
        for sex, stats in sex_data.items():
            label = sex_decode.get(sex, sex_decode.get(str(sex), str(sex)))
            f.write(f"{str(label).capitalize()} patients have a heart disease rate of {stats['rate']}%.\n")
    
        f.write("\n")
    
        chest_data = insights.get("disease_by_chest_pain", {})
        chest_decode = SCHEMA.get("Chest pain type", {}).get("decode", {})
        for cp, stats in chest_data.items():
            cp_label = chest_decode.get(cp, chest_decode.get(str(cp), str(cp)))
            f.write(f"Chest pain type {cp_label} has a heart disease rate of {stats['rate']}%.\n")
    
        f.write("\n")
    
        age_data = insights.get("disease_by_age", {})
        f.write("Heart disease rate by age group:\n")
        for age_group, stats in sorted(age_data.items()):
            f.write(f"  Age {age_group}: {stats['rate']}%\n")

        print(f"Wrote report to {filepath}")


if __name__ == "__main__":
    from pipeline.ingestion import load_csv
    from pipeline.validation import validate
    from pipeline.analysis import generate_insights

    seen = set()
    records = []
    rejected = 0

    for row in load_csv("data/train.csv"):
        result = validate(row, seen)
        if result["valid"]:
            records.append(result["record"])
        else:
            rejected += 1

    insights = generate_insights(records)
    insights["total_rows"] = len(records) + rejected
    insights["clean_rows"] = len(records)
    insights["rejected_rows"] = rejected

    write_report(insights, records, "output")
