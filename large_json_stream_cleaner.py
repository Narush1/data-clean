import ijson
import json
import pandas as pd
from pathlib import Path


# Number of records processed per chunk (lower = less RAM usage)
CHUNK_SIZE = 5000


def detect_json_type(file_path):
    # Detect if JSON is an array or NDJSON (json lines)
    with open(file_path, "rb") as f:
        first_char = f.read(1).strip()
        if first_char == b"[":
            return "array"
        return "ndjson"


def stream_json_array(file_path):
    # Stream large JSON array without loading entire file into memory
    with open(file_path, "rb") as f:
        objects = ijson.items(f, "item")
        for obj in objects:
            yield obj


def stream_ndjson(file_path):
    # Stream JSON lines (one JSON object per line)
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    # Skip broken lines instead of crashing
                    continue


def clean_chunk(df: pd.DataFrame) -> pd.DataFrame:
    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicates inside chunk
    df = df.drop_duplicates()

    # Strip whitespace from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Replace empty strings with proper null values
    df = df.replace("", pd.NA)

    # Attempt numeric conversion safely
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass

    # Attempt date parsing for likely date/time columns
    for col in df.columns:
        col_lower = col.lower()
        if "date" in col_lower or "time" in col_lower:
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass

    # Remove fully empty columns
    df = df.dropna(axis=1, how="all")

    return df


def write_chunk(output_file, records, is_first_chunk):
    # Write chunk safely to output JSON without loading everything in RAM
    mode = "w" if is_first_chunk else "a"

    with open(output_file, mode, encoding="utf-8") as f:
        if is_first_chunk:
            f.write("[\n")
        else:
            f.write(",\n")

        json.dump(records, f, ensure_ascii=False, indent=2)


def finalize_json(output_file):
    # Close JSON array properly
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n]")


def process_large_json(input_path, output_path):
    # Main memory-efficient processing pipeline
    json_type = detect_json_type(input_path)

    # Choose correct streaming method
    if json_type == "array":
        stream = stream_json_array(input_path)
        print("Detected large JSON array format")
    else:
        stream = stream_ndjson(input_path)
        print("Detected NDJSON (JSON Lines) format")

    chunk = []
    chunk_count = 0
    total_processed = 0
    first_chunk = True

    for record in stream:
        chunk.append(record)

        # Process data in chunks to prevent high RAM usage
        if len(chunk) >= CHUNK_SIZE:
            df = pd.json_normalize(chunk)
            df = clean_chunk(df)

            clean_records = df.to_dict(orient="records")
            write_chunk(output_path, clean_records, first_chunk)

            first_chunk = False
            total_processed += len(chunk)
            chunk_count += 1

            print(f"Processed chunk {chunk_count}, total records: {total_processed}")

            # Clear chunk from memory
            chunk.clear()

    # Process remaining records
    if chunk:
        df = pd.json_normalize(chunk)
        df = clean_chunk(df)

        clean_records = df.to_dict(orient="records")
        write_chunk(output_path, clean_records, first_chunk)

        total_processed += len(chunk)
        print(f"Processed final chunk, total records: {total_processed}")

    # Finalize JSON structure
    finalize_json(output_path)

    print("Cleaning completed successfully!")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    # Path to large raw JSON file (can be 1GB, 10GB, 15GB+)
    input_file = "raw.json"

    # Output cleaned JSON file (analysis-ready)
    output_file = "clean.json"

    # Run memory-efficient cleaning
    process_large_json(input_file, output_file)
