# Memory-Efficient Large JSON Cleaner (Streaming)

A professional Python script for cleaning extremely large JSON files (1GB–15GB+ and more) using streaming and chunk-based processing.

This tool does NOT load the entire file into RAM, making it safe for very large datasets.

Designed for:
- Data Engineers
- Data Analysts
- Data Scientists
- ETL pipelines
- Big Data preprocessing

## Key Features

- Handles massive JSON files (10GB, 15GB+)
- Low RAM usage (stream processing)
- Chunk-by-chunk cleaning (stable & safe)
- Supports:
  - Large JSON arrays `[{}, {}, {}]`
  - NDJSON / JSON Lines
- Fault-tolerant (skips broken records)
- Automatic data normalization
- Analysis-ready output JSON

## Why This Script Is Special

Most scripts use:

json.load()

This loads the entire file into memory and crashes on large datasets.

This project uses streaming (ijson) to:
- Read data piece by piece
- Clean in chunks
- Prevent RAM overflow
- Stay stable on long runs

## Installation

Install dependencies:

```bash
pip install pandas ijson
Project Structure
.
├── data_clean.py   # Streaming cleaner script
├── raw.json        # Raw large JSON input
├── clean.json      # Output cleaned JSON
└── README.md
How To Use

Put your raw JSON file in the project folder:

raw.json

Run the script:

python data_clean.py

Cleaned file will be generated:

clean.json
Memory Efficiency

The script processes data in chunks instead of loading everything at once.

Example RAM usage:

1GB file → ~100-200MB RAM

10GB file → ~200-300MB RAM

15GB+ file → Stable (depends on chunk size)

You can control memory usage in the script:

CHUNK_SIZE = 5000

Lower chunk size:

Less RAM usage

Slower processing

Higher chunk size:

Faster processing

More RAM usage

Supported Input Formats
1. Large JSON Array
[
  {"id": 1, "name": "Alice", "value": "100"},
  {"id": 2, "name": "Bob", "value": "200"}
]
2. NDJSON (JSON Lines)
{"id": 1, "name": "Alice", "value": "100"}
{"id": 2, "name": "Bob", "value": "200"}
Cleaning Pipeline

The script automatically:

Flattens nested JSON structures

Removes empty rows

Removes duplicates

Strips whitespace from strings

Converts numeric columns

Parses date/time fields

Removes empty columns

Outputs analysis-ready JSON

Stability & Error Handling

Skips corrupted JSON records

Prevents crashes on invalid lines

Safe chunk clearing (no memory leaks)

Suitable for long-running jobs (hours/days)

Use Cases

Data Cleaning for Machine Learning

Forecasting dataset preparation

Big data preprocessing

ETL pipelines

Log data cleaning

Large dataset normalization

Performance Tip

For VERY large files (10GB+):

CHUNK_SIZE = 1000–3000

This gives maximum stability and low RAM usage.
