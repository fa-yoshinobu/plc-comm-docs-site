from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_validation_results import EvidenceError, generate, load_evidence


class ValidationResultGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.input = self.root / "evidence"
        self.run = self.input / "00000000-0000-4000-8000-000000000001"
        self.run.mkdir(parents=True)
        self.output = self.root / "result.md"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_evidence(self, extra_target: dict[str, object] | None = None) -> None:
        target = {
            "manufacturer": "Mitsubishi Electric", "model": "R120PCPU", "cpu_firmware": None,
            "canonical_profile": "melsec:iq-r", "transport": "tcp", "frame": "4E",
        }
        if extra_target:
            target.update(extra_target)
        result = {
            "schema_version": "1.0", "classification": "public",
            "run_id": "00000000-0000-4000-8000-000000000001", "protocol": "slmp",
            "test_kind": "basic_use", "execution_status": "completed", "verdict": "pass",
            "library": {"name": "plc-comm-slmp", "version": "tested-version", "language": "Python",
                        "runtime": "CPython", "artifact_sha256": "1" * 64},
            "target": target,
            "host": {"os": "linux", "architecture": "arm64", "runtime": "Linux runtime"},
            "timing": {"started_at": "2026-07-31T00:00:00Z", "finished_at": "2026-07-31T00:05:00Z",
                       "monotonic_duration_seconds": 300},
            "scope": {"required_case_count": 1, "executed_case_count": 1, "required_attempt_count": 1,
                      "executed_attempt_count": 1, "inventory_feature_count": 0,
                      "inventory_covered_count": 0, "excluded_feature_count": 0,
                      "excluded_features": [], "unconditional_full_feature_claim": False},
            "operation_summaries": [{
                "case_id": "B-READ-WORD-1", "operation": "read_one_word",
                "public_api": "slmp.read_typed", "attempts": 1, "successful_attempts": 1,
                "requests": 1, "successful_requests": 1, "unexpected_errors": 0,
                "timeouts": 0, "plc_errors": 0, "decode_errors": 0,
                "readback_mismatches": 0,
                "latency_ms": {"count": 1, "p50": 1, "p95": 1, "p99": 1, "max": 1},
            }],
            "totals": {"requests": 1, "successful_requests": 1, "unexpected_errors": 0,
                       "timeouts": 0, "plc_errors": 0, "decode_errors": 0,
                       "readback_mismatches": 0, "reconnect_attempts": 0, "successful_reconnects": 0},
            "evidence_manifest": "evidence-manifest.json", "failure_code": None,
        }
        result_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
        (self.run / "validation-result.json").write_bytes(result_bytes)
        manifest = {
            "schema_version": "1.0", "manifest_scope": "public", "run_id": result["run_id"],
            "generated_at": "2026-07-31T00:05:00Z",
            "artifacts": [{"role": "validation_result", "path": "validation-result.json",
                           "media_type": "application/json", "sha256": hashlib.sha256(result_bytes).hexdigest(),
                           "classification": "public"}],
        }
        (self.run / "evidence-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    def replace_result(self, result: dict[str, object]) -> None:
        result_bytes = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode()
        (self.run / "validation-result.json").write_bytes(result_bytes)
        manifest_path = self.run / "evidence-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["artifacts"][0]["sha256"] = hashlib.sha256(result_bytes).hexdigest()
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def test_generates_minimal_public_page_and_check_mode(self) -> None:
        self.write_evidence()
        generate(self.input, self.output, check=False)
        page = self.output.read_text(encoding="utf-8")
        self.assertIn("R120PCPU", page)
        self.assertIn("tested-version", page)
        self.assertNotIn("192.0.2.10", page)
        generate(self.input, self.output, check=True)

    def test_rejects_unexpected_endpoint_field(self) -> None:
        self.write_evidence({"host": "192.0.2.10"})
        with self.assertRaises(EvidenceError):
            load_evidence(self.run)

    def test_rejects_manifest_digest_mismatch(self) -> None:
        self.write_evidence()
        manifest_path = self.run / "evidence-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["artifacts"][0]["sha256"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(EvidenceError):
            load_evidence(self.run)

    def test_rejects_unexpected_file_in_public_evidence_directory(self) -> None:
        self.write_evidence()
        (self.run / "target.json").write_text('{"host":"192.0.2.10"}', encoding="utf-8")
        with self.assertRaises(EvidenceError):
            load_evidence(self.run)

    def test_rejects_invalid_nested_performance_summary(self) -> None:
        self.write_evidence()
        result_path = self.run / "validation-result.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["performance_summary"] = {
            "throughput_requests_per_second": 10,
            "latency_ms": {"p50": 3, "p95": 2, "p99": 4, "max": 5},
        }
        self.replace_result(result)
        with self.assertRaises(EvidenceError):
            load_evidence(self.run)

    def test_rejects_operation_summary_that_does_not_match_totals(self) -> None:
        self.write_evidence()
        result_path = self.run / "validation-result.json"
        result = json.loads(result_path.read_text(encoding="utf-8"))
        result["operation_summaries"][0]["requests"] = 2
        self.replace_result(result)
        with self.assertRaises(EvidenceError):
            load_evidence(self.run)

    def test_rejects_self_consistent_pass_with_an_error(self) -> None:
        self.write_evidence()
        result = json.loads((self.run / "validation-result.json").read_text(encoding="utf-8"))
        result["operation_summaries"][0]["unexpected_errors"] = 1
        result["totals"]["unexpected_errors"] = 1
        self.replace_result(result)
        with self.assertRaises(EvidenceError):
            load_evidence(self.run)

    def test_rejects_non_full_feature_claim(self) -> None:
        self.write_evidence()
        result = json.loads((self.run / "validation-result.json").read_text(encoding="utf-8"))
        result["scope"]["inventory_feature_count"] = 1
        result["scope"]["inventory_covered_count"] = 1
        self.replace_result(result)
        with self.assertRaises(EvidenceError):
            load_evidence(self.run)

    def test_rejects_full_feature_with_unaccounted_inventory(self) -> None:
        self.write_evidence()
        result = json.loads((self.run / "validation-result.json").read_text(encoding="utf-8"))
        result["test_kind"] = "full_feature"
        result["scope"]["inventory_feature_count"] = 2
        result["scope"]["inventory_covered_count"] = 1
        self.replace_result(result)
        with self.assertRaises(EvidenceError):
            load_evidence(self.run)

    def test_rejects_public_api_containing_endpoint_or_device_address(self) -> None:
        for public_api in ("Client.ReadWords + D100", "Client.ReadWords + 192.0.2.10"):
            with self.subTest(public_api=public_api):
                self.write_evidence()
                result = json.loads(
                    (self.run / "validation-result.json").read_text(encoding="utf-8")
                )
                result["operation_summaries"][0]["public_api"] = public_api
                self.replace_result(result)
                with self.assertRaises(EvidenceError):
                    load_evidence(self.run)


if __name__ == "__main__":
    unittest.main()
