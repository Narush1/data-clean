# Large JSON Streaming Cleaner (Memory-Efficient)

A memory-efficient Python script for cleaning and preprocessing extremely large JSON files (1GB–15GB+ and beyond) without loading the entire dataset into RAM.

This tool is designed for data engineers, analysts, and data scientists who work with raw, messy, and large-scale JSON datasets.

## Features

- Processes massive JSON files (10GB, 15GB, etc.)
- Streaming processing (chunk-by-chunk)
- Low RAM usage (no full file loading)
- Supports:
  - Large JSON arrays `[{}, {}, {}]`
  - NDJSON / JSON Lines format
- Automatic data cleaning:
  - Removes empty rows
  - Removes duplicates
  - Fixes string whitespace
  - Converts numeric fields
  - Detects and parses date/time columns
  - Removes empty columns
- Fault-tolerant (skips broken JSON records)
- Stable for long-running jobs (no memory leaks)

## Installation

Install required dependencies:

```bash
pip install pandas ijson
