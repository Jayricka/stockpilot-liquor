
#!/usr/bin/env python3
"""Safely rename StockSafi branding to StockSafi."""

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = {
    "StockSafi": "StockSafi",
    "stocksafi": "stocksafi",
    "STOCKSAFI": "STOCKSAFI",
}

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "myenv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".next",
}

EXCLUDED_FILES = {
    "db.sqlite3",
}

EXCLUDED_PARTS = {
    "migrations",
}


def get_files():
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "-co",
            "--exclude-standard",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    files = []

    for name in result.stdout.splitlines():
        path = ROOT / name

        if not path.is_file():
            continue

        if EXCLUDED_DIRS.intersection(path.parts):
            continue

        if EXCLUDED_PARTS.intersection(path.parts):
            continue

        if path.name in EXCLUDED_FILES:
            continue

        if path.name.endswith((".lock", ".map", ".pyc")):
            continue

        files.append(path)

    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write replacements to files.",
    )
    args = parser.parse_args()

    changed_files = 0
    total_replacements = 0

    for path in get_files():
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        updated = original

        for old, new in REPLACEMENTS.items():
            updated = updated.replace(old, new)

        if updated == original:
            continue

        count = sum(
            original.count(old)
            for old in REPLACEMENTS
        )

        print(f"{path.relative_to(ROOT)}: {count} replacement(s)")

        changed_files += 1
        total_replacements += count

        if args.apply:
            path.write_text(
                updated,
                encoding="utf-8",
                newline="",
            )

    action = "Updated" if args.apply else "Found"

    print(
        f"\n{action} {total_replacements} occurrence(s) "
        f"across {changed_files} file(s)."
    )

    if not args.apply:
        print("Dry run only. Add --apply to make changes.")


if __name__ == "__main__":
    main()
