#argument parser for modes and inputs/outputs
import argparse

parser = argparse.ArgumentParser(description='Pipeline for processing data')
parser.add_argument('--input', type=str, default='data/train.csv', help='Input file for preprocess mode')
parser.add_argument('--output', type=str, default='output/', help='Output directory')
parser.add_argument('--mode', type=str, choices=['full', 'validate', 'report'], default='full', help='Mode to run the pipeline in') 
parser.add_argument('--log', type=bool, default=False, help='Enable logging for rejection reasons')    
args = parser.parse_args()

from pipeline.validation import validate
from pipeline.transformer import decode_record
from pipeline.exporter import export_clean, export_rejected
from pipeline.analysis import value_distribution, disease_rate_by_group, age_group_analysis
from pipeline.ingestion import load_csv