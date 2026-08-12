#!/usr/bin/env python3
"""Validate the public Evidence Contract service KPI ledger.

The ledger deliberately distinguishes an uninstrumented metric from a measured zero.
No customer-private data belongs in this public file.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

EXPECTED_METRICS = {
    "starter_opened",
    "template_copied",
    "integration_inquiry_started",
    "qualified_inquiry",
    "mapping_session_completed",
    "paid_pilot",
    "multi_repo_expansion_requested",
}
ALLOWED_METRIC_STATES = {"not_instrumented", "measured", "unavailable"}
ALLOWED_LEDGER_STATES = {"NOT_INSTRUMENTED", "MEASURING", "COMPLETE"}
SENSITIVE_KEYS = {
    "customer_name",
    "email",
    "phone",
    "credential",
    "credentials",
    "token",
    "api_key",
    "prompt",
    "private_source",
    "business_data",
}


class ContractError(ValueError):
    """Raised when the KPI ledger violates the public evidence contract."""


def _require_https(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{field} must be a string")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ContractError(f"{field} must be an absolute HTTPS URL")
    return value


def _reject_sensitive_keys(value: object, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower()
            if normalized in SENSITIVE_KEYS:
                raise ContractError(f"public ledger contains forbidden sensitive key: {path}.{key}")
            _reject_sensitive_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _reject_sensitive_keys(child, f"{path}[{index}]")


def validate_ledger(data: object) -> None:
    if not isinstance(data, dict):
        raise ContractError("ledger root must be an object")
    if data.get("schema_version") != "evidence-contract-kpi.v2":
        raise ContractError("schema_version must be evidence-contract-kpi.v2")

    status = data.get("status")
    if status not in ALLOWED_LEDGER_STATES:
        raise ContractError(f"invalid ledger status: {status!r}")

    window = data.get("measurement_window_days")
    if not isinstance(window, int) or isinstance(window, bool) or window <= 0:
        raise ContractError("measurement_window_days must be a positive integer")

    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        raise ContractError("metrics must be an object")
    metric_names = set(metrics)
    if metric_names != EXPECTED_METRICS:
        missing = sorted(EXPECTED_METRICS - metric_names)
        extra = sorted(metric_names - EXPECTED_METRICS)
        raise ContractError(f"metric set mismatch; missing={missing}, extra={extra}")

    evidence = data.get("evidence")
    if not isinstance(evidence, list):
        raise ContractError("evidence must be an array")

    evidence_by_id: dict[str, dict[str, object]] = {}
    for item in evidence:
        if not isinstance(item, dict):
            raise ContractError("each evidence item must be an object")
        evidence_id = item.get("id")
        if not isinstance(evidence_id, str) or not evidence_id.strip():
            raise ContractError("evidence.id must be a non-empty string")
        if evidence_id in evidence_by_id:
            raise ContractError(f"duplicate evidence id: {evidence_id}")
        metric = item.get("metric")
        if metric not in EXPECTED_METRICS:
            raise ContractError(f"evidence {evidence_id} has unknown metric: {metric!r}")
        observed_at = item.get("observed_at")
        if not isinstance(observed_at, str) or not observed_at.strip():
            raise ContractError(f"evidence {evidence_id} must include observed_at")
        _require_https(item.get("source_url"), f"evidence[{evidence_id}].source_url")
        evidence_by_id[evidence_id] = item

    measured_count = 0
    for name, metric in metrics.items():
        if not isinstance(metric, dict):
            raise ContractError(f"metric {name} must be an object")
        state = metric.get("measurement_state")
        if state not in ALLOWED_METRIC_STATES:
            raise ContractError(f"metric {name} has invalid measurement_state: {state!r}")
        count = metric.get("count")
        refs = metric.get("evidence_refs")
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            raise ContractError(f"metric {name}.evidence_refs must be a string array")
        if len(refs) != len(set(refs)):
            raise ContractError(f"metric {name} has duplicate evidence_refs")

        if state == "measured":
            measured_count += 1
            if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                raise ContractError(f"measured metric {name} must have a non-negative integer count")
            if not refs:
                raise ContractError(f"measured metric {name} requires evidence even when count is zero")
            for ref in refs:
                item = evidence_by_id.get(ref)
                if item is None:
                    raise ContractError(f"metric {name} references unknown evidence: {ref}")
                if item.get("metric") != name:
                    raise ContractError(f"metric {name} references evidence for {item.get('metric')}: {ref}")
        else:
            if count is not None:
                raise ContractError(f"unmeasured metric {name} must use count=null, not {count!r}")
            if refs:
                raise ContractError(f"unmeasured metric {name} must not claim evidence_refs")

    if status == "NOT_INSTRUMENTED" and measured_count != 0:
        raise ContractError("NOT_INSTRUMENTED ledger cannot contain measured metrics")
    if status == "MEASURING" and measured_count == 0:
        raise ContractError("MEASURING ledger requires at least one measured metric")
    if status == "COMPLETE" and measured_count != len(EXPECTED_METRICS):
        raise ContractError("COMPLETE ledger requires every metric to be measured")

    _reject_sensitive_keys(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    data = json.loads(args.ledger.read_text(encoding="utf-8"))
    validate_ledger(data)
    print(f"validated {args.ledger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
