#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_RESULTS = {"PASS", "FAIL", "REVIEW_REQUIRED", "UNKNOWN"}


def validate(document: dict) -> list[str]:
    errors: list[str] = []
    required = {"schema_version", "observations", "claims", "tests", "evidence", "decisions"}
    missing = sorted(required - document.keys())
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
        return errors

    if document["schema_version"] != "1.0.0":
        errors.append("schema_version must be 1.0.0")

    collections = {name: document[name] for name in required - {"schema_version"}}
    for name, rows in collections.items():
        if not isinstance(rows, list):
            errors.append(f"{name} must be an array")

    if errors:
        return errors

    ids: dict[str, str] = {}
    for name, rows in collections.items():
        for index, row in enumerate(rows):
            record_id = row.get("id") if isinstance(row, dict) else None
            if not record_id:
                errors.append(f"{name}[{index}] requires id")
                continue
            if record_id in ids:
                errors.append(f"duplicate id {record_id!r} in {name} and {ids[record_id]}")
            ids[record_id] = name

    claim_ids = {row.get("id") for row in document["claims"] if isinstance(row, dict)}
    evidence_ids = {row.get("id") for row in document["evidence"] if isinstance(row, dict)}

    for index, observation in enumerate(document["observations"]):
        source = observation.get("source") if isinstance(observation, dict) else None
        if not source:
            errors.append(f"observations[{index}] requires provenance source")

    for index, test in enumerate(document["tests"]):
        if test.get("claim_id") not in claim_ids:
            errors.append(f"tests[{index}] references unknown claim_id")
        if test.get("result") not in ALLOWED_RESULTS:
            errors.append(f"tests[{index}] has invalid result")

    for index, evidence in enumerate(document["evidence"]):
        if evidence.get("claim_id") not in claim_ids:
            errors.append(f"evidence[{index}] references unknown claim_id")
        if not evidence.get("location"):
            errors.append(f"evidence[{index}] requires location")

    for index, decision in enumerate(document["decisions"]):
        result = decision.get("result")
        refs = decision.get("evidence", [])
        if result not in ALLOWED_RESULTS:
            errors.append(f"decisions[{index}] has invalid result")
            continue
        missing_refs = [ref for ref in refs if ref not in evidence_ids]
        if missing_refs:
            errors.append(f"decisions[{index}] references unknown evidence: {missing_refs}")
        if result == "PASS" and not refs:
            errors.append(f"decisions[{index}] cannot PASS without evidence")
        if result == "PASS":
            bad = [row["id"] for row in document["evidence"] if row.get("id") in refs and row.get("integrity_status") != "VERIFIED"]
            if bad:
                errors.append(f"decisions[{index}] cannot PASS with unverified evidence: {bad}")
        if not decision.get("decision_rule"):
            errors.append(f"decisions[{index}] requires decision_rule")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_contract.py PATH.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = validate(document)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
