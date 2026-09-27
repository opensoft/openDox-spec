"""openDox's neutral snapshot contract, checked by this leg's own gate.

Plan 034 T053 (R1Q11 (a) and R1Q12 (a), ruled on opensoft/openxFactory issue
656, comment 5850003126) gives openDox a snapshot contract of its own,
`contracts/schemas/opendox-snapshot.schema.yaml`: what openDox's neutral
generator writes over a plain repository and what its views read. openXdox's
governed generator keeps `ideation-dashboard-snapshot` in openXdox-spec, which
this leg does not touch.

Nothing else in this leg reads the schema or its examples, so this module is
where the contract's claims become checkable:

* the schema says what the plan asks of it: its kind, the six station role
  keys as stage values, the neutral candidate states and station statuses,
  and the sections it requires;
* every rule has an identifier and every rule can be broken: each negative
  example breaks exactly the rule its `# expected_failure:` line names, at one
  place, and every rule in the `x-rules` catalog has a negative example;
* the positive examples break no rule;
* neither the contract nor any example carries the declared vocabulary that
  #1144's F5.3 refuses in a generated neutral snapshot.

WHY A SMALL EVALUATOR LIVES HERE. The required `validate` check installs pytest
and nothing else, so this module evaluates, with the standard library, exactly
the JSON Schema keywords the contract uses. A keyword the contract starts to use
and this evaluator does not know fails `test_the_evaluator_knows_every_keyword`
instead of passing unread. Where `jsonschema` and PyYAML are installed, the two
tests at the end hold this evaluator to them: the same rule identifiers at the
same places for every example, and the same parsed object for every file. In
the required check they skip, and a local run with both installed is how a
change to the contract is shown to keep them in agreement.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path
from typing import Any, Callable, Iterator, NamedTuple

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts/schemas/opendox-snapshot.schema.yaml"
EXAMPLES = ROOT / "examples/ideation-dashboard"
POSITIVE = sorted(EXAMPLES.glob("opendox-snapshot-*.example.yaml"))
NEGATIVE = sorted((EXAMPLES / "negative").glob("opendox-snapshot-*.negative.yaml"))

#: openDox-code's `display_profile.STAGE_ROLES`, in spine order. T053: "Its
#: stage values are the six role keys."
STAGE_ROLES = ["source", "grouping", "candidate", "selection", "submission", "completion"]
#: NEUTRAL_DISPLAY's candidate words, as the candidate station's machine values.
CANDIDATE_STATES = ["unselected", "selected", "declined", "replaced"]
#: openDox-code's `display_profile.STAGE_FIELDS`: the two change stations' status.
SUBMISSION_STATUSES = ["active", "archived"]
#: What the neutral projection writes (T054), every station's section among it.
REQUIRED = ["schema_version", "kind", "repository", "generation",
            "documents", "clusters", "possibles", "staged_topics", "changes"]

#: #1144's F5.3 word list, verbatim, and its own pattern over it.
DECLARED_WORDS = ["brainstorm", "staged", "draft", "ratified", "standard", "superseded",
                  "retired", "record", "openspec", "proposal.md", "tasks.md", "design.md",
                  "added requirements", "modified requirements"]
_DECLARED = re.compile(r"\b(" + "|".join(re.escape(w) for w in DECLARED_WORDS) + r")\b")
#: The one exempted string: the JSON Schema dialect's own URI, which spells a
#: declared word and is not vocabulary.
DIALECT = "https://json-schema.org/draft/2020-12/schema"


# ---------------------------------------------------------------------------
# reading a file: a `#` comment header, then one JSON value
# ---------------------------------------------------------------------------

def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """`json` keeps the LAST of two equal keys without a word, which would drop
    a declaration from the contract in silence. A repeated key is refused."""
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"the key {key!r} appears twice in one object")
        out[key] = value
    return out


def _no_constants(name: str) -> Any:
    """`json` reads NaN, Infinity and -Infinity, which JSON does not define and
    PyYAML reads as text. A body that spells one is refused."""
    raise ValueError(f"{name} is not JSON")


def read(path: Path) -> tuple[list[str], Any]:
    """The comment header's lines and the parsed JSON body of `path`."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    header: list[str] = []
    while lines and (lines[0].startswith("#") or not lines[0].strip()):
        header.append(lines.pop(0).rstrip("\n"))
    return header, json.loads("".join(lines), object_pairs_hook=_no_duplicate_keys,
                              parse_constant=_no_constants)


SCHEMA = read(SCHEMA_PATH)[1]


# ---------------------------------------------------------------------------
# the evaluator: exactly the keywords the contract uses, as JSON Schema 2020-12
# defines them
# ---------------------------------------------------------------------------

#: The keywords that can FAIL, and that this evaluator evaluates.
CONSTRAINING = frozenset({"type", "const", "enum", "required", "minLength", "minItems",
                          "uniqueItems", "minimum", "pattern"})
