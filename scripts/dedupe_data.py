"""
dedupe_data.py — resolves duplicate records found by verify_data.py.
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

from bson import ObjectId
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import settings  # noqa: E402


def fill_score(doc: dict) -> int:
    return sum(1 for k, v in doc.items() if k not in ("_id",) and v not in (None, ""))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("collection", nargs="?", default="fermented_beverages")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--auto", action="store_true")
    args = parser.parse_args()

    client = MongoClient(settings.mongodb_uri)
    db = client[settings.mongodb_db_name]
    collection = db[args.collection]

    docs = list(collection.find({}))

    groups = defaultdict(list)
    for doc in docs:
        name = (doc.get("Beverage Name") or "").strip().lower()
        region = (doc.get("Region / State (typical)") or "").strip().lower()
        if name:
            groups[(name, region)].append(doc)

    duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}

    if not duplicate_groups:
        print("No duplicate groups found. Nothing to do.")
        client.close()
        return

    print(f"Found {len(duplicate_groups)} duplicate group(s) across {sum(len(v) for v in duplicate_groups.values())} records.\n")
    total_deleted = 0

    for (name, region), group_docs in duplicate_groups.items():
        ranked = sorted(group_docs, key=fill_score, reverse=True)
        keeper = ranked[0]
        to_delete = ranked[1:]

        print(f"--- '{name}' in '{region or 'unspecified region'}' ({len(group_docs)} copies) ---")
        for doc in ranked:
            marker = "KEEP" if doc is keeper else "DELETE"
            source = doc.get("_source_file", "no source file")
            print(f"  [{marker:>6}]  fields filled: {fill_score(doc):>3}   source: {source}   id: {doc['_id']}")

        if args.dry_run:
            print("  (dry run -- nothing deleted)\n")
            continue

        if not args.auto:
            answer = input(f"  Delete the {len(to_delete)} lower-quality copy(ies) shown above? (y/N/skip): ").strip().lower()
            if answer != "y":
                print("  Skipped.\n")
                continue

        ids_to_delete = [ObjectId(doc["_id"]) for doc in to_delete]
        result = collection.delete_many({"_id": {"$in": ids_to_delete}})
        total_deleted += result.deleted_count
        print(f"  Deleted {result.deleted_count} record(s).\n")

    if args.dry_run:
        print("Dry run complete -- re-run without --dry-run to actually clean these up.")
    else:
        print(f"Done. Deleted {total_deleted} duplicate record(s) total.")

    client.close()


if __name__ == "__main__":
    main()
