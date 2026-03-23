# argument parser for modes and inputs/outputs
import argparse
import os

from pipeline.analysis import generate_insights
from pipeline.exporter import export_clean, export_rejected, write_report
from pipeline.ingestion import load_csv
from pipeline.transformer import decode_record
from pipeline.validation import validate


def parse_args():
    parser = argparse.ArgumentParser(description='Pipeline for processing data')
    parser.add_argument('--input', type=str, default='data/train.csv', help='Input file for preprocess mode')
    parser.add_argument('--output', type=str, default='output/', help='Output directory')
    parser.add_argument('--mode', type=str, choices=['full', 'validate', 'report'], default='full', help='Mode to run the pipeline in')
    parser.add_argument('--log', type=bool, default=False, help='Enable logging for rejection reasons')
    return parser.parse_args()
  
def main():
    args = parse_args()
    seen_ids = set()
    clean_records = []
    rejected_records = []

    for row in load_csv(args.input) or []:
        result = validate(row, seen_ids)
        if result["valid"]:
            clean_records.append(decode_record(result["record"]))
        else:
            rejected_records.append(result)

    if args.mode in ["full", "validate"]:
        export_clean(clean_records, args.output)
        export_rejected(rejected_records, args.output)

    if args.mode in ["full", "report"]:
        insights = generate_insights(clean_records)
        report = {
            "total_rows": len(clean_records) + len(rejected_records),
            "clean_rows": len(clean_records),
            "rejected_rows": len(rejected_records),
        }
        insights.update(report)
        write_report(insights, clean_records, args.output)
    if args.log == True:
        for record in rejected_records:
            print(f"ID: {record['record'].get('id', 'unknown')}, Reasons: {', '.join(record['reasons'])}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Pipeline failed: {e}")
