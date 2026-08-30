#!/usr/bin/env python3
"""Run dependency-free structural checks over the generated static site."""

from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", "__pycache__"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[tuple[str, str]] = []
        self.title_count = 0
        self.h1_count = 0
        self.heading_levels: list[int] = []
        self.main_count = 0
        self.nav_labels: list[str | None] = []
        self.images_without_alt = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.append(attributes["id"] or "")
        if tag == "title":
            self.title_count += 1
        elif len(tag) == 2 and tag.startswith("h") and tag[1].isdigit():
            level = int(tag[1])
            self.heading_levels.append(level)
            if level == 1:
                self.h1_count += 1
        elif tag == "main":
            self.main_count += 1
        elif tag == "nav":
            self.nav_labels.append(attributes.get("aria-label"))
        elif tag == "img" and "alt" not in attributes:
            self.images_without_alt += 1
        if tag in {"a", "link"} and attributes.get("href"):
            self.references.append(("href", attributes["href"] or ""))
        if tag == "script" and attributes.get("src"):
            self.references.append(("src", attributes["src"] or ""))
        if tag == "img" and attributes.get("src"):
            self.references.append(("src", attributes["src"] or ""))


def html_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part in EXCLUDED_PARTS for part in path.parts)
    )


def resolve_local(page: Path, reference: str) -> tuple[Path, str] | None:
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("mailto:", "tel:")):
        return None
    if parsed.path.startswith("/"):
        raise ValueError("root-relative URL would escape or assume the /astro/ deployment path")
    path_text = unquote(parsed.path)
    target = page if not path_text else (page.parent / path_text)
    if path_text.endswith("/"):
        target = target / "index.html"
    elif target.is_dir():
        target = target / "index.html"
    return target.resolve(), parsed.fragment


def has_exact_case(target: Path) -> bool:
    """Catch path-case mistakes even when checks run on case-insensitive macOS."""
    try:
        relative = target.relative_to(ROOT.resolve())
    except ValueError:
        return False
    current = ROOT.resolve()
    for part in relative.parts:
        if part not in {entry.name for entry in current.iterdir()}:
            return False
        current = current / part
    return True


def main() -> int:
    errors: list[str] = []
    pages = html_files()
    parsers: dict[Path, PageParser] = {}
    for page in pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parsers[page.resolve()] = parser
        relative = page.relative_to(ROOT)
        if parser.title_count != 1:
            errors.append(f"{relative}: expected one <title>, found {parser.title_count}")
        if parser.h1_count != 1:
            errors.append(f"{relative}: expected one <h1>, found {parser.h1_count}")
        if parser.heading_levels and parser.heading_levels[0] != 1:
            errors.append(f"{relative}: first heading is not <h1>")
        for previous, current in zip(parser.heading_levels, parser.heading_levels[1:]):
            if current > previous + 1:
                errors.append(f"{relative}: heading order jumps from h{previous} to h{current}")
        if parser.main_count != 1:
            errors.append(f"{relative}: expected one <main>, found {parser.main_count}")
        if None in parser.nav_labels:
            errors.append(f"{relative}: navigation landmark lacks aria-label")
        if len(parser.ids) != len(set(parser.ids)):
            errors.append(f"{relative}: duplicate element id")
        if parser.images_without_alt:
            errors.append(f"{relative}: {parser.images_without_alt} image(s) lack alt text")
        source = page.read_text(encoding="utf-8").lower()
        if "coming soon" in source or "href=\"#\"" in source:
            errors.append(f"{relative}: placeholder content or empty destination found")

    for page, parser in parsers.items():
        relative = page.relative_to(ROOT)
        for attribute, reference in parser.references:
            try:
                resolved = resolve_local(page, reference)
            except ValueError as error:
                errors.append(f"{relative}: {attribute}={reference!r}: {error}")
                continue
            if resolved is None:
                continue
            target, fragment = resolved
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{relative}: local reference escapes repository: {reference}")
                continue
            if not target.exists():
                errors.append(f"{relative}: missing local target: {reference}")
                continue
            if not has_exact_case(target):
                errors.append(f"{relative}: local target has a case mismatch: {reference}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = parsers.get(target)
                if target_parser and fragment not in target_parser.ids:
                    errors.append(f"{relative}: missing fragment #{fragment} in {target.relative_to(ROOT)}")

    data = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
    year_slugs = [year["slug"] for year in data["years"]]
    if len(year_slugs) != len(set(year_slugs)):
        errors.append("data/site.json: research year slugs are not unique")
    if data["site"]["latest_year"] not in year_slugs:
        errors.append("data/site.json: latest_year is not a declared research year")
    slugs: list[str] = []
    for project in data["projects"]:
        slugs.append(project["slug"])
        if project.get("year") not in year_slugs:
            errors.append(f"data/site.json: undeclared year for {project['slug']}")
        if not all(project.get(key) for key in ("question", "significance", "method", "result")):
            errors.append(f"data/site.json: incomplete public record for {project['slug']}")
        if project.get("credits") and not project.get("external_collaboration"):
            errors.append(f"data/site.json: credits require external_collaboration for {project['slug']}")
        if project.get("external_collaboration") and not project.get("collaboration"):
            errors.append(f"data/site.json: external collaboration lacks a public description for {project['slug']}")
        for artifact in project["artifacts"]:
            artifact_path = ROOT / artifact["path"]
            if not artifact_path.is_file():
                errors.append(f"data/site.json: missing artifact {artifact['path']}")
    if len(slugs) != len(set(slugs)):
        errors.append("data/site.json: project slugs are not unique")
    if not data["site"].get("show_project_credits"):
        credited = [project["slug"] for project in data["projects"] if project.get("credits")]
        if credited:
            errors.append("data/site.json: credits must be deleted from public data when show_project_credits is false")

    if errors:
        print("Site checks failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"Site checks passed: {len(pages)} HTML pages, {len(data['projects'])} project records, and all local targets resolved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
