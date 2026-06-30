"""Validate fake JSON payloads used by the GTM loop workspace."""

from __future__ import annotations

import json
import sys
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_DIR = WORKSPACE_ROOT / "payloads"


def main() -> int:
    if not PAYLOAD_DIR.exists():
        print(f"Missing payload directory: {PAYLOAD_DIR}")
        return 1

    invalid_files = []
    json_files = sorted(PAYLOAD_DIR.rglob("*.json"))

    if not json_files:
        print(f"No JSON files found in {PAYLOAD_DIR}")
        return 1

    for path in json_files:
        try:
            with path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        except json.JSONDecodeError as exc:
            display_path = path.relative_to(WORKSPACE_ROOT).as_posix()
            invalid_files.append(display_path)
            print(f"INVALID {display_path}: line {exc.lineno}, column {exc.colno}: {exc.msg}")
        else:
            display_path = path.relative_to(WORKSPACE_ROOT).as_posix()
            print(f"VALID   {display_path}")

    if invalid_files:
        print(f"\nInvalid JSON files: {', '.join(invalid_files)}")
        return 1

    print(f"\nValidated {len(json_files)} JSON payloads.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
