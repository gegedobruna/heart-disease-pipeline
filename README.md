# heart-disease-pipeline

Simple data pipeline for heart-disease CSV files.

## Project Structure

- `main.py`: entry point
- `pipeline/`: pipeline logic (ingestion, validation, transform, export, analysis)
- `data/`: sample input files
- `output/`: generated output files

## How To Run

From the project root:

```bash
python main.py --mode full --input data/train.csv --output output
```

## Modes

### 1) `full`
Runs validation + exports CSV files + writes report.

```bash
python main.py --mode full --input data/train.csv --output output
```

### 2) `validate`
Runs validation and exports:
- `output/clean.csv`
- `output/rejected.csv`

```bash
python main.py --mode validate --input data/train.csv --output output
```

### 3) `report`
Runs validation and writes:
- `output/report.txt`

```bash
python main.py --mode report --input data/train.csv --output output
```

## Output Files

- `output/clean.csv`: valid records
- `output/rejected.csv`: invalid records + rejection reasons
- `output/report.txt`: simple summary and pattern report
