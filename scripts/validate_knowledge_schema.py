#!/usr/bin/env python3
"""Validate Know's MkDocs metadata; optionally export an OKF v0.3 bundle.

The files under docs/ are the single source of truth. Never assert that a
knowledge page has been verified merely because its metadata is well formed.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCHEMA = ROOT / "ontology" / "knowledge.schema.json"
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)


def load_page(path: Path) -> tuple[dict, str]:
    content = path.read_text(encoding="utf-8")
    match = FRONTMATTER.match(content)
    if not match:
        raise ValueError("YAML frontmatter is missing")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a mapping")
    return metadata, content


def validate() -> tuple[list[Path], list[str]]:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
    pages = sorted(DOCS.rglob("*.md"))
    errors: list[str] = []
    for page in pages:
        name = page.relative_to(ROOT).as_posix()
        try:
            metadata, body = load_page(page)
        except (ValueError, yaml.YAMLError, UnicodeError) as error:
            errors.append(f"{name}: {error}")
            continue
        for error in sorted(validator.iter_errors(metadata), key=lambda item: str(item.path)):
            field = ".".join(str(p) for p in error.absolute_path) or "<root>"
            errors.append(f"{name}: {field}: {error.message}")
        # A schema-compliant value is not evidence of an independent review.
        if metadata.get("status") == "verified" and not (metadata.get("sources") and metadata.get("verified")):
            errors.append(f"{name}: verified status requires sources and verified records")
        sources = metadata.get("sources", [])
        if isinstance(sources, list):
            ids = [s.get("id") for s in sources if isinstance(s, dict)]
            if len(ids) != len(set(ids)):
                errors.append(f"{name}: duplicate sources[].id")
            for source_id in ids:
                if isinstance(source_id, str) and f"[^{source_id}]" not in body:
                    errors.append(f"{name}: sources id {source_id!r} is not cited as a footnote")
    return pages, errors


def export_okf(pages: list[Path], destination: Path) -> None:
    """Produce a derived OKF bundle without changing MkDocs URLs or source files.

    The source index.md is a MkDocs page. It becomes overview.md in the bundle,
    leaving index.md for OKF's directory navigation contract.
    """
    destination = destination.resolve()
    if destination == DOCS.resolve() or DOCS.resolve() in destination.parents:
        raise ValueError("export destination cannot be inside docs/")
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("export destination must not contain existing files")
    directories: set[Path] = {Path(".")}
    concept_paths: list[Path] = []
    for page in pages:
        relative = page.relative_to(DOCS)
        if relative.name == "index.md":
            relative = relative.with_name("overview.md")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(page, target)
        concept_paths.append(relative)
        current = relative.parent
        while current != Path("."):
            directories.add(current)
            current = current.parent

    for directory in sorted(directories, key=lambda p: (len(p.parts), p.as_posix())):
        local_files = sorted(p for p in concept_paths if p.parent == directory)
        children = sorted(d for d in directories if d.parent == directory and d != directory)
        prefix = '---\nokf_version: "0.3"\n---\n\n' if directory == Path(".") else ""
        title = "Know" if directory == Path(".") else directory.name
        lines = [f"# {title}", "", "## 文書", ""]
        lines.extend(f"- [{p.stem}]({p.name})" for p in local_files)
        if children:
            lines += ["", "## 下位フォルダ", ""]
            lines.extend(f"- [{d.name}]({d.name}/index.md)" for d in children)
        (destination / directory / "index.md").write_text(
            prefix + "\n".join(lines) + "\n", encoding="utf-8"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-okf", type=Path, metavar="DIRECTORY")
    args = parser.parse_args()
    pages, errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"FAIL: {len(errors)} schema errors in {len(pages)} pages", file=sys.stderr)
        return 1
    print(f"PASS: {len(pages)} MkDocs pages satisfy ontology/knowledge.schema.json")
    if args.export_okf:
        try:
            export_okf(pages, args.export_okf)
        except (ValueError, OSError) as error:
            print(f"OKF export failed: {error}", file=sys.stderr)
            return 1
        print(f"OKF v0.3 bundle exported to {args.export_okf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
