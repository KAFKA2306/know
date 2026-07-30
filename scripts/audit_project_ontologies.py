#!/usr/bin/env python3
"""Validate registered KAFKA project ontology manifests and README discovery links."""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "ontology" / "projects.yaml"
SCHEMA_PATH = ROOT / "ontology" / "project.schema.json"
USER_AGENT = "KAFKA2306-ontology-audit/0.1"
TIMEOUT_SECONDS = 30


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset)


def read_yaml_text(text: str, label: str) -> dict[str, Any]:
    value = yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError(f"{label}: YAML root must be an object")
    return value


def read_local_yaml(path: Path) -> dict[str, Any]:
    return read_yaml_text(path.read_text(encoding="utf-8"), str(path))


def read_local_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return value


def readme_url_from_manifest(manifest_url: str) -> str:
    suffix = "/ontology/project.yaml"
    if not manifest_url.endswith(suffix):
        raise ValueError(f"manifest URL must end with {suffix}: {manifest_url}")
    return manifest_url[: -len(suffix)] + "/README.md"


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    projects = registry.get("projects")
    if not isinstance(projects, list) or not projects:
        return ["registry.projects must be a non-empty list"]

    seen_ids: set[str] = set()
    seen_repositories: set[str] = set()
    for index, entry in enumerate(projects):
        label = f"registry.projects[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label}: entry must be an object")
            continue
        project_id = entry.get("id")
        repository = entry.get("repository")
        manifest = entry.get("manifest")
        upper_system = entry.get("upper_system")
        for key, value in {
            "id": project_id,
            "repository": repository,
            "manifest": manifest,
            "upper_system": upper_system,
        }.items():
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{label}.{key}: required non-empty string")
        if isinstance(project_id, str):
            if project_id in seen_ids:
                errors.append(f"{label}.id: duplicate {project_id}")
            seen_ids.add(project_id)
        if isinstance(repository, str):
            if repository in seen_repositories:
                errors.append(f"{label}.repository: duplicate {repository}")
            seen_repositories.add(repository)
    return errors


def audit_project(entry: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    project_id = str(entry.get("id", "<unknown>"))
    manifest_url = entry.get("manifest")
    repository = entry.get("repository")
    upper_system = entry.get("upper_system")

    if not isinstance(manifest_url, str):
        return [f"{project_id}: manifest URL is missing"]

    try:
        manifest_text = fetch_text(manifest_url)
        manifest = read_yaml_text(manifest_text, manifest_url)
    except (urllib.error.URLError, TimeoutError, UnicodeError, ValueError) as exc:
        return [f"{project_id}: cannot fetch or parse manifest: {exc}"]

    try:
        jsonschema.Draft202012Validator(schema).validate(manifest)
    except jsonschema.ValidationError as exc:
        path = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        errors.append(f"{project_id}: schema error at {path}: {exc.message}")

    project = manifest.get("project", {})
    if isinstance(project, dict):
        if project.get("id") != project_id:
            errors.append(
                f"{project_id}: manifest project.id is {project.get('id')!r}"
            )
        if project.get("repository") != repository:
            errors.append(
                f"{project_id}: manifest repository does not match registry"
            )
    else:
        errors.append(f"{project_id}: manifest.project must be an object")

    domain_mapping = manifest.get("domain_mapping", {})
    manifest_system = domain_mapping.get("System") if isinstance(domain_mapping, dict) else None
    if manifest_system != upper_system:
        errors.append(
            f"{project_id}: domain_mapping.System {manifest_system!r} "
            f"does not match registry upper_system {upper_system!r}"
        )

    try:
        readme_url = readme_url_from_manifest(manifest_url)
        readme = fetch_text(readme_url)
    except (urllib.error.URLError, TimeoutError, UnicodeError, ValueError) as exc:
        errors.append(f"{project_id}: cannot fetch README: {exc}")
    else:
        if "ontology/project.yaml" not in readme:
            errors.append(f"{project_id}: README does not link ontology/project.yaml")
        if "causal-evidence-core" not in readme:
            errors.append(f"{project_id}: README does not link the shared core ontology")

    return errors


def main() -> int:
    registry = read_local_yaml(REGISTRY_PATH)
    schema = read_local_json(SCHEMA_PATH)

    errors = validate_registry(registry)
    projects = registry.get("projects", [])
    if isinstance(projects, list):
        for entry in projects:
            if isinstance(entry, dict):
                errors.extend(audit_project(entry, schema))

    if errors:
        print("Ontology audit failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Ontology audit passed for {len(projects)} registered projects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
