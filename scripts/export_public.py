#!/usr/bin/env python3
"""Export committed public lab files and optional minicourses to an empty directory.

Reads Git blobs, never untracked files or working-tree edits. Does not deploy.
"""
from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
import posixpath
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

LAB_BASE = "https://activities.tjhsst.edu/astro/"
SCHOOL_BASE = "https://astro2627.sites.tjhsst.edu/"
PUBLIC_SUFFIXES = {".html", ".css", ".js", ".pdf", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".zip"}
ATTR = re.compile(r'''\b(href|src|poster)\s*=\s*(["'])(.*?)\2''', re.I | re.S)
CSS_URL = re.compile(r'''url\(\s*(["']?)([^)'"\s]+)\1\s*\)''', re.I)


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(repo), *args])


class Snapshot:
    def __init__(self, root: Path, ref: str):
        self.root = root
        self.commit = git(root, "rev-parse", "--verify", ref + "^{commit}").decode().strip()
        self.paths: dict[str, str] = {}
        for entry in git(root, "ls-tree", "-rz", self.commit).split(b"\0"):
            if entry:
                metadata, name = entry.split(b"\t", 1)
                mode, kind, _ = metadata.decode().split()
                if kind == "blob":
                    self.paths[name.decode()] = mode
        self.cache: dict[str, bytes] = {}

    def read(self, path: str) -> bytes:
        if self.paths.get(path) not in {"100644", "100755"}:
            raise ValueError(f"Missing, untracked, or symlink file at {self.commit}: {path}")
        if path not in self.cache:
            self.cache[path] = git(self.root, "show", f"{self.commit}:{path}")
        return self.cache[path]


def public_path(path: str) -> None:
    parts = PurePosixPath(path).parts
    if not parts or path.startswith("/") or any(p.startswith(".") or p in {"instructor_outputs", "workflow_runs", "experiments"} for p in parts):
        raise ValueError(f"Unsafe public path: {path}")
    if PurePosixPath(path).suffix.lower() not in PUBLIC_SUFFIXES:
        raise ValueError(f"Not an approved public file type: {path}")


class HTMLReferences(HTMLParser):
    """Rewrite only parsed URL attributes, preserving all other source bytes."""
    def __init__(self, source: str, rewrite):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.rewrite = rewrite
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.edits = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if "srcset" in values or tag == "base":
            raise ValueError("srcset/base requires an explicit export implementation")
        raw = self.get_starttag_text()
        line, col = self.getpos()
        start = self.offsets[line - 1] + col
        canonical = tag == "link" and values.get("rel") == "canonical"
        for match in ATTR.finditer(raw):
            attr = match[1].lower()
            kind = "navigation" if tag == "a" else ("canonical" if canonical else "runtime")
            old = html.unescape(match[3])
            new = self.rewrite(old, kind)
            if new != old:
                self.edits.append((start + match.start(3), start + match.end(3), html.escape(new, quote=True)))

    handle_startendtag = handle_starttag

    def result(self):
        result = self.source
        for start, end, replacement in reversed(self.edits):
            result = result[:start] + replacement + result[end:]
        return result


