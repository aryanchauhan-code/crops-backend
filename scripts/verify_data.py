"""
verify_data.py — sanity-checks what's actually in MongoDB against what you imported.
"""
import sys
from collections import Counter, defaultdict
from pathlib import Path

from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import settings  # noqa: E402

SPARSE_THRESHOLD = 0.15


def main():
    collection_name = sys.argv[1] if len(sys.argv) > 1 else "fermented_beverages"

    client = MongoClient(settings.mongodb_uri)
    db = client[settings.mongodb_db_name]
    collection = db[collection_name]

    docs = list(collection.find({}))
    total = len(docs)
    print(f"=== {collection_name}: {total} total documents ===\n")

    by_source = Counter(doc.get("_source_file", "(no source file / manually added)") for doc in docs)
    print("--- Records per source file ---")
    for source, count in sorted(by_source.items()):
        print(f"  {count:>4}  {source}")
    print()

    no_source = by_source.get("(no source file / manually added)", 0)
    if no_source:
        print(f"Note: {no_source} record(s) have no _source_file -- seeded/manual records, not an error.\n")

    print("--- Sparse records (< 15% of fields filled in) ---")
    sparse_by_source = defaultdict(int)
    sparse_count = 0
    for doc in docs:
        fields = {k: v for k, v in doc.items() if k not in ("_id", "_source_file")}
        if not fields:
            continue
        filled = sum(1 for v in fields.values() if v not in (None, ""))
        fill_rate = filled / len(fields)
        if fill_rate < SPARSE_THRESHOLD:
            sparse_count += 1
            sparse_by_source[doc.get("_source_file", "unknown")] += 1

    if sparse_count:
        print(f"  {sparse_count} of {total} records are mostly empty (only a few columns filled).")
        print("  By source file:")
        for source, count in sorted(sparse_by_source.items(), key=lambda x: -x[1]):
            print(f"    {count:>4}  {source}")
    else:
        print("  None found -- every record has reasonable field coverage.")
    print()

    print("--- Possible duplicate records (same Beverage Name + Region/State) ---")
    key_counter = Counter()
    for doc in docs:
        name = (doc.get("Beverage Name") or "").strip().lower()
        region = (doc.get("Region / State (typical)") or "").strip().lower()
        if name:
            key_counter[(name, region)] += 1

    duplicates = {k: v for k, v in key_counter.items() if v > 1}
    if duplicates:
        for (name, region), count in sorted(duplicates.items(), key=lambda x: -x[1]):
            print(f"  x{count}  '{name}' in '{region or 'unspecified region'}'")
    else:
        print("  None found.")
    print()

    print("=== Summary ===")
    print(f"Total records: {total}")
    print(f"Source files represented: {len([s for s in by_source if s != '(no source file / manually added)'])}")
    print(f"Sparse records: {sparse_count}")
    print(f"Possible duplicate groups: {len(duplicates)}")

    client.close()


if __name__ == "__main__":
    main()
