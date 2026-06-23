#!/usr/bin/env python3
"""Simple local search for wiki Markdown files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIRS = [ROOT / "wiki"]
ALL_DIRS = [ROOT / "wiki", ROOT / "raw"]
TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".tsv", ".json", ".yaml", ".yml"}


def iter_files(include_raw: bool) -> list[Path]:
    roots = ALL_DIRS if include_raw else DEFAULT_DIRS
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
                files.append(path)
    return sorted(files)


def snippets(text: str, pattern: re.Pattern[str], limit: int) -> list[tuple[int, str]]:
    results: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if pattern.search(line):
            clean = " ".join(line.strip().split())
            results.append((line_number, clean[:220]))
            if len(results) >= limit:
                break
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Search the LLM wiki.")
    parser.add_argument("query", help="Case-insensitive regular expression")
    parser.add_argument("--all", action="store_true", help="include raw text files")
    parser.add_argument("--limit", type=int, default=12, help="maximum files to show")
    parser.add_argument("--snippets", type=int, default=3, help="snippets per file")
    args = parser.parse_args()

    pattern = re.compile(args.query, re.IGNORECASE)
    hits: list[tuple[int, Path, list[tuple[int, str]]]] = []

    for path in iter_files(args.all):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        count = len(pattern.findall(text))
        if count:
            hits.append((count, path, snippets(text, pattern, args.snippets)))

    hits.sort(key=lambda item: (-item[0], item[1].as_posix()))

    for count, path, lines in hits[: args.limit]:
        rel = path.relative_to(ROOT).as_posix()
        print(f"{rel} ({count} match{'es' if count != 1 else ''})")
        for line_number, snippet in lines:
            print(f"  {line_number}: {snippet}")

    if not hits:
        print("No matches.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

