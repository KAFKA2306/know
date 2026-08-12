import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_evidence_contract_kpi.py"
SPEC = importlib.util.spec_from_file_location("validate_evidence_contract_kpi", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
ContractError = MODULE.ContractError
validate_ledger = MODULE.validate_ledger


def production_ledger():
    return json.loads((ROOT / "audit" / "evidence-contract-kpi.json").read_text(encoding="utf-8"))


class EvidenceContractKpiTests(unittest.TestCase):
    def test_production_ledger_is_valid(self):
        validate_ledger(production_ledger())

    def test_uninstrumented_zero_is_rejected(self):
        ledger = production_ledger()
        ledger["metrics"]["starter_opened"]["count"] = 0
        with self.assertRaisesRegex(ContractError, "count=null"):
            validate_ledger(ledger)

    def test_measured_zero_requires_measurement_evidence(self):
        ledger = production_ledger()
        ledger["status"] = "MEASURING"
        ledger["metrics"]["starter_opened"] = {
            "measurement_state": "measured",
            "count": 0,
            "evidence_refs": [],
        }
        with self.assertRaisesRegex(ContractError, "requires evidence"):
            validate_ledger(ledger)

    def test_synthetic_measured_event_with_public_evidence_is_valid(self):
        ledger = production_ledger()
        ledger["status"] = "MEASURING"
        ledger["evidence"] = [
            {
                "id": "synthetic-test-evidence",
                "metric": "paid_pilot",
                "observed_at": "2026-01-01T00:00:00Z",
                "source_url": "https://example.com/public-evidence",
            }
        ]
        ledger["metrics"]["paid_pilot"] = {
            "measurement_state": "measured",
            "count": 1,
            "evidence_refs": ["synthetic-test-evidence"],
        }
        validate_ledger(ledger)

    def test_public_ledger_rejects_sensitive_fields(self):
        ledger = production_ledger()
        ledger["evidence"] = [
            {
                "id": "synthetic-test-evidence",
                "metric": "qualified_inquiry",
                "observed_at": "2026-01-01T00:00:00Z",
                "source_url": "https://example.com/public-evidence",
                "email": "private@example.com",
            }
        ]
        ledger["status"] = "MEASURING"
        ledger["metrics"]["qualified_inquiry"] = {
            "measurement_state": "measured",
            "count": 1,
            "evidence_refs": ["synthetic-test-evidence"],
        }
        with self.assertRaisesRegex(ContractError, "forbidden sensitive key"):
            validate_ledger(ledger)

    def test_evidence_cannot_be_reused_for_another_metric(self):
        ledger = production_ledger()
        ledger["status"] = "MEASURING"
        ledger["evidence"] = [
            {
                "id": "synthetic-test-evidence",
                "metric": "qualified_inquiry",
                "observed_at": "2026-01-01T00:00:00Z",
                "source_url": "https://example.com/public-evidence",
            }
        ]
        ledger["metrics"]["paid_pilot"] = {
            "measurement_state": "measured",
            "count": 1,
            "evidence_refs": ["synthetic-test-evidence"],
        }
        with self.assertRaisesRegex(ContractError, "references evidence for"):
            validate_ledger(ledger)


if __name__ == "__main__":
    unittest.main()
