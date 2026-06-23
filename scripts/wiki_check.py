#!/usr/bin/env python3
"""Dependency-free health checks for the LLM wiki."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
INDEX = WIKI / "index.md"
LOG = WIKI / "log.md"

WIKILINK_RE = re.compile(r"!\[\[[^\]]+\]\]|\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
LOG_HEADING_RE = re.compile(r"^## \[\d{4}-\d{2}-\d{2}\] (ingest|query|lint|schema|maintenance) \| .+")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def wiki_pages() -> list[Path]:
    return sorted(p for p in WIKI.rglob("*.md") if p.is_file())


def content_pages() -> list[Path]:
    excluded = {WIKI / "README.md", INDEX, LOG}
    return [p for p in wiki_pages() if p not in excluded]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_frontmatter(text: str) -> bool:
    return bool(FRONTMATTER_RE.match(text))


def parse_wikilinks(text: str) -> list[str]:
    links: list[str] = []
    for match in WIKILINK_RE.finditer(text):
        target = match.group(1)
        if target:
            links.append(target.strip())
    return links


def parse_markdown_links(text: str) -> list[str]:
    return [m.group(1).split("#", 1)[0] for m in MD_LINK_RE.finditer(text)]


def resolve_wikilink(target: str, page: Path, all_pages: list[Path]) -> Path | None:
    clean = target.strip().split("#", 1)[0]
    if not clean:
        return None
    if not clean.endswith(".md"):
        clean = f"{clean}.md"

    direct = WIKI / clean
    if direct.exists():
        return direct.resolve()

    same_folder = page.parent / clean
    if same_folder.exists():
        return same_folder.resolve()

    matches = [p for p in all_pages if p.name == Path(clean).name]
    if len(matches) == 1:
        return matches[0].resolve()
    return None


def resolve_markdown_link(target: str, page: Path) -> Path | None:
    if target.startswith(("http://", "https://", "mailto:")):
        return None
    candidate = (page.parent / target).resolve()
    if candidate.exists():
        return candidate
    candidate = (ROOT / target).resolve()
    if candidate.exists():
        return candidate
    return None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not INDEX.exists():
        errors.append("Missing wiki/index.md")
    if not LOG.exists():
        errors.append("Missing wiki/log.md")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    pages = wiki_pages()
    contents = {p: read(p) for p in pages}
    index_text = contents[INDEX]
    inbound: dict[Path, set[Path]] = defaultdict(set)

    for page in content_pages():
        if not has_frontmatter(contents[page]):
            errors.append(f"{rel(page)} is missing YAML frontmatter")
        if rel(page) not in index_text and page.stem not in index_text:
            warnings.append(f"{rel(page)} may be missing from wiki/index.md")

    for page, text in contents.items():
        for target in parse_wikilinks(text):
            resolved = resolve_wikilink(target, page, pages)
            if resolved is None:
                errors.append(f"{rel(page)} has broken wikilink [[{target}]]")
            elif resolved.is_relative_to(WIKI.resolve()):
                inbound[resolved].add(page)

        for target in parse_markdown_links(text):
            resolved = resolve_markdown_link(target, page)
            if resolved is None:
                errors.append(f"{rel(page)} has broken markdown link ({target})")
            elif resolved.is_relative_to(WIKI.resolve()):
                inbound[resolved].add(page)

        if re.search(r"\b(TODO|TBD|FIXME)\b", text):
            warnings.append(f"{rel(page)} contains TODO/TBD/FIXME")

    for page in content_pages():
        incoming = {p for p in inbound.get(page.resolve(), set()) if p != INDEX}
        if not incoming and page.parent.name not in {"sources", "lints"}:
            warnings.append(f"{rel(page)} has no inbound wiki links except index")

    for line_number, line in enumerate(contents[LOG].splitlines(), start=1):
        if line.startswith("## [") and not LOG_HEADING_RE.match(line):
            errors.append(f"wiki/log.md:{line_number} has nonstandard log heading")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"OK: {len(pages)} wiki page(s) checked, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

