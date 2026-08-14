#!/bin/bash
# inspect_csv.sh — quick terminal-based CSV inspection using cat / grep / sed / awk
#
# Usage:
#   ./inspect_csv.sh path/to/file.csv
#
# What it does:
#   1. Prints row + column counts
#   2. Extracts the header row and lists each column on its own line (numbered)
#   3. Greps for columns that look empty across all rows (candidate "research gap" fields)
#   4. Shows a few sample rows
#
# NOTE: this uses sed/awk for a QUICK look only. Because these research CSVs contain
# commas *inside* quoted fields (e.g. "Munda; Ho; Santhal"), the actual import into
# MongoDB is done with Python's csv module (scripts/import_csv.py), which parses quoting
# correctly. Never rely on naive comma-splitting for the real import.

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 path/to/file.csv"
  exit 1
fi

CSV_FILE="$1"

if [ ! -f "$CSV_FILE" ]; then
  echo "File not found: $CSV_FILE"
  exit 1
fi

echo "=== File: $CSV_FILE ==="
echo

TOTAL_LINES=$(wc -l < "$CSV_FILE")
DATA_ROWS=$((TOTAL_LINES - 1))
echo "Total lines: $TOTAL_LINES  (header + $DATA_ROWS data rows, approx — quoted newlines aren't counted here)"
echo

echo "=== Column list (from header row) ==="
# grab header line with cat + head, split on top-level commas is unsafe with quoted commas,
# so we just number-and-print raw header segments for a quick eyeball view
cat "$CSV_FILE" | head -1 | tr ',' '\n' | sed 's/^"//; s/"$//' | nl -ba -w2 -s'. '
echo

echo "=== Column count ==="
cat "$CSV_FILE" | head -1 | tr ',' '\n' | wc -l
echo

echo "=== First 3 data rows (raw) ==="
cat "$CSV_FILE" | sed -n '2,4p'
echo

echo "=== Columns that are entirely empty across sampled rows (candidate gaps) ==="
# crude heuristic: look for ",," patterns column-position-wise is unreliable with quoting,
# so this just flags columns whose header contains "Not analyzed / Not available / Not performed" style values in row 2
sed -n '2p' "$CSV_FILE" | grep -oE 'Not analyzed|Not available|Not performed|Not quantified' | sort | uniq -c || echo "(none found in sampled row)"
