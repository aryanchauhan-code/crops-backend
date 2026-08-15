"""
bulk_import_all.py — import every CSV/Excel file in a folder into ONE MongoDB collection.

Use this when your files share the same columns (e.g. one file per state, same
schema each time) — which is your case with the 17 fermented-beverages files.
Each row gets tagged with its source filename so you can always trace it back,
even though everything lands in a single queryable collection.

Usage:
    cd backend
    python scripts/bulk_import_all.py /path/to/folder/with/17/files fermented_beverages

    # Dry run first (recommended) -- shows what WOULD happen, inserts nothing:
    python scripts/bulk_import_all.py /path/to/folder fermented_beverages --dry-run

    # Skip files you've already imported (matched by _source_file), safe to re-run:
    python scripts/bulk_import_all.py /path/to/folder fermented_beverages --skip-existing
"""
import argparse
import math
import sys
import time
from pathlib import Path

import pandas as pd
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import settings  # noqa: E402

BATCH_SIZE = 500  # insert_many in chunks -- fast, and keeps memory low for big files


def clean_value(v):
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


def load_data_file(file_path: Path) -> list[dict]:
    """Reads a .csv, .xlsx, or .xls file into a list of dicts. Excel files are
    read sheet by sheet and concatenated -- several of our source files bundle
    multiple states as separate sheets in one workbook, and reading only
    sheet_name=0 silently dropped every sheet after the first. Each row is
    tagged with 'filename::sheetname' so rows stay traceable back to their
    original sheet, not just the workbook."""
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        df = pd.read_csv(file_path, dtype=str)
        df = df.where(pd.notnull(df), None)
        records = df.to_dict(orient="records")
        records = [{k: clean_value(v) for k, v in rec.items()} for rec in records]
        for rec in records:
            rec["_source_file"] = file_path.name
        return records

    if suffix in (".xlsx", ".xls"):
        engine = "openpyxl" if suffix == ".xlsx" else None
        sheets = pd.read_excel(file_path, dtype=str, sheet_name=None, engine=engine)
        records = []
        for sheet_name, df in sheets.items():
            df = df.where(pd.notnull(df), None)
            sheet_records = df.to_dict(orient="records")
            sheet_records = [{k: clean_value(v) for k, v in rec.items()} for rec in sheet_records]
            for rec in sheet_records:
                rec["_source_file"] = f"{file_path.name}::{sheet_name}"
            records.extend(sheet_records)
        return records

    raise ValueError(f"Unsupported file type: {file_path.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", help="Folder containing your 17 data files")
    parser.add_argument("collection", help="Target MongoDB collection name, e.g. fermented_beverages")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be imported, insert nothing")
    parser.add_argument("--skip-existing", action="store_true",
                         help="Skip any file whose filename is already present as _source_file in the collection")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(f"Not a folder: {folder}")
        sys.exit(1)

    data_files = sorted(folder.glob("*.csv")) + sorted(folder.glob("*.xlsx")) + sorted(folder.glob("*.xls"))
    if not data_files:
        print(f"No .csv, .xlsx, or .xls files found in {folder}")
        sys.exit(1)

    print(f"Found {len(data_files)} data file(s) in {folder}")

    client = None
    already_imported = set()
    if not args.dry_run:
        client = MongoClient(settings.mongodb_uri)
        db = client[settings.mongodb_db_name]
        collection = db[args.collection]
        if args.skip_existing:
            already_imported = set(collection.distinct("_source_file"))
            if already_imported:
                print(f"Skipping {len(already_imported)} already-imported file(s): {sorted(already_imported)}")

    start = time.time()
    total_inserted = 0
    total_rows_seen = 0

    for data_path in data_files:
        if data_path.name in already_imported:
            print(f"  SKIP  {data_path.name} (already imported)")
            continue

        records = load_data_file(data_path)
        total_rows_seen += len(records)

        if args.dry_run:
            print(f"  WOULD IMPORT  {data_path.name}  ->  {len(records)} rows")
            continue

        for i in range(0, len(records), BATCH_SIZE):
            batch = records[i:i + BATCH_SIZE]
            collection.insert_many(batch)
            total_inserted += len(batch)

        print(f"  OK  {data_path.name}  ->  {len(records)} rows inserted")

    elapsed = time.time() - start

    if args.dry_run:
        print(f"\nDry run complete. {total_rows_seen} total rows would be inserted across "
              f"{len(data_files)} files. Re-run without --dry-run to actually import.")
    else:
        print(f"\nDone. Inserted {total_inserted} documents into '{args.collection}' "
              f"in {elapsed:.1f}s.")
        client.close()


if __name__ == "__main__":
    main()