def export(lab: Snapshot, output: Path, school: Snapshot | None = None,
           public_base: str = "https://wdlinch3.github.io/astro/",
           personal_course_base: str | None = None) -> dict:
    if output.exists() and any(output.iterdir()):
        raise ValueError("Output must be absent or empty; existing files are never removed")
    parsed_base = urlsplit(public_base)
    if parsed_base.scheme not in {"https", "http"} or not parsed_base.netloc or not public_base.endswith("/") or parsed_base.query or parsed_base.fragment:
        raise ValueError("public-base must be an absolute HTTP(S) URL ending in /")
    course_mappings = {}
    if personal_course_base:
        parsed_course = urlsplit(personal_course_base)
        if parsed_course.scheme not in {"https", "http"} or not parsed_course.netloc or not personal_course_base.endswith("/") or parsed_course.query or parsed_course.fragment:
            raise ValueError("personal-course-base must be an absolute HTTP(S) URL ending in /")
        course_mappings = {
            SCHOOL_BASE: personal_course_base,
            SCHOOL_BASE + "ss/2026-2027/": personal_course_base + "ss/2026-2027/",
        }
    files: dict[str, tuple[Snapshot, str, str]] = {}
    # Only generator-owned committed pages seed the lab export. References then
    # include its public artifacts/assets; unrelated or untracked files cannot enter.
    for path in lab.paths:
        if path.endswith(".html") and b"Generated by scripts/build_site.py" in lab.read(path):
            files[path] = (lab, path, urljoin(LAB_BASE, path))
    if "index.html" not in files:
        raise ValueError("No generator-owned lab homepage in the selected revision")
    school_paths = set()
    if school:
        school_paths = set(json.loads(school.read("scripts/minicourses.json"))["files"])
        school_paths.add("assets/css/aa_packet_theme.css")
        for path in sorted(school_paths):
            public_path(path)
            school.read(path)
            files["school/" + path] = (school, path, urljoin(SCHOOL_BASE, path))
    external: dict[tuple[str, str], set[str]] = {}
    links = []
    payload: dict[str, bytes] = {}
    source_info = {}
    ids = {}

    def record_external(url, kind, page):
        external.setdefault((url, kind), set()).add(page)

    def rewrite(value, kind, page, origin):
        if not value or value.startswith(("data:", "mailto:", "tel:", "javascript:")):
            return value
        absolute = urljoin(origin, value)
        parsed = urlsplit(absolute)
        clean = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
        target = None
        if kind == "navigation" and clean in course_mappings:
            mapped = urlsplit(course_mappings[clean])
            destination = urlunsplit((mapped.scheme, mapped.netloc, mapped.path, parsed.query, parsed.fragment))
            record_external(destination, "personal_course_navigation", page)
            return destination
        if clean.startswith(LAB_BASE):
            source_path = unquote(clean[len(LAB_BASE):])
            if not source_path or source_path.endswith("/"):
                source_path += "index.html"
            public_path(source_path)
            lab.read(source_path)
            target = source_path
            files.setdefault(target, (lab, source_path, urljoin(LAB_BASE, source_path)))
        elif clean.startswith(SCHOOL_BASE):
            source_path = unquote(clean[len(SCHOOL_BASE):])
            if source_path in school_paths:
                target = "school/" + source_path
            elif kind == "runtime" and school:
                raise ValueError(f"School runtime dependency absent from allowlist: {absolute} ({page})")
        if target is None:
            if parsed.scheme in {"http", "https"}:
                record_external(absolute, kind, page)
            return absolute if value.startswith("/") or not urlsplit(value).scheme else value
        links.append((page, target, unquote(parsed.fragment)))
        if kind == "canonical":
            relative = target.removesuffix("index.html")
            return urljoin(public_base, relative)
        relative = posixpath.relpath(target, posixpath.dirname(page) or ".")
        if target == page and not parsed.query and parsed.fragment:
            relative = ""
        return urlunsplit(("", "", relative, parsed.query, parsed.fragment))

    while set(files) - set(payload):
        page = sorted(set(files) - set(payload))[0]
        snapshot, source_path, origin = files[page]
        public_path(source_path)
        original = snapshot.read(source_path)
        content = original
        suffix = PurePosixPath(source_path).suffix.lower()
        if suffix == ".html":
            parser = HTMLReferences(original.decode("utf-8"), lambda value, kind: rewrite(value, kind, page, origin))
            parser.feed(original.decode("utf-8"))
            content = parser.result().encode("utf-8")
            ids[page] = parser.ids
        elif suffix == ".css":
            source = original.decode("utf-8")
            content = CSS_URL.sub(lambda m: "url(" + m[1] + rewrite(m[2], "runtime", page, origin) + m[1] + ")", source).encode("utf-8")
        payload[page] = content
        source_info[page] = {"repository": "lab" if snapshot is lab else "school", "path": source_path,
                             "source_sha256": hashlib.sha256(original).hexdigest(), "sha256": hashlib.sha256(content).hexdigest()}
    for page, target, fragment in links:
        if target not in payload:
            raise ValueError(f"Missing export target: {page} -> {target}")
        if fragment and target in ids and fragment not in ids[target]:
            raise ValueError(f"Missing fragment: {page} -> {target}#{fragment}")
    manifest = {
        "schema_version": 1, "public_base": public_base,
        "sources": {"lab": {"commit": lab.commit, "repository": "https://github.com/wdlinch3/astro_site"}},
        "files": dict(sorted(source_info.items())),
        "personal_course_link_mappings": course_mappings,
        "external_dependencies": [{"url": url, "kind": kind, "pages": sorted(pages)} for (url, kind), pages in sorted(external.items())],
        "scope": "Committed generated lab pages and their public dependencies; optional allowlisted minicourses. No private sources or remote-only files.",
        "limitations": ["External navigation and CDN runtime dependencies remain listed below.", "JavaScript-created requests are not inferred; this is not an offline edition.", "School/Director-only changes cannot be recovered from Git and require a separate live/source comparison."],
    }
    if school:
        manifest["sources"]["school"] = {"commit": school.commit, "repository": "https://github.com/wdlinch3/astro2627"}
        if "SOURCE_COMMIT" in school.paths:
            manifest["sources"]["school"]["content_source_commit"] = school.read("SOURCE_COMMIT").decode().strip()
    output.mkdir(parents=True, exist_ok=True)
    for path, contents in sorted(payload.items()):
        destination = output / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(contents)
    (output / "MIRROR_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--school-source", type=Path)
    parser.add_argument("--school-ref", default="HEAD")
    parser.add_argument("--personal-course-base", help="Map the AA home and 2026-27 class links to an independently validated personal-site AA base URL")
    parser.add_argument("--public-base", default="https://wdlinch3.github.io/astro/")
    args = parser.parse_args()
    try:
        manifest = export(Snapshot(args.source, args.ref), args.output,
                          Snapshot(args.school_source, args.school_ref) if args.school_source else None, args.public_base, args.personal_course_base)
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Export failed: {error}\n")
    print(f"Exported {len(manifest['files'])} files; {len(manifest['external_dependencies'])} external dependencies recorded.")
    print(f"Manifest: {args.output / 'MIRROR_MANIFEST.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