#: `format` can fail too, but only under a validator that asserts it (as
#: `jsonschema` does with its format checker). This evaluator leaves it to the
#: `pattern` beside it: `test_a_format_travels_with_its_pattern` holds the pair.
MAY_FAIL = CONSTRAINING | {"format"}
#: The keywords that only carry, annotate or route.
CARRYING = frozenset({"$schema", "$id", "$ref", "$defs", "title", "description",
                      "contract_schema_version", "x-rule", "x-rules", "format",
                      "properties", "items", "allOf", "if", "then"})


class Violation(NamedTuple):
    rule: str       # the broken rule's id, from `x-rule` or a reference check
    where: str      # a JSON pointer into the instance ("" is the root)
    keyword: str    # the schema keyword that failed, or "reference"
    detail: str


def _pointer(parts: Any) -> str:
    return "".join("/" + str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def _is_type(value: Any, name: str) -> bool:
    if name == "object":
        return isinstance(value, dict)
    if name == "array":
        return isinstance(value, list)
    if name == "string":
        return isinstance(value, str)
    if name == "null":
        return value is None
    if name == "boolean":
        return isinstance(value, bool)
    if isinstance(value, bool):          # JSON true is not the number 1
        return False
    if name == "integer":
        return isinstance(value, int) or (isinstance(value, float) and value.is_integer())
    if name == "number":
        return isinstance(value, (int, float))
    raise AssertionError(f"the contract names a type this evaluator does not know: {name!r}")


def _canon(value: Any) -> Any:
    """JSON equality: `true` is not `1`, `1` is `1.0`, and key order is noise."""
    if isinstance(value, bool):
        return ("boolean", value)
    if isinstance(value, (int, float)):
        return ("number", value)
    if isinstance(value, str):
        return ("string", value)
    if value is None:
        return ("null",)
    if isinstance(value, list):
        return ("array", tuple(_canon(v) for v in value))
    return ("object", tuple(sorted((k, _canon(v)) for k, v in value.items())))


def _resolve(ref: str) -> dict[str, Any]:
    assert ref.startswith("#/"), f"only local references are part of the contract: {ref!r}"
    node: Any = SCHEMA
    for part in ref[2:].split("/"):
        node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def _check(value: Any, schema: dict[str, Any], where: str) -> Iterator[Violation]:
    if "$ref" in schema:
        yield from _check(value, _resolve(schema["$ref"]), where)
    rule = schema.get("x-rule", "<no rule named>")

    def broken(keyword: str, detail: str) -> Violation:
        return Violation(rule, where, keyword, detail)

    if "type" in schema:
        names = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_is_type(value, n) for n in names):
            yield broken("type", f"{value!r} is not of type {names}")
    if "const" in schema and _canon(value) != _canon(schema["const"]):
        yield broken("const", f"{value!r} is not {schema['const']!r}")
    if "enum" in schema and _canon(value) not in {_canon(v) for v in schema["enum"]}:
        yield broken("enum", f"{value!r} is not one of {schema['enum']}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            yield broken("minLength", f"{value!r} is shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            yield broken("pattern", f"{value!r} does not match the rule's pattern")
    if _is_type(value, "number") and "minimum" in schema and value < schema["minimum"]:
        yield broken("minimum", f"{value!r} is less than {schema['minimum']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            yield broken("minItems", f"{len(value)} items, fewer than {schema['minItems']}")
        if schema.get("uniqueItems") and len({_canon(v) for v in value}) != len(value):
            yield broken("uniqueItems", f"{value!r} repeats an item")
        if "items" in schema:
            for i, item in enumerate(value):
                yield from _check(item, schema["items"], f"{where}/{i}")
    if isinstance(value, dict):
        for key in schema.get("required", ()):
            if key not in value:
                yield broken("required", f"{key!r} is required")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                yield from _check(value[key], sub, where + _pointer([key]))
    for sub in schema.get("allOf", ()):
        yield from _check(value, sub, where)
    # `if` is a test, never a failure: it only chooses whether `then` applies.
    if "if" in schema and "then" in schema:
        if not any(True for _ in _check(value, schema["if"], where)):
            yield from _check(value, schema["then"], where)


def shape_violations(instance: Any) -> list[Violation]:
    return list(_check(instance, SCHEMA, ""))


# ---------------------------------------------------------------------------
# the reference rules: the cross-references no JSON Schema keyword can state
# ---------------------------------------------------------------------------

def _entries(snap: Any, section: str) -> list[tuple[int, dict[str, Any]]]:
    items = snap.get(section) if isinstance(snap, dict) else None
    if not isinstance(items, list):
        return []
    return [(i, e) for i, e in enumerate(items) if isinstance(e, dict)]


def _ids(snap: Any, section: str, key: str = "id") -> set[str]:
    return {e[key] for _i, e in _entries(snap, section) if isinstance(e.get(key), str)}


def _ids_are_unique(snap: Any) -> Iterator[Violation]:
    for section, key in (("documents", "id"), ("clusters", "id"), ("possibles", "id"),
                         ("staged_topics", "staging_id"), ("changes", "id")):
        seen: set[str] = set()
        for i, entry in _entries(snap, section):
            value = entry.get(key)
            if isinstance(value, str):
                if value in seen:
                    yield Violation("ids-are-unique", f"/{section}/{i}/{key}", "reference",
                                    f"{value!r} is already an id in {section}")
                seen.add(value)


def _edge_names_a_document(snap: Any) -> Iterator[Violation]:
    known = _ids(snap, "documents")
    for gi, group in _entries(snap, "clusters"):
        edges = group.get("document_edges")
        for ei, edge in enumerate(edges if isinstance(edges, list) else []):
            ref = edge.get("document") if isinstance(edge, dict) else None
            if isinstance(ref, str) and ref not in known:
                yield Violation("edge-names-a-document",
                                f"/clusters/{gi}/document_edges/{ei}/document", "reference",
                                f"no document has the id {ref!r}")


def _one_edge_per_document(snap: Any) -> Iterator[Violation]:
    for gi, group in _entries(snap, "clusters"):
        edges = group.get("document_edges")
        seen: set[str] = set()
        for ei, edge in enumerate(edges if isinstance(edges, list) else []):
            ref = edge.get("document") if isinstance(edge, dict) else None
            if isinstance(ref, str):
                if ref in seen:
                    yield Violation("one-edge-per-document",
                                    f"/clusters/{gi}/document_edges/{ei}/document", "reference",
                                    f"{ref!r} already has an edge in this group")
                seen.add(ref)


def _keyword_index_matches_topics(snap: Any) -> Iterator[Violation]:
    """Present, the index never contradicts the documents, so a reader that
    seeds its rail from it sees what the documents say: every topic they carry
    has one entry, and every entry counts the documents that carry its keyword.
    An entry for a keyword no document carries is lawful at 0, which leaves
    room for a later count of another kind without reopening this rule."""
    index = snap.get("keyword_index") if isinstance(snap, dict) else None
    if not isinstance(index, list):
        return                  # absent is lawful; not a list is section-is-a-list's
    carried: dict[str, int] = {}
    for _i, document in _entries(snap, "documents"):
        topics = document.get("topics")
        for topic in {t for t in topics if isinstance(t, str)} if isinstance(topics, list) else ():
            carried[topic] = carried.get(topic, 0) + 1
    listed: set[str] = set()
    rule = "keyword-index-matches-topics"
    for ki, entry in enumerate(index):
        keyword = entry.get("keyword") if isinstance(entry, dict) else None
        if not isinstance(keyword, str):
            continue            # keyword-entry-keys and topic-is-trimmed-text say why
        if keyword in listed:
            yield Violation(rule, f"/keyword_index/{ki}/keyword", "reference",
                            f"{keyword!r} already has an entry")
            continue
        listed.add(keyword)
        count = entry.get("declared_doc_count")
        if _is_type(count, "integer") and count != carried.get(keyword, 0):
            yield Violation(rule, f"/keyword_index/{ki}/declared_doc_count", "reference",
                            f"{count} documents, but {carried.get(keyword, 0)} carry {keyword!r}")
    unlisted = sorted(set(carried) - listed)
    if unlisted:
        yield Violation(rule, "/keyword_index", "reference",
                        f"topics the documents carry and the index does not list: {unlisted}")


def _candidate_names_a_group(snap: Any) -> Iterator[Violation]:
    known = _ids(snap, "clusters")
    for pi, candidate in _entries(snap, "possibles"):
        refs = candidate.get("claiming_clusters")
        for ri, ref in enumerate(refs if isinstance(refs, list) else []):
            if isinstance(ref, str) and ref not in known:
                yield Violation("candidate-names-a-group",
                                f"/possibles/{pi}/claiming_clusters/{ri}", "reference",
                                f"no group has the id {ref!r}")


def _pick_names_a_selection(snap: Any) -> Iterator[Violation]:
    known = _ids(snap, "staged_topics", "staging_id")
    for pi, candidate in _entries(snap, "possibles"):
        pick = candidate.get("pick")
        ref = pick.get("staging_id") if isinstance(pick, dict) else None
        if isinstance(ref, str) and ref not in known:
            yield Violation("pick-names-a-selection", f"/possibles/{pi}/pick/staging_id",
                            "reference", f"no selection has the staging_id {ref!r}")


def _target_names_a_submission(snap: Any) -> Iterator[Violation]:
    known = _ids(snap, "changes")
    for ti, selection in _entries(snap, "staged_topics"):
        ref = selection.get("target_change")
        if isinstance(ref, str) and ref not in known:
            yield Violation("target-names-a-submission", f"/staged_topics/{ti}/target_change",
                            "reference", f"no changes entry has the id {ref!r}")


REFERENCE_CHECKS: dict[str, Callable[[Any], Iterator[Violation]]] = {
    "ids-are-unique": _ids_are_unique,
    "edge-names-a-document": _edge_names_a_document,
    "one-edge-per-document": _one_edge_per_document,
    "candidate-names-a-group": _candidate_names_a_group,
    "pick-names-a-selection": _pick_names_a_selection,
    "target-names-a-submission": _target_names_a_submission,
    "keyword-index-matches-topics": _keyword_index_matches_topics,
}


def violations(instance: Any) -> list[Violation]:
    found = shape_violations(instance)
    for check in REFERENCE_CHECKS.values():
        found.extend(check(instance))
    return found


# ---------------------------------------------------------------------------
# walking the schema
# ---------------------------------------------------------------------------

def _subschemas(node: Any, at: str = "", *, tests: bool = False
                ) -> Iterator[tuple[str, dict[str, Any]]]:
    """Every subschema that can produce a failure, with its location. An `if`
    is a test that never fails, so it and what is inside it are skipped, unless
    `tests` asks for them too (to check that every keyword is one evaluated)."""
    if not isinstance(node, dict):
        return
    yield at, node
    for key in ("properties", "$defs"):
        for name, sub in node.get(key, {}).items():
            yield from _subschemas(sub, f"{at}/{key}/{name}", tests=tests)
    for key in ("items", "then", "if") if tests else ("items", "then"):
        if key in node:
            yield from _subschemas(node[key], f"{at}/{key}", tests=tests)
    for i, sub in enumerate(node.get("allOf", ())):
        yield from _subschemas(sub, f"{at}/allOf/{i}", tests=tests)


CATALOG: dict[str, dict[str, Any]] = {rule["id"]: rule for rule in SCHEMA["x-rules"]}


def _expected_failure(path: Path) -> str:
    header = read(path)[0]
    named = [m.group(1) for line in header
             if (m := re.fullmatch(r"# expected_failure: (\S+)\s*", line))]
    assert len(named) == 1, f"{path.name} must name exactly one expected_failure: {named}"
    return named[0]


# ---------------------------------------------------------------------------
# the contract says what the plan asks of it
# ---------------------------------------------------------------------------

def test_the_schema_identifies_itself() -> None:
    assert SCHEMA["$schema"] == DIALECT
    assert SCHEMA["$id"] == SCHEMA_PATH.name
    assert SCHEMA["contract_schema_version"] == 1
    assert SCHEMA["properties"]["schema_version"]["const"] == 1
    # openDox's own kind, and not the governed generator's.
    assert SCHEMA["properties"]["kind"]["const"] == "opendox-snapshot"


def test_the_stage_values_are_the_six_role_keys() -> None:
    stage = SCHEMA["$defs"]["document"]["properties"]["stage"]
    assert stage == {"$ref": "#/$defs/stage_role"}
    assert SCHEMA["$defs"]["stage_role"]["enum"] == STAGE_ROLES


def test_the_candidate_and_submission_values_are_neutral() -> None:
    assert SCHEMA["$defs"]["candidate_state"]["enum"] == CANDIDATE_STATES
    assert SCHEMA["$defs"]["submission_status"]["enum"] == SUBMISSION_STATUSES


def test_it_requires_the_station_sections_and_no_more() -> None:
    assert SCHEMA["required"] == REQUIRED
    assert set(SCHEMA["properties"]) == set(REQUIRED) | {"keyword_index"}


def test_it_is_forward_compatible() -> None:
    """A reader ignores unknown properties, so no object closes itself: an
    additive field needs no `schema_version` bump."""
    closed = [at or "<root>" for at, node in _subschemas(SCHEMA)
              if "additionalProperties" in node or "unevaluatedProperties" in node]
    assert not closed, f"objects that refuse unknown properties: {closed}"


def test_the_evaluator_knows_every_keyword() -> None:
    unknown = {(at, key) for at, node in _subschemas(SCHEMA, tests=True) for key in node
               if key not in CONSTRAINING | CARRYING}
    assert not unknown, f"keywords this module does not evaluate: {sorted(unknown)}"


def test_a_format_travels_with_its_pattern() -> None:
    """This evaluator does not assert `format`, so the leg's own gate would
    miss a `format` that stood alone. Each one stands beside a `pattern` that
    says the same thing, and the pattern is what the required check asserts."""
    alone = [at for at, node in _subschemas(SCHEMA) if "format" in node and "pattern" not in node]
    assert not alone, f"a format with no pattern beside it: {alone}"


# ---------------------------------------------------------------------------
# every rule has an identifier, and the catalog is the rules
# ---------------------------------------------------------------------------

def test_every_rule_in_the_catalog_is_declared_once() -> None:
    ids = [rule["id"] for rule in SCHEMA["x-rules"]]
    assert len(ids) == len(set(ids)), "a rule id is catalogued twice"
    for rule in SCHEMA["x-rules"]:
        assert set(rule) == {"id", "class", "says"}, rule
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", rule["id"]), rule["id"]
        assert rule["class"] in ("shape", "reference"), rule
        assert rule["says"].strip(), rule


def test_every_subschema_that_can_fail_names_a_catalogued_shape_rule() -> None:
    for at, node in _subschemas(SCHEMA):
        if MAY_FAIL & set(node):
            assert "x-rule" in node, f"{at or '<root>'} can fail and names no rule"
        if "x-rule" in node:
            assert node["x-rule"] in CATALOG, f"{at}: {node['x-rule']!r} is not catalogued"
            assert CATALOG[node["x-rule"]]["class"] == "shape", (
                f"{at}: {node['x-rule']!r} is a reference rule; no keyword enforces it")


def test_every_shape_rule_is_enforced_somewhere() -> None:
    enforced = {node["x-rule"] for _at, node in _subschemas(SCHEMA) if "x-rule" in node}
    shape = {rid for rid, rule in CATALOG.items() if rule["class"] == "shape"}
    assert shape == enforced


def test_every_reference_rule_is_checked_here() -> None:
    reference = {rid for rid, rule in CATALOG.items() if rule["class"] == "reference"}
    assert reference == set(REFERENCE_CHECKS)


# ---------------------------------------------------------------------------
# the examples
# ---------------------------------------------------------------------------

def test_the_examples_exist() -> None:
    assert [p.name for p in POSITIVE] == [
        "opendox-snapshot-no-front-matter.example.yaml",
        "opendox-snapshot-six-stations.example.yaml"]
    assert len(NEGATIVE) == len(CATALOG)


@pytest.mark.parametrize("path", POSITIVE, ids=lambda p: p.name)
def test_a_positive_example_breaks_no_rule(path: Path) -> None:
    found = violations(read(path)[1])
    assert not found, "\n".join(f"[{v.rule}] {v.where or '<root>'}: {v.detail}" for v in found)


@pytest.mark.parametrize("path", NEGATIVE, ids=lambda p: p.name)
def test_a_negative_example_breaks_its_rule_and_no_other(path: Path) -> None:
    expected = _expected_failure(path)
    assert path.name == f"opendox-snapshot-{expected}.negative.yaml"
    found = violations(read(path)[1])
    assert {v.rule for v in found} == {expected}, (
        f"{path.name} names {expected!r} and breaks "
        + "; ".join(f"[{v.rule}] {v.where or '<root>'}: {v.detail}" for v in found))
    assert len({v.where for v in found}) == 1, f"{path.name} breaks its rule in two places"


def test_every_rule_has_a_negative_example() -> None:
    assert sorted(_expected_failure(p) for p in NEGATIVE) == sorted(CATALOG)


def test_the_six_station_example_fills_every_station() -> None:
    snap = read(EXAMPLES / "opendox-snapshot-six-stations.example.yaml")[1]
    assert {d["stage"] for d in snap["documents"]} == set(STAGE_ROLES)
    assert {p["state"] for p in snap["possibles"]} == set(CANDIDATE_STATES)
    assert snap["clusters"], "the grouping station is empty"
    assert snap["staged_topics"], "the selection station is empty"
    assert {c["status"] for c in snap["changes"]} == set(SUBMISSION_STATUSES)
    # one-edge-per-document holds within a group: a document feeds several.
    fed = [e["document"] for c in snap["clusters"] for e in c["document_edges"]]
    assert len(fed) > len(set(fed)), "no document feeds two groups"


SIX_INDEX = [{"keyword": "compost", "declared_doc_count": 3},
             {"keyword": "reuse", "declared_doc_count": 3},
             {"keyword": "soil", "declared_doc_count": 1},
             {"keyword": "tools", "declared_doc_count": 1},
             {"keyword": "water", "declared_doc_count": 4}]


@pytest.mark.parametrize("change, where", [
    ("keeps the example's own index", set()),
    ("adds moss, which no document carries, at 0", set()),
    ("adds moss, which no document carries, at 1", {"/keyword_index/5/declared_doc_count"}),
    ("drops soil, which a document carries", {"/keyword_index"}),
    ("gives compost a second entry", {"/keyword_index/5/keyword"}),
    ("counts water at 3 where 4 documents carry it", {"/keyword_index/4/declared_doc_count"}),
    ("counts water in words", set()),
], ids=lambda v: v if isinstance(v, str) else "")
def test_the_keyword_index_agrees_with_the_documents(change: str, where: set[str]) -> None:
    """keyword-index-matches-topics, branch by branch, over the six-station
    example's documents. A count in words is keyword-entry-keys' to refuse."""
    snap = read(EXAMPLES / "opendox-snapshot-six-stations.example.yaml")[1]
    assert snap["keyword_index"] == SIX_INDEX
    index = [dict(e) for e in SIX_INDEX]
    if "moss" in change:
        index.append({"keyword": "moss", "declared_doc_count": 1 if change.endswith("1") else 0})
    elif "drops soil" in change:
        index = [e for e in index if e["keyword"] != "soil"]
    elif "second entry" in change:
        index.append({"keyword": "compost", "declared_doc_count": 3})
    elif "at 3" in change:
        index[4]["declared_doc_count"] = 3
    elif "in words" in change:
        index[4]["declared_doc_count"] = "four"
    snap["keyword_index"] = index
    found = list(_keyword_index_matches_topics(snap))
    assert {v.where for v in found} == where, found
    assert all(v.rule == "keyword-index-matches-topics" for v in found)


def test_a_document_carries_its_topics() -> None:
    """document-keys requires topics, as it requires stage: every entry carries
    what the generator assigned, an empty list when that is nothing, so no
    reader supplies a default."""
    snap = read(EXAMPLES / "opendox-snapshot-no-front-matter.example.yaml")[1]
    document = dict(snap["documents"][0])
    assert not list(_check(document, _resolve("#/$defs/document"), ""))
    assert not list(_check({**document, "topics": []}, _resolve("#/$defs/document"), ""))
    del document["topics"]
    found = list(_check(document, _resolve("#/$defs/document"), ""))
    assert [(v.rule, v.keyword) for v in found] == [("document-keys", "required")], found


def test_the_no_front_matter_example_is_the_smallest_shape() -> None:
    """AT-R1's plain repository: every document a source, at least one group
    (the tile the chat pane opens from), and every other station empty."""
    snap = read(EXAMPLES / "opendox-snapshot-no-front-matter.example.yaml")[1]
    assert sorted(snap) == sorted(REQUIRED)
    assert {d["stage"] for d in snap["documents"]} == {"source"}
    assert snap["clusters"]
    assert snap["possibles"] == snap["staged_topics"] == snap["changes"] == []


#: The pattern rules' table, value by value: `(rule, value, admitted)`. It is
#: read here, and again through a browser's regex engine below.
PATTERN_CASES: list[tuple[str, str, bool]] = [
        ("path-is-repo-relative", "notes/soil-test.md", True),
        ("path-is-repo-relative", "a..b/c.md", True),
        ("path-is-repo-relative", "/notes/soil-test.md", False),
        ("path-is-repo-relative", "../notes.md", False),
        ("path-is-repo-relative", "notes/../soil.md", False),
        ("path-is-repo-relative", "notes/..", False),
        ("path-is-repo-relative", "notes\\soil.md", False),
        ("path-is-repo-relative", "notes/soil.md\n", False),
        ("path-is-repo-relative", "", False),
        # every control character is refused, DEL and C1 as well as C0
        ("path-is-repo-relative", "notes/a\u007fb.md", False),
        ("path-is-repo-relative", "notes/a\u0085b.md", False),
        ("path-is-repo-relative", "notes/a\u009fb.md", False),
        ("path-is-repo-relative", "notes/caf\u00e9.md", True),
    # a drive letter and a colon: Windows joins it onto a root as a path outside it
    ("path-is-repo-relative", "C:/outside.txt", False),
    ("path-is-repo-relative", "C:outside.txt", False),
    ("path-is-repo-relative", "c:/outside.txt", False),
    ("path-is-repo-relative", "notes/C:/inside.md", True),
        ("topic-is-trimmed-text", "two words", True),
        ("topic-is-trimmed-text", " leading", False),
        ("topic-is-trimmed-text", "trailing ", False),
        ("topic-is-trimmed-text", "newline\n", False),
        ("topic-is-trimmed-text", "tab\there", False),
        ("topic-is-trimmed-text", "", False),
        ("topic-is-trimmed-text", "bre\u007fad", False),
        ("topic-is-trimmed-text", "bread\u0085", False),
        # U+FEFF is whitespace to a browser and not to Python: named, so both refuse it
        ("topic-is-trimmed-text", "\ufeffbread", False),
        ("topic-is-trimmed-text", "bread\u00a0", False),
        ("topic-is-trimmed-text", "two\u00a0words", True),
        ("generated-at-is-rfc3339", "2026-09-27T12:00:00Z", True),
        ("generated-at-is-rfc3339", "2026-09-27t12:00:00.25+05:30", True),
        ("generated-at-is-rfc3339", "2024-02-29T00:00:00Z", True),
        ("generated-at-is-rfc3339", "2000-02-29T00:00:00Z", True),
        ("generated-at-is-rfc3339", "2026-09-27", False),
        ("generated-at-is-rfc3339", "2026-09-27T12:00:00", False),
        ("generated-at-is-rfc3339", "27 September 2026", False),
        ("generated-at-is-rfc3339", "2026-13-27T12:00:00Z", False),
        ("generated-at-is-rfc3339", "2026-02-31T12:00:00Z", False),
        ("generated-at-is-rfc3339", "2026-04-31T12:00:00Z", False),
        ("generated-at-is-rfc3339", "2026-02-29T12:00:00Z", False),
        ("generated-at-is-rfc3339", "1900-02-29T12:00:00Z", False),
        ("generated-at-is-rfc3339", "2026-09-27T24:00:00Z", False),
        ("generated-at-is-rfc3339", "2016-12-31T23:59:59Z", True),
    # year 0000 is RFC 3339's and not this contract's: Python's datetime cannot hold it
    ("generated-at-is-rfc3339", "0000-01-01T00:00:00Z", False),
    ("generated-at-is-rfc3339", "0000-02-29T00:00:00Z", False),
    ("generated-at-is-rfc3339", "0001-01-01T00:00:00Z", True),
        # RFC 3339 allows a leap second's 60, and this contract does not: a git
        # commit date cannot hold one, and neither Python nor a browser reads one.
        ("generated-at-is-rfc3339", "2016-12-31T23:59:60Z", False),
        ("generated-at-is-rfc3339", "2026-09-27T12:00:00Z\n", False),
]


def _pattern_of(rule: str) -> str:
    return {"path-is-repo-relative": _resolve("#/$defs/path"),
            "topic-is-trimmed-text": _resolve("#/$defs/topic"),
            "generated-at-is-rfc3339":
                SCHEMA["$defs"]["generation"]["properties"]["generated_at"]}[rule]["pattern"]


@pytest.mark.parametrize("rule, value, admitted", PATTERN_CASES)
def test_a_pattern_rule_admits_and_refuses(rule: str, value: str, admitted: bool) -> None:
    """The pattern rules, value by value. Each pattern guards its own tail with
    a lookahead, because a Python `$` also matches before a final newline and an
    ECMA-262 `$` does not: a pattern that relied on `$` would admit
    `...md\\n` here and refuse it in a browser."""
    subschema = {"path-is-repo-relative": _resolve("#/$defs/path"),
                 "topic-is-trimmed-text": _resolve("#/$defs/topic"),
                 "generated-at-is-rfc3339":
                     SCHEMA["$defs"]["generation"]["properties"]["generated_at"]}[rule]
    found = list(_check(value, subschema, ""))
    assert (not found) is admitted, found
    assert {v.rule for v in found} <= {rule}


#: The characters where Python's and a browser's regex engines could part:
#: every control, every character either engine counts as whitespace, the
#: zero-width and invisible neighbours of those, and two ordinary letters.
_EDGE_CHARACTERS = [*range(0x00, 0xA1), 0x1680, 0x180E, *range(0x2000, 0x2010),
                    *range(0x2028, 0x2030), 0x205F, 0x2060, 0x3000, 0xFEFF, 0xFFFE, 0x10FFFF]


def test_a_browser_reads_every_pattern_as_python_does() -> None:
    """A JSON Schema pattern is an ECMA-262 regular expression, and openDox's
    views run in a browser, so a pattern must give a browser's engine the
    verdict it gives Python's. Node's RegExp with the `u` flag, which is how
    JSON Schema validators in JavaScript compile a pattern, reads the pattern
    table and a sweep of the characters where the two engines could part:
    each one leading, trailing and inside a topic, and inside a path."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed; validate.yml installs it")
    cases = [(_pattern_of(rule), value) for rule, value, _admitted in PATTERN_CASES]
    for code in _EDGE_CHARACTERS:
        ch = chr(code)
        cases += [(_pattern_of("topic-is-trimmed-text"), v) for v in (f"x{ch}", f"{ch}x", f"a{ch}b")]
        cases.append((_pattern_of("path-is-repo-relative"), f"n/a{ch}b.md"))
    script = ("const c = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
              "process.stdout.write(JSON.stringify(c.map(([p, v]) => new RegExp(p, 'u').test(v))));")
    run = subprocess.run([node, "-e", script], input=json.dumps(cases), capture_output=True,
                         text=True, check=True)
    theirs = json.loads(run.stdout)
    parted = [(p[:24], v, ours) for (p, v), ours, js in
              zip(cases, (bool(re.search(p, v)) for p, v in cases), theirs) if ours is not js]
    assert not parted, f"Python and a browser read these differently: {parted[:10]}"


@pytest.mark.parametrize("body", ['{"a": NaN}', '{"a": Infinity}', '{"a": -Infinity}',
                                  '{"a": 1, "a": 2}'],
                         ids=["NaN", "Infinity", "-Infinity", "a repeated key"])
def test_the_reader_refuses_what_json_does_not_mean(tmp_path: Path, body: str) -> None:
    """The reader is strict where Python's `json` is lenient. It refuses the
    constants JSON does not define, which PyYAML would read as text, and a key
    repeated in one object, which `json` would drop in silence."""
    path = tmp_path / "body.yaml"
    path.write_text(f"# a header line\n{body}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read(path)


@pytest.mark.parametrize("station, entry, keys", [
    ("selection", {"staging_id": "loaf-club"}, "selection-keys"),
    ("submission", {"id": "bake-sale", "status": "active"}, "submission-keys"),
], ids=["selection", "submission"])
@pytest.mark.parametrize("files, broken", [
    (["notes/a.md", "notes/b.md"], set()),
    (["notes/a.md", "notes/a.md"], {"keys"}),
    (["/notes/a.md"], {"path-is-repo-relative"}),
    ("notes/a.md", {"keys"}),
], ids=["two paths", "a path twice", "an absolute path", "not a list"])
def test_a_files_list_names_repository_paths_once(
        station: str, entry: dict[str, Any], keys: str, files: Any, broken: set[str]) -> None:
    """A selection's files and a changes entry's files take one shape: repository-
    relative paths, each once. The tile that opens onto them lists them as given."""
    found = list(_check({**entry, "files": files}, _resolve(f"#/$defs/{station}"), ""))
    assert {v.rule for v in found} == {keys if b == "keys" else b for b in broken}, found


@pytest.mark.parametrize("count, admitted", [
    (0, True), (2, True), (2.0, True),
    (-1, False), ("one", False), (True, False), (1.5, False), (None, False),
], ids=repr)
def test_a_keyword_entry_counts_in_whole_numbers(count: Any, admitted: bool) -> None:
    """keyword-entry-keys on the count alone: a whole number no less than 0,
    where JSON's 2.0 is the number 2 and JSON's true is not the number 1. Only
    this table holds `minimum`, because a negative count in a snapshot is also a
    count that keyword-index-matches-topics refuses."""
    found = list(_check({"keyword": "bread", "declared_doc_count": count},
                        _resolve("#/$defs/keyword_entry"), ""))
    assert (not found) is admitted, found
    assert {v.rule for v in found} <= {"keyword-entry-keys"}


def test_the_timestamp_pattern_knows_the_calendar() -> None:
    """The pattern, not `format`, is what the required check asserts, so the
    pattern carries the calendar: each month's length and the leap years. It is
    held here to Python's own calendar, day by day, over every month of years
    chosen for their leap rules: ordinary, divisible by 4, by 100 and by 400."""
    pattern = SCHEMA["$defs"]["generation"]["properties"]["generated_at"]["pattern"]
    wrong = []
    for year in (1, 4, 100, 400, 1600, 1700, 1800, 1900, 1996, 1999, 2000, 2023, 2024,
                 2025, 2026, 2100, 2400, 9996, 9999):
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    date(year, month, day)
                    real = True
                except ValueError:
                    real = False
                stamp = f"{year:04d}-{month:02d}-{day:02d}T00:00:00Z"
                if bool(re.search(pattern, stamp)) is not real:
                    wrong.append(stamp)
    assert not wrong, f"the pattern and the calendar disagree on {wrong[:10]}"


# ---------------------------------------------------------------------------
# the declared vocabulary stays out
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("path", [SCHEMA_PATH, *POSITIVE, *NEGATIVE], ids=lambda p: p.name)
def test_no_file_carries_the_declared_vocabulary(path: Path) -> None:
    """F5.3's words, by F5.3's own pattern, over each WHOLE file: its comment
    header, its keys and its values. A neutral contract and its fixtures that
    spelled the governed vocabulary would teach a generator to write it."""
    text = path.read_text(encoding="utf-8")
    if path == SCHEMA_PATH:
        assert text.count(f'"{DIALECT}"') == 1
        text = text.replace(f'"{DIALECT}"', '""')
    leaks = sorted({m.group(1) for m in _DECLARED.finditer(text.lower())})
    assert not leaks, f"{path.name} carries the declared vocabulary: {leaks}"


# ---------------------------------------------------------------------------
# held to the real thing, where the real thing is installed
# ---------------------------------------------------------------------------

def test_pyyaml_reads_every_file_as_the_same_object() -> None:
    """Every loader in the family reads these files with PyYAML, and this
    module reads them with `json`: the two must see one object per file."""
    yaml = pytest.importorskip("yaml")
    differ = [p.name for p in [SCHEMA_PATH, *POSITIVE, *NEGATIVE]
              if yaml.safe_load(p.read_text(encoding="utf-8")) != read(p)[1]]
    assert not differ, f"PyYAML and json read these files differently: {differ}"


def test_the_format_checker_admits_whatever_the_pattern_admits() -> None:
    """The pattern is what the required check enforces, so it must never be
    looser than the standard `date-time` checker. Over the pattern table's
    stamps and the calendar sweep, a stamp the pattern admits is one the
    checker admits. A leap second is refused by both."""
    jsonschema = pytest.importorskip("jsonschema")
    pytest.importorskip("rfc3339_validator")     # jsonschema's date-time checker
    checker = jsonschema.Draft202012Validator.FORMAT_CHECKER
    pattern = SCHEMA["$defs"]["generation"]["properties"]["generated_at"]["pattern"]
    stamps = [f"{y:04d}-{m:02d}-{d:02d}T23:59:59+05:30"
              for y in (1900, 2000, 2023, 2024, 2100) for m in range(1, 13) for d in range(1, 32)]
    stamps += ["0000-01-01T00:00:00Z", "0000-02-29T00:00:00Z", "0001-01-01T00:00:00Z"]
    stamps += ["2026-09-27T12:00:00Z", "2026-09-27t12:00:00.25+05:30", "2016-12-31T23:59:60Z",
               "2026-02-31T12:00:00Z", "2026-09-27T12:00:00", "2026-09-27T24:00:00Z"]
    looser = [s for s in stamps if re.search(pattern, s) and not checker.conforms(s, "date-time")]
    assert not looser, f"the pattern admits what the date-time checker refuses: {looser[:10]}"
    leap = "2016-12-31T23:59:60Z"
    assert not re.search(pattern, leap), "the pattern admits a leap second"
    assert not checker.conforms(leap, "date-time"), "the date-time checker admits a leap second"


def test_jsonschema_agrees_rule_for_rule() -> None:
    """`jsonschema` names each failing subschema (`error.schema`), so its
    verdict can be read in rule identifiers exactly as a validator reports
    them. It must find the same rules at the same places as this module's
    evaluator, over every example. The reference rules are not JSON Schema, so
    the reference negatives must pass it."""
    jsonschema = pytest.importorskip("jsonschema")
    validator_class = jsonschema.Draft202012Validator
    validator_class.check_schema(SCHEMA)
    validator = validator_class(SCHEMA, format_checker=validator_class.FORMAT_CHECKER)
    for path in [*POSITIVE, *NEGATIVE]:
        instance = read(path)[1]
        theirs = {(e.schema.get("x-rule"), _pointer(e.absolute_path))
                  for e in validator.iter_errors(instance)}
        ours = {(v.rule, v.where) for v in shape_violations(instance)}
        assert theirs == ours, f"{path.name}: jsonschema {sorted(theirs)} != {sorted(ours)}"
