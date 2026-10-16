#!/usr/bin/env python3
"""Summarize a CSV input's structure without fitting a model or interpreting results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_csv(path: Path) -> dict[str, Any]:
    columns: list[str] = []
    missing_counts: dict[str, int] = {}
    row_count = 0

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Input CSV is empty or has no header row.")

        columns = list(reader.fieldnames)
        if not columns or any(name is None or not name.strip() for name in columns):
            raise ValueError("Every column must have a non-empty header.")
        if len(set(columns)) != len(columns):
            raise ValueError("Duplicate column names were found.")

        missing_counts = {name: 0 for name in columns}
        for row in reader:
            row_count += 1
            for name in columns:
                value = row.get(name)
                if value is None or not value.strip():
                    missing_counts[name] += 1

    return {
        "input_file": str(path),
        "input_sha256": sha256_file(path),
        "row_count": row_count,
        "column_count": len(columns),
        "columns": columns,
        "blank_or_missing_cells_by_column": missing_counts,
        "note": "Structural audit only; no modeling or biological interpretation was performed.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write a reproducible structural audit of a CSV file."
    )
    parser.add_argument("input_csv", type=Path, help="Path to the input CSV file.")
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("outputs"),
        help="Directory for the JSON audit report (default: outputs).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = args.input_csv.expanduser().resolve()
    if not input_path.is_file():
        raise SystemExit(f"Input file does not exist: {input_path}")

    try:
        report = audit_csv(input_path)
    except (UnicodeDecodeError, csv.Error, ValueError) as error:
        raise SystemExit(f"Could not audit CSV: {error}") from error

    args.outdir.mkdir(parents=True, exist_ok=True)
    output_path = args.outdir / "input_audit.json"
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote structural audit: {output_path.resolve()}")


if __name__ == "__main__":
    main()
