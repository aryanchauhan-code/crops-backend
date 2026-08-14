"""
import_csv.py — load one of your 17 CSV files into a MongoDB Atlas collection.

Usage:
    cd backend
    python scripts/import_csv.py ../sample_data/fermented_beverages.csv fermented_beverages
    python scripts/import_csv.py path/to/crops_by_state.csv crops_by_state

Each CSV file becomes its own collection. Run this once per file for all 17.
Requires .env in backend/ with MONGODB_URI set (see .env.example).
"""
import sys
import math
from pathlib import Path

import pandas as pd
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import settings  # noqa: E402


def clean_value(v):
    """NaN -> None so MongoDB stores proper nulls instead of the string 'nan'."""
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    collection_name = sys.argv[2]

    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        sys.exit(1)

    print(f"Reading {csv_path} ...")
    df = pd.read_csv(csv_path, dtype=str)  # read everything as string first, safest for messy research data
    df = df.where(pd.notnull(df), None)

    records = df.to_dict(orient="records")
    records = [{k: clean_value(v) for k, v in rec.items()} for rec in records]

    print(f"Parsed {len(records)} rows, {len(df.columns)} columns.")
    print("Columns:", list(df.columns))

    client = MongoClient(settings.mongodb_uri)
    db = client[settings.mongodb_db_name]
    collection = db[collection_name]

    if records:
        result = collection.insert_many(records)
        print(f"Inserted {len(result.inserted_ids)} documents into '{collection_name}' "
              f"in database '{settings.mongodb_db_name}'.")
    else:
        print("No rows found to insert.")

    client.close()


if __name__ == "__main__":
    main()
