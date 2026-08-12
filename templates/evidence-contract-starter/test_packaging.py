import json
from pathlib import Path
import unittest


STARTER = Path(__file__).resolve().parent
REPO_ROOT = STARTER.parents[1]


class EvidenceIntegrationPackagingTests(unittest.TestCase):
    def test_copyable_starter_is_complete(self):
        required = [
            STARTER / "README.md",
            STARTER / "contract.schema.json",
            STARTER / "validate_contract.py",
            STARTER / "test_validator.py",
            STARTER / "examples" / "valid.json",
            STARTER / "examples" / "missing-evidence.json",
            STARTER / "ontology" / "project.yaml",
            STARTER / ".github" / "workflows" / "evidence-contract.yml",
        ]
        missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.is_file()]
        self.assertEqual([], missing)

    def test_sample_workflow_is_read_only_and_fail_closed(self):
        workflow = (STARTER / ".github" / "workflows" / "evidence-contract.yml").read_text()
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertIn("missing-evidence.json", workflow)
        self.assertIn("exit 1", workflow)
        self.assertNotIn("secrets.", workflow)

    def test_public_kpi_ledger_does_not_turn_unknown_into_zero(self):
        ledger = json.loads((REPO_ROOT / "audit" / "evidence-contract-kpi.json").read_text())
        self.assertEqual("evidence-contract-kpi.v2", ledger["schema_version"])
        self.assertEqual("NOT_INSTRUMENTED", ledger["status"])
        self.assertEqual([], ledger["evidence"])
        self.assertTrue(ledger["metrics"])
        for metric in ledger["metrics"].values():
            self.assertEqual("not_instrumented", metric["measurement_state"])
            self.assertIsNone(metric["count"])
            self.assertEqual([], metric["evidence_refs"])

    def test_service_page_keeps_guarantee_boundary(self):
        page = (REPO_ROOT / "docs" / "services" / "evidence-contract-integration.md").read_text()
        self.assertIn("保証しません", page)
        self.assertIn("private source", page)
        self.assertIn("templateを見る", page)
        self.assertIn("自分のrepoへ適用する", page)
        self.assertIn("not_instrumented", page)
        self.assertIn("実測0", page)


if __name__ == "__main__":
    unittest.main()
