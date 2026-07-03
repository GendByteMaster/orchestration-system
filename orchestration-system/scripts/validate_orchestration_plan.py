#!/usr/bin/env python3
"""Validate a JSON orchestration plan."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "objective": str,
    "assumptions": list,
    "workstreams": list,
    "dependencies": list,
    "artifacts": list,
    "validation": list,
    "risks": list,
    "integration": str,
    "stop_conditions": list,
}

REQUIRED_WORKSTREAM = {
    "id": str,
    "role": str,
    "task": str,
    "inputs": list,
    "outputs": list,
    "status": str,
}

VALID_STATUSES = {"pending", "in_progress", "blocked", "complete"}


def load_json(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```json\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1)
    return json.loads(text)


def check_non_empty(value: Any, field: str, errors: list[str]) -> None:
    if isinstance(value, str) and not value.strip():
        errors.append(f"{field} must not be empty")
    if isinstance(value, list) and len(value) == 0:
        errors.append(f"{field} must contain at least one item")


def validate(plan: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["Plan must be a JSON object"]

    for field, expected_type in REQUIRED_TOP_LEVEL.items():
        if field not in plan:
            errors.append(f"Missing top-level field: {field}")
            continue
        if not isinstance(plan[field], expected_type):
            errors.append(f"{field} must be {expected_type.__name__}")
            continue
        check_non_empty(plan[field], field, errors)

    workstreams = plan.get("workstreams", [])
    ids: set[str] = set()
    for index, workstream in enumerate(workstreams):
        prefix = f"workstreams[{index}]"
        if not isinstance(workstream, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field, expected_type in REQUIRED_WORKSTREAM.items():
            if field not in workstream:
                errors.append(f"{prefix} missing field: {field}")
                continue
            if not isinstance(workstream[field], expected_type):
                errors.append(f"{prefix}.{field} must be {expected_type.__name__}")
                continue
            check_non_empty(workstream[field], f"{prefix}.{field}", errors)
        workstream_id = workstream.get("id")
        if isinstance(workstream_id, str):
            if workstream_id in ids:
                errors.append(f"Duplicate workstream id: {workstream_id}")
            ids.add(workstream_id)
        status = workstream.get("status")
        if isinstance(status, str) and status not in VALID_STATUSES:
            errors.append(f"{prefix}.status must be one of: {', '.join(sorted(VALID_STATUSES))}")

    for index, dependency in enumerate(plan.get("dependencies", [])):
        prefix = f"dependencies[{index}]"
        if not isinstance(dependency, dict):
            errors.append(f"{prefix} must be an object")
            continue
        before = dependency.get("before")
        after = dependency.get("after")
        if before not in ids:
            errors.append(f"{prefix}.before references unknown workstream: {before}")
        if after not in ids:
            errors.append(f"{prefix}.after references unknown workstream: {after}")
        if not dependency.get("reason"):
            errors.append(f"{prefix}.reason must not be empty")

    if len(workstreams) > 1 and not plan.get("integration"):
        errors.append("integration is required when multiple workstreams exist")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a JSON orchestration plan.")
    parser.add_argument("plan", type=Path, help="Path to a JSON file or markdown file with a JSON fence.")
    args = parser.parse_args()

    try:
        plan = load_json(args.plan)
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.plan}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate(plan)
    if errors:
        print("Invalid orchestration plan:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Valid orchestration plan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
