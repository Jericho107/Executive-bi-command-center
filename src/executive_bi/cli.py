from __future__ import annotations

import json
import sys

from .core import ExecutiveRecord, sample, serialise_sample, validate
from .decision import scenario_comparison, write_executive_report


def smoke() -> int:
    payload = serialise_sample()
    payload["stress_test"] = scenario_comparison()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def report() -> int:
    path = write_executive_report("output/executive_command_center.html")
    print(path.as_posix())
    return 0


def reverse_test() -> int:
    cases: list[dict[str, str]] = []

    try:
        rows = sample()
        validate(rows + [rows[0]])
    except ValueError as exc:
        cases.append({"case": "duplicate-grain", "status": "PASS", "error": str(exc)})
    else:
        cases.append({"case": "duplicate-grain", "status": "FAIL", "error": "corruption accepted"})

    try:
        validate([ExecutiveRecord("2026-09", "X", 100, 100, 101, 20, 80, 100, 90, 100)])
    except ValueError as exc:
        cases.append({"case": "impossible-margin", "status": "PASS", "error": str(exc)})
    else:
        cases.append({"case": "impossible-margin", "status": "FAIL", "error": "corruption accepted"})

    scenario = scenario_comparison()
    if any(row["priority_deteriorated"] for row in scenario):
        cases.append({"case": "stress-responsiveness", "status": "PASS", "error": "stress changes risk"})
    else:
        cases.append({"case": "stress-responsiveness", "status": "FAIL", "error": "stress ignored"})

    print(json.dumps(cases, indent=2, sort_keys=True))
    return 0 if all(case["status"] == "PASS" for case in cases) else 1


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    if command == "smoke":
        return smoke()
    if command == "report":
        return report()
    if command == "reverse-test":
        return reverse_test()
    print("usage: python -m executive_bi.cli [smoke|report|reverse-test]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
