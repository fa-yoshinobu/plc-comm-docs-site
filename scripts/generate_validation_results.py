#!/usr/bin/env python3
"""Generate the public real-hardware validation page from hashed public evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


class EvidenceError(ValueError):
    pass


TOP_LEVEL_KEYS = {
    "schema_version", "classification", "run_id", "protocol", "test_kind",
    "execution_status", "verdict", "library", "target", "host", "timing",
    "scope", "operation_summaries", "totals", "performance_summary", "resource_summary",
    "evidence_manifest", "failure_code",
}
LIBRARY_KEYS = {"name", "version", "language", "runtime", "artifact_sha256"}
TARGET_KEYS = {"manufacturer", "model", "cpu_firmware", "canonical_profile", "transport", "frame"}
HOST_KEYS = {"os", "architecture", "runtime"}
TIMING_KEYS = {"started_at", "finished_at", "monotonic_duration_seconds"}
SCOPE_KEYS = {
    "required_case_count", "executed_case_count", "required_attempt_count",
    "executed_attempt_count", "inventory_feature_count", "inventory_covered_count",
    "excluded_feature_count", "excluded_features", "unconditional_full_feature_claim",
}
TOTAL_KEYS = {
    "requests", "successful_requests", "unexpected_errors", "timeouts", "plc_errors",
    "decode_errors", "readback_mismatches", "reconnect_attempts", "successful_reconnects",
}
PERFORMANCE_KEYS = {"throughput_requests_per_second", "latency_ms"}
LATENCY_KEYS = {"p50", "p95", "p99", "max"}
RESOURCE_KEYS = {
    "rss_start_bytes", "rss_end_bytes", "rss_peak_bytes", "fd_start", "fd_end",
    "fd_peak", "thread_start", "thread_end", "thread_peak",
}
EXCLUSION_KEYS = {"feature_id", "reason_code"}
OPERATION_KEYS = {
    "case_id", "operation", "public_api", "attempts", "successful_attempts",
    "requests", "successful_requests", "unexpected_errors", "timeouts",
    "plc_errors", "decode_errors", "readback_mismatches", "latency_ms",
}
OPERATION_COUNTER_KEYS = {
    "requests", "successful_requests", "unexpected_errors", "timeouts",
    "plc_errors", "decode_errors", "readback_mismatches",
}
EXCLUSION_REASONS = {
    "unsupported_by_selected_profile", "unavailable_in_selected_configuration",
    "not_applicable_to_selected_transport", "documented_read_only",
    "other_approved_exclusion",
}
FRAME_NAMES = {
    "slmp": {"3E", "4E"},
    "hostlink": {"hostlink"},
    "computerlink": {"computerlink"},
    "mcprotocol-serial": {
        "c4-binary-format5",
        "c4-ascii-format1", "c4-ascii-format2", "c4-ascii-format3", "c4-ascii-format4",
        "c3-ascii-format1", "c3-ascii-format2", "c3-ascii-format3", "c3-ascii-format4",
        "c2-ascii-format1", "c2-ascii-format2", "c2-ascii-format3", "c2-ascii-format4",
        "c1-ascii-format1", "c1-ascii-format3", "c1-ascii-format4",
        "e1-binary", "e1-ascii",
    },
}
RUN_ID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
OPERATION_RE = re.compile(r"^[a-z][a-z0-9_]*$")
PUBLIC_API_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_.:]*(?: \+ [A-Za-z_][A-Za-z0-9_.:]*)*$"
)
IPV4_RE = re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")
DEVICE_ADDRESS_RE = re.compile(r"(?<![A-Za-z0-9_])[A-Z]{1,3}[0-9]{1,8}(?![A-Za-z0-9_])")


def _object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvidenceError(f"{name} must be an object")
    return value


def _exact_keys(value: dict[str, Any], allowed: set[str], required: set[str], name: str) -> None:
    extra = set(value) - allowed
    missing = required - set(value)
    if extra:
        raise EvidenceError(f"{name} contains non-public fields: {', '.join(sorted(extra))}")
    if missing:
        raise EvidenceError(f"{name} is missing fields: {', '.join(sorted(missing))}")


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f"{name} must be a non-empty string")
    return value


def _integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise EvidenceError(f"{name} must be a non-negative integer")
    return value


def _number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EvidenceError(f"{name} must be a non-negative number")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise EvidenceError(f"{name} must be a finite non-negative number")
    return number


def _sha256(value: Any, name: str) -> str:
    text = _text(value, name)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text):
        raise EvidenceError(f"{name} must be a lowercase SHA-256")
    return text


def _public_operation_text(operation: Any, public_api: Any) -> tuple[str, str]:
    operation_text = _text(operation, "operation summary operation")
    api_text = _text(public_api, "operation summary public_api")
    if not OPERATION_RE.fullmatch(operation_text):
        raise EvidenceError("operation summary operation must be a stable operation identifier")
    if (not PUBLIC_API_RE.fullmatch(api_text) or IPV4_RE.search(api_text)
            or DEVICE_ADDRESS_RE.search(api_text)):
        raise EvidenceError("operation summary public_api must contain API names only")
    return operation_text, api_text


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return _object(json.loads(path.read_text(encoding="utf-8")), path.name)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"cannot read {path}: {exc}") from exc


def load_evidence(run_dir: Path) -> dict[str, Any]:
    result_path = run_dir / "validation-result.json"
    manifest_path = run_dir / "evidence-manifest.json"
    result_bytes = result_path.read_bytes()
    result = _load_json(result_path)
    manifest = _load_json(manifest_path)

    unexpected_files = sorted(path.name for path in run_dir.iterdir()
                              if path.name not in {"validation-result.json", "evidence-manifest.json"})
    if unexpected_files:
        raise EvidenceError(
            "public evidence directory contains non-public or unexpected files: "
            + ", ".join(unexpected_files)
        )

    required_top = TOP_LEVEL_KEYS - {"performance_summary", "resource_summary", "failure_code"}
    _exact_keys(result, TOP_LEVEL_KEYS, required_top, "validation result")
    if result.get("schema_version") != "1.0" or result.get("classification") != "public":
        raise EvidenceError("validation result is not public schema 1.0")
    if result.get("evidence_manifest") != "evidence-manifest.json":
        raise EvidenceError("validation result does not reference evidence-manifest.json")
    if result.get("execution_status") not in {"completed", "aborted", "infrastructure_error"}:
        raise EvidenceError("invalid execution_status")
    if result.get("verdict") not in {"pass", "fail", "not_evaluated"}:
        raise EvidenceError("invalid verdict")
    if result.get("test_kind") not in {"endurance_72h", "full_feature", "basic_use"}:
        raise EvidenceError("invalid test_kind")
    if result.get("protocol") not in {"slmp", "hostlink", "computerlink", "mcprotocol-serial"}:
        raise EvidenceError("invalid protocol")
    if not isinstance(result.get("run_id"), str) or not RUN_ID_RE.fullmatch(result["run_id"]):
        raise EvidenceError("invalid run_id")
    if result["execution_status"] == "completed" and result["verdict"] == "not_evaluated":
        raise EvidenceError("completed result cannot be not_evaluated")
    if result["execution_status"] != "completed" and result["verdict"] != "not_evaluated":
        raise EvidenceError("incomplete execution must be not_evaluated")
    failure_code = result.get("failure_code")
    if failure_code is not None:
        _text(failure_code, "failure_code")

    library = _object(result["library"], "library")
    target = _object(result["target"], "target")
    host = _object(result["host"], "host")
    timing = _object(result["timing"], "timing")
    scope = _object(result["scope"], "scope")
    operations = result["operation_summaries"]
    totals = _object(result["totals"], "totals")
    _exact_keys(library, LIBRARY_KEYS, LIBRARY_KEYS, "library")
    _exact_keys(target, TARGET_KEYS, TARGET_KEYS, "target")
    _exact_keys(host, HOST_KEYS, HOST_KEYS, "host")
    _exact_keys(timing, TIMING_KEYS, TIMING_KEYS, "timing")
    _exact_keys(scope, SCOPE_KEYS, SCOPE_KEYS, "scope")
    _exact_keys(totals, TOTAL_KEYS, TOTAL_KEYS, "totals")

    for key in ("name", "version", "language", "runtime"):
        _text(library[key], f"library.{key}")
    _sha256(library["artifact_sha256"], "library.artifact_sha256")
    for key in ("manufacturer", "model", "canonical_profile", "transport", "frame"):
        _text(target[key], f"target.{key}")
    if target["frame"] not in FRAME_NAMES[result["protocol"]]:
        raise EvidenceError("target.frame is not canonical for the protocol")
    if target["cpu_firmware"] is not None:
        _text(target["cpu_firmware"], "target.cpu_firmware")
    if host.get("os") != "linux" or host.get("architecture") not in {"x64", "arm64"}:
        raise EvidenceError("host must identify Linux x64 or arm64")
    _text(host["runtime"], "host.runtime")
    _text(timing["started_at"], "timing.started_at")
    _text(timing["finished_at"], "timing.finished_at")
    _number(timing["monotonic_duration_seconds"], "timing.monotonic_duration_seconds")
    for key in SCOPE_KEYS - {"excluded_features", "unconditional_full_feature_claim"}:
        _integer(scope[key], f"scope.{key}")
    if not isinstance(scope["unconditional_full_feature_claim"], bool):
        raise EvidenceError("scope.unconditional_full_feature_claim must be boolean")
    if not isinstance(scope["excluded_features"], list):
        raise EvidenceError("scope.excluded_features must be an array")
    excluded_ids: set[str] = set()
    for item in scope["excluded_features"]:
        exclusion = _object(item, "scope.excluded_features item")
        _exact_keys(exclusion, EXCLUSION_KEYS, EXCLUSION_KEYS, "scope.excluded_features item")
        feature_id = _text(exclusion["feature_id"], "excluded feature_id")
        if feature_id in excluded_ids:
            raise EvidenceError("scope.excluded_features contains a duplicate feature_id")
        excluded_ids.add(feature_id)
        if exclusion["reason_code"] not in EXCLUSION_REASONS:
            raise EvidenceError("invalid excluded feature reason_code")
    if scope["excluded_feature_count"] != len(scope["excluded_features"]):
        raise EvidenceError("scope.excluded_feature_count does not match excluded_features")
    if scope["inventory_covered_count"] > scope["inventory_feature_count"]:
        raise EvidenceError("scope inventory coverage exceeds the feature inventory")
    if result["test_kind"] == "full_feature":
        if (scope["inventory_covered_count"] + scope["excluded_feature_count"]
                != scope["inventory_feature_count"]):
            raise EvidenceError("full-feature scope does not account for every inventory feature")
    elif (scope["inventory_feature_count"] != 0 or scope["inventory_covered_count"] != 0
          or scope["excluded_feature_count"] != 0 or scope["excluded_features"]
          or scope["unconditional_full_feature_claim"]):
        raise EvidenceError("non-full result must not contain a feature-coverage claim")
    if scope["excluded_feature_count"] > 0 and scope["unconditional_full_feature_claim"]:
        raise EvidenceError("excluded features forbid an unconditional full-feature claim")
    if not isinstance(operations, list) or len(operations) != scope["required_case_count"]:
        raise EvidenceError("operation summaries must cover every required case")
    operation_ids: set[str] = set()
    operation_totals = {key: 0 for key in OPERATION_COUNTER_KEYS}
    operation_attempts = 0
    reconnect_attempts = 0
    reconnect_successes = 0
    for value in operations:
        operation = _object(value, "operation summary")
        _exact_keys(operation, OPERATION_KEYS, OPERATION_KEYS, "operation summary")
        case_id = _text(operation["case_id"], "operation summary case_id")
        if case_id in operation_ids:
            raise EvidenceError("operation summary case_id is duplicated")
        operation_ids.add(case_id)
        operation_name, _ = _public_operation_text(
            operation["operation"], operation["public_api"]
        )
        attempts = _integer(operation["attempts"], "operation summary attempts")
        successful_attempts = _integer(
            operation["successful_attempts"], "operation summary successful_attempts"
        )
        if successful_attempts > attempts:
            raise EvidenceError("operation summary successful_attempts exceeds attempts")
        operation_attempts += attempts
        for key in OPERATION_COUNTER_KEYS:
            operation_totals[key] += _integer(operation[key], f"operation summary {key}")
        if operation["successful_requests"] > operation["requests"]:
            raise EvidenceError("operation summary successful_requests exceeds requests")
        latency = _object(operation["latency_ms"], "operation summary latency_ms")
        _exact_keys(latency, {"count", *LATENCY_KEYS}, {"count", *LATENCY_KEYS},
                    "operation summary latency_ms")
        latency_count = _integer(latency["count"], "operation summary latency count")
        latency_values = [_number(latency[key], f"operation summary latency {key}")
                          for key in ("p50", "p95", "p99", "max")]
        if latency_count > operation["requests"] or latency_values != sorted(latency_values):
            raise EvidenceError("operation summary latency is inconsistent")
        if operation_name == "disconnect_reconnect_read":
            reconnect_attempts += attempts
            reconnect_successes += successful_attempts
        if result["verdict"] == "pass" and (
            successful_attempts != attempts
            or operation["successful_requests"] != operation["requests"]
            or latency_count != operation["requests"]
        ):
            raise EvidenceError("passing operation summary is incomplete")
    if operation_attempts != scope["executed_attempt_count"]:
        raise EvidenceError("operation summary attempts do not match scope")
    if result["verdict"] == "pass":
        if scope["executed_case_count"] != scope["required_case_count"]:
            raise EvidenceError("passing result has incomplete cases")
        if result["test_kind"] == "endurance_72h":
            if scope["executed_attempt_count"] < scope["required_attempt_count"]:
                raise EvidenceError("passing endurance result has incomplete minimum attempts")
        elif scope["executed_attempt_count"] != scope["required_attempt_count"]:
            raise EvidenceError("passing result has incomplete attempts")
    for key in TOTAL_KEYS:
        _integer(totals[key], f"totals.{key}")
    for key in OPERATION_COUNTER_KEYS:
        if operation_totals[key] != totals[key]:
            raise EvidenceError(f"operation summary {key} does not match totals")
    if reconnect_attempts != totals["reconnect_attempts"] or reconnect_successes != totals["successful_reconnects"]:
        raise EvidenceError("operation reconnect summaries do not match totals")
    if totals["successful_requests"] > totals["requests"]:
        raise EvidenceError("totals.successful_requests exceeds requests")
    if totals["successful_reconnects"] > totals["reconnect_attempts"]:
        raise EvidenceError("totals.successful_reconnects exceeds reconnect_attempts")
    if result["verdict"] == "pass":
        if totals["successful_requests"] != totals["requests"]:
            raise EvidenceError("passing result contains an unsuccessful request")
        if any(totals[key] != 0 for key in (
            "unexpected_errors", "timeouts", "plc_errors", "decode_errors",
            "readback_mismatches",
        )):
            raise EvidenceError("passing result contains an error or mismatch")
        if totals["successful_reconnects"] != totals["reconnect_attempts"]:
            raise EvidenceError("passing result contains an unsuccessful reconnect")

    if "performance_summary" in result:
        performance = _object(result["performance_summary"], "performance_summary")
        _exact_keys(performance, PERFORMANCE_KEYS, PERFORMANCE_KEYS, "performance_summary")
        _number(performance["throughput_requests_per_second"], "performance throughput")
        latency = _object(performance["latency_ms"], "performance_summary.latency_ms")
        _exact_keys(latency, LATENCY_KEYS, LATENCY_KEYS, "performance_summary.latency_ms")
        latency_values = [_number(latency[key], f"latency_ms.{key}") for key in ("p50", "p95", "p99", "max")]
        if latency_values != sorted(latency_values):
            raise EvidenceError("latency percentiles must satisfy p50 <= p95 <= p99 <= max")
    if "resource_summary" in result:
        resources = _object(result["resource_summary"], "resource_summary")
        _exact_keys(resources, RESOURCE_KEYS, RESOURCE_KEYS, "resource_summary")
        for key in RESOURCE_KEYS:
            _integer(resources[key], f"resource_summary.{key}")
        for start, end, peak in (
            ("rss_start_bytes", "rss_end_bytes", "rss_peak_bytes"),
            ("fd_start", "fd_end", "fd_peak"),
            ("thread_start", "thread_end", "thread_peak"),
        ):
            if resources[peak] < max(resources[start], resources[end]):
                raise EvidenceError(f"resource_summary.{peak} is smaller than start or end")
    if result["test_kind"] == "endurance_72h" and result["verdict"] == "pass":
        if "performance_summary" not in result or "resource_summary" not in result:
            raise EvidenceError("passing endurance result requires performance and resource summaries")
        if timing["monotonic_duration_seconds"] < 259200:
            raise EvidenceError("passing endurance result is shorter than 72 hours")

    _exact_keys(manifest, {"schema_version", "manifest_scope", "run_id", "generated_at", "artifacts"},
                {"schema_version", "manifest_scope", "run_id", "generated_at", "artifacts"}, "manifest")
    if manifest.get("schema_version") != "1.0" or manifest.get("manifest_scope") != "public":
        raise EvidenceError("manifest is not public schema 1.0")
    if manifest.get("run_id") != result.get("run_id"):
        raise EvidenceError("manifest run_id does not match result")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise EvidenceError("manifest.artifacts must be an array")
    if len(artifacts) != 1:
        raise EvidenceError("public docs evidence manifest must contain only validation-result.json")
    result_artifacts = [item for item in artifacts if isinstance(item, dict) and item.get("role") == "validation_result"]
    if len(result_artifacts) != 1:
        raise EvidenceError("manifest must contain exactly one validation_result")
    artifact = result_artifacts[0]
    _exact_keys(artifact, {"role", "path", "media_type", "sha256", "classification"},
                {"role", "path", "media_type", "sha256", "classification"}, "manifest artifact")
    if artifact.get("path") != "validation-result.json" or artifact.get("media_type") != "application/json" or artifact.get("classification") != "public":
        raise EvidenceError("validation_result manifest metadata is invalid")
    if _sha256(artifact.get("sha256"), "manifest artifact sha256") != hashlib.sha256(result_bytes).hexdigest():
        raise EvidenceError("validation-result.json digest does not match manifest")
    return result


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _duration(seconds: float) -> str:
    if seconds >= 3600:
        return f"{seconds / 3600:.2f} h"
    if seconds >= 60:
        return f"{seconds / 60:.1f} min"
    return f"{seconds:.1f} s"


def render(results: list[dict[str, Any]]) -> str:
    lines = [
        "# Real-hardware reliability validation",
        "",
        "This page is generated from hashed public evidence. It is not edited to display",
        "current package versions. An exact version appears only because it identifies the",
        "artifact that was actually tested.",
        "",
        "The result applies only to the listed library artifact, PLC, profile, transport,",
        "frame, and test scope. It does not claim that every feature was tested on every PLC.",
        "",
    ]
    if not results:
        lines += ["No public validation result has been added yet.", ""]
        return "\n".join(lines)

    lines += [
        "| Verdict | Library artifact | PLC / profile | Test | Duration | Requests | Completed |",
        "|---|---|---|---|---:|---:|---|",
    ]
    for result in results:
        library, target, timing, totals = result["library"], result["target"], result["timing"], result["totals"]
        run_id = _cell(result["run_id"])
        lines.append(
            f"| [{_cell(result['verdict']).upper()}](#{run_id}) | "
            f"{_cell(library['name'])} {_cell(library['version'])} | "
            f"{_cell(target['model'])} / `{_cell(target['canonical_profile'])}` | "
            f"{_cell(result['test_kind'])} | {_duration(float(timing['monotonic_duration_seconds']))} | "
            f"{int(totals['requests']):,} | {_cell(timing['finished_at'])} |"
        )
    lines.append("")

    for result in results:
        library, target, host = result["library"], result["target"], result["host"]
        timing, scope, totals = result["timing"], result["scope"], result["totals"]
        lines += [
            f"## {_cell(result['run_id'])}",
            "",
            f"- Verdict: **{_cell(result['verdict']).upper()}** (`{_cell(result['execution_status'])}`)",
            f"- Library: `{_cell(library['name'])}` `{_cell(library['version'])}`; "
            f"{_cell(library['language'])} / {_cell(library['runtime'])}",
            f"- Library artifact SHA-256: `{_cell(library['artifact_sha256'])}`",
            f"- PLC: {_cell(target['manufacturer'])} {_cell(target['model'])}; "
            f"profile `{_cell(target['canonical_profile'])}`; {_cell(target['transport'])} / {_cell(target['frame'])}",
            f"- PLC firmware: {_cell(target['cpu_firmware'] if target['cpu_firmware'] is not None else 'not recorded')}",
            f"- Host: Linux {_cell(host['architecture'])}; runtime {_cell(host['runtime'])}",
            f"- Scope: {int(scope['executed_case_count']):,}/{int(scope['required_case_count']):,} cases, "
            f"{int(scope['executed_attempt_count']):,}/{int(scope['required_attempt_count']):,} attempts",
            f"- Requests: {int(totals['successful_requests']):,}/{int(totals['requests']):,} successful; "
            f"unexpected errors {int(totals['unexpected_errors']):,}; timeouts {int(totals['timeouts']):,}; "
            f"PLC errors {int(totals['plc_errors']):,}; decode errors {int(totals['decode_errors']):,}; "
            f"readback mismatches {int(totals['readback_mismatches']):,}",
            f"- Reconnects: {int(totals['successful_reconnects']):,}/{int(totals['reconnect_attempts']):,} successful",
            f"- Duration: {_duration(float(timing['monotonic_duration_seconds']))}; "
            f"{_cell(timing['started_at'])} to {_cell(timing['finished_at'])}",
        ]
        if result.get("performance_summary"):
            performance = result["performance_summary"]
            latency = performance["latency_ms"]
            lines.append(
                f"- Performance: {float(performance['throughput_requests_per_second']):.2f} requests/s; "
                f"latency p50/p95/p99/max {float(latency['p50']):.3f}/"
                f"{float(latency['p95']):.3f}/{float(latency['p99']):.3f}/{float(latency['max']):.3f} ms"
            )
        if result.get("resource_summary"):
            resource = result["resource_summary"]
            lines.append(
                f"- Process resources: RSS {int(resource['rss_start_bytes']):,}/"
                f"{int(resource['rss_end_bytes']):,}/{int(resource['rss_peak_bytes']):,} bytes start/end/peak; "
                f"FD {int(resource['fd_start']):,}/{int(resource['fd_end']):,}/{int(resource['fd_peak']):,}; "
                f"threads {int(resource['thread_start']):,}/{int(resource['thread_end']):,}/{int(resource['thread_peak']):,}"
            )
        lines += [
            "",
            "| Operation / documented public API | Attempts | Requests | Successful | Errors | Latency p50/p95/p99/max (ms) |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for operation in result["operation_summaries"]:
            latency = operation["latency_ms"]
            errors = sum(int(operation[key]) for key in (
                "unexpected_errors", "timeouts", "plc_errors", "decode_errors", "readback_mismatches"
            ))
            latency_text = "—" if int(latency["count"]) == 0 else (
                f"{float(latency['p50']):.3f}/{float(latency['p95']):.3f}/"
                f"{float(latency['p99']):.3f}/{float(latency['max']):.3f}"
            )
            lines.append(
                f"| `{_cell(operation['operation'])}` / `{_cell(operation['public_api'])}` | "
                f"{int(operation['attempts']):,} | {int(operation['requests']):,} | "
                f"{int(operation['successful_requests']):,} | {errors:,} | {latency_text} |"
            )
        exclusions = scope.get("excluded_features", [])
        if exclusions:
            lines.append("- Approved exclusions: " + ", ".join(
                f"`{_cell(item['feature_id'])}` ({_cell(item['reason_code'])})" for item in exclusions
            ))
        lines.append("")
    return "\n".join(lines)


def generate(input_dir: Path, output: Path, check: bool) -> None:
    results = [load_evidence(path) for path in sorted(input_dir.iterdir()) if path.is_dir()]
    results.sort(key=lambda item: str(item["timing"]["finished_at"]), reverse=True)
    content = render(results)
    if check:
        if not output.exists() or output.read_text(encoding="utf-8") != content:
            raise EvidenceError(f"generated page is stale: {output}")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("evidence/validation-results"))
    parser.add_argument("--output", type=Path, default=Path("docs/quality-validation.md"))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        generate(args.input_dir, args.output, args.check)
    except (EvidenceError, OSError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
