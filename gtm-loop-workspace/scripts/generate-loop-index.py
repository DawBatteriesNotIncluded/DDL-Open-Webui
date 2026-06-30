"""Generate an index of loop specs from Markdown files."""

from __future__ import annotations

import re
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
LOOPS_DIR = WORKSPACE_ROOT / "loops"
INDEX_PATH = LOOPS_DIR / "INDEX.md"


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def extract_first_paragraph(text: str) -> str:
    lines = []
    in_heading = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if lines:
                break
            continue
        if line.startswith("#"):
            in_heading = True
            continue
        if in_heading and not line.startswith(("-", "|")):
            lines.append(line)

    return " ".join(lines) if lines else "No summary provided."


def main() -> int:
    loop_files = sorted(
        path
        for path in LOOPS_DIR.glob("*.md")
        if path.name.lower() not in {"readme.md", "index.md"}
    )

    rows = ["# Loop Index", "", "Generated from files in `gtm-loop-workspace/loops`.", ""]

    for path in loop_files:
        text = path.read_text(encoding="utf-8")
        title = extract_title(text, path.stem)
        summary = extract_first_paragraph(text)
        rows.append(f"## [{title}]({path.name})")
        rows.append("")
        rows.append(summary)
        rows.append("")

    INDEX_PATH.write_text("\n".join(rows).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {INDEX_PATH} with {len(loop_files)} loops.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

