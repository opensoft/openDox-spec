"""The README's contract index, held to the schemas on disk.

Plan 038 T040 adds three schemas, and decision N-15 (opensoft/openxFactory
issue 656, comment 6013547504) makes one of them, the health finding, a shape
the engine reads and not a file kind. The README's "Contracts" section is the
index that says so, one row per schema under `contracts/schemas/`. This module
keeps it level with the tree:

* every schema on disk has exactly one row, and every row names a schema on
  disk, linked by its own path;
* for the schemas this leg reads with the standard library (their bodies are
  JSON), the row's `kind` column is the schema's own `kind` constant, and it
  is "none" for the finding, whose `kind` is a family and never a constant.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SCHEMA_DIR = ROOT / "contracts/schemas"

_ROW = re.compile(r"^\| \[([^\]]+)\]\(([^)]+)\) \| ([^|]+) \| ([^|]+) \|$")


def _rows() -> list[tuple[str, str, str, str]]:
    text = README.read_text(encoding="utf-8")
    start = text.index("\n## Contracts\n")
    end = text.find("\n## ", start + 1)
    section = text[start:] if end == -1 else text[start:end]
    rows = []
    for line in section.splitlines():
        if line.startswith("| ["):
            m = _ROW.fullmatch(line)
            assert m, f"a contract row the index cannot read: {line!r}"
            rows.append(tuple(part.strip() for part in m.groups()))
    return rows  # type: ignore[return-value]


def _json_body(path: Path) -> Any | None:
    """The schema's body, if it is JSON under a `#` header; None for YAML."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    while lines and (lines[0].startswith("#") or not lines[0].strip()):
        lines.pop(0)
    try:
        return json.loads("".join(lines))
    except json.JSONDecodeError:
        return None


def test_every_schema_has_one_row_linked_by_its_own_path() -> None:
    on_disk = sorted(f"contracts/schemas/{p.name}" for p in SCHEMA_DIR.glob("*.schema.yaml"))
    rows = _rows()
    assert [text for text, _target, _what, _kind in rows] == on_disk
    assert all(text == target for text, target, _what, _kind in rows)


def test_the_kind_column_is_the_schemas_own_kind() -> None:
    read = 0
    for _text, target, _what, kind in _rows():
        body = _json_body(ROOT / target)
        if body is None:
            continue
        read += 1
        declared = body.get("properties", {}).get("kind", {}).get("const")
        named = re.findall(r"`([^`]+)`", kind)
        if declared is None:
            assert kind.startswith("none") and not named, (target, kind)
        else:
            assert named == [declared], (target, kind)
    assert read == 4, "the snapshot and the three health schemas are read here"


def test_the_finding_row_says_it_is_not_a_file_kind() -> None:
    """N-15, in the index's own words."""
    kinds = {target: kind for _text, target, _what, kind in _rows()}
    finding = kinds["contracts/schemas/opendox-health-finding.schema.yaml"]
    assert finding == "none: a shape the health engine reads, not a file kind"
