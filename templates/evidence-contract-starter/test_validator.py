from __future__ import annotations

import json
import unittest
from pathlib import Path

from validate_contract import validate

ROOT = Path(__file__).parent


class EvidenceContractValidatorTests(unittest.TestCase):
    def load(self, name: str) -> dict:
        return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))

    def test_valid_contract_passes(self) -> None:
        self.assertEqual(validate(self.load("valid.json")), [])

    def test_pass_without_evidence_is_rejected(self) -> None:
        errors = validate(self.load("missing-evidence.json"))
        self.assertTrue(any("cannot PASS without evidence" in error for error in errors))

    def test_unverified_evidence_blocks_pass(self) -> None:
        document = self.load("valid.json")
        document["evidence"][0]["integrity_status"] = "UNVERIFIED"
        errors = validate(document)
        self.assertTrue(any("cannot PASS with unverified evidence" in error for error in errors))

    def test_unknown_evidence_reference_is_rejected(self) -> None:
        document = self.load("valid.json")
        document["decisions"][0]["evidence"] = ["missing"]
        errors = validate(document)
        self.assertTrue(any("unknown evidence" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
