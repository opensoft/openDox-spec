"""openDox's three health contracts, checked by this leg's own gate.

Plan 038 T040 (R2Q22 (a), ruled on opensoft/openxFactory issue 656, comment
6003486656) gives openDox-spec three schemas for health:

* `contracts/schemas/opendox-health-finding.schema.yaml`: the neutral shape of
  one finding. It is a shape the engine reads, not a file kind (decision N-15):
  a finding carries no `schema_version`, and its `kind` is its family.
* `contracts/schemas/opendox-health-packs.schema.yaml`: `health/packs.yaml`,
  the check-pack manifest, kind `opendox-health-packs`.
* `contracts/schemas/opendox-health-dispositions.schema.yaml`:
  `health/dispositions.yaml`, the exceptions file, kind
  `opendox-health-dispositions`.

Nothing else in this leg reads them, so this module is where their claims
become checkable, as `test_opendox_snapshot_contract.py` is for the snapshot:

* each schema says what plan 038's contracts ask of it: the id rule and its
  bounds (R2Q10 (a), R2Q25 (a), N-13), the manifest's commit and digest rules
  (15.1a, OQ-H15-12, OQ-H15-14), and the exceptions file's keying (OQ-H-13);
* every rule has an identifier and every rule can be broken: each negative
  example breaks exactly the rule its `# expected_failure:` line names, at one
  place, and every rule in an `x-rules` catalog has a negative example;
* the positive examples break no rule, and every finding id they carry is the
  id the id rule computes.

WHY A SMALL EVALUATOR LIVES HERE. The required `validate` check installs pytest
and nothing else, so this module evaluates, with the standard library, exactly
the JSON Schema keywords the three contracts use. A keyword a contract starts
to use and this evaluator does not know fails
`test_the_evaluator_knows_every_keyword` instead of passing unread. Every one of
those keywords is one openDox-code's validator evaluates too, so the two file
kinds can join its kinds by copy alone. Where `jsonschema` and PyYAML are
installed, the two tests at the end hold this evaluator to them; in the
required check they skip.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable, Iterator, NamedTuple

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "contracts/schemas"
EXAMPLES = ROOT / "examples/health"

FINDING = "opendox-health-finding"
PACKS = "opendox-health-packs"
DISPOSITIONS = "opendox-health-dispositions"
CONTRACTS = (FINDING, PACKS, DISPOSITIONS)
#: The two FILE kinds: each is a document with a schema_version and a `kind`
#: constant equal to its contract's id. The finding is not one (N-15).
FILE_KINDS = (PACKS, DISPOSITIONS)

DIALECT = "https://json-schema.org/draft/2020-12/schema"


def _positive(contract: str) -> list[Path]:
    return sorted(EXAMPLES.glob(f"{contract}-*.example.yaml"))


def _negative(contract: str) -> list[Path]:
    return sorted((EXAMPLES / "negative").glob(f"{contract}-*.negative.yaml"))


# ---------------------------------------------------------------------------
# reading a file: a `#` comment header, then one JSON value
# ---------------------------------------------------------------------------

def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """`json` keeps the LAST of two equal keys without a word. A repeated key
    is refused, so no declaration can be dropped in silence."""
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"the key {key!r} appears twice in one object")
        out[key] = value
    return out


def _no_constants(name: str) -> Any:
    """`json` reads NaN, Infinity and -Infinity, which JSON does not define."""
    raise ValueError(f"{name} is not JSON")


def read(path: Path) -> tuple[list[str], Any]:
    """The comment header's lines and the parsed JSON body of `path`."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    header: list[str] = []
    while lines and (lines[0].startswith("#") or not lines[0].strip()):
        header.append(lines.pop(0).rstrip("\n"))
    return header, json.loads("".join(lines), object_pairs_hook=_no_duplicate_keys,
                              parse_constant=_no_constants)


SCHEMA_PATHS = {c: SCHEMA_DIR / f"{c}.schema.yaml" for c in CONTRACTS}
SCHEMAS = {c: read(p)[1] for c, p in SCHEMA_PATHS.items()}


# ---------------------------------------------------------------------------
# the evaluator: exactly the keywords the three contracts use, as JSON Schema
# 2020-12 defines them
# ---------------------------------------------------------------------------

#: The keywords that can FAIL. `additionalProperties` fails only when it is
#: `false`; as a schema it routes, as `properties` does.
CONSTRAINING = frozenset({"type", "const", "enum", "required", "dependentRequired",
                          "minLength", "maxLength", "minProperties", "minimum",
                          "pattern", "not"})
#: The keywords that only carry, annotate or route.
CARRYING = frozenset({"$schema", "$id", "$ref", "$defs", "title", "description",
                      "contract_schema_version", "x-rule", "x-rules",
                      "properties", "additionalProperties", "propertyNames",
                      "items", "allOf", "if", "then"})
#: openDox-code's validator's keywords (`opendox.validator.KEYWORDS` at
#: openDox-code a9ac96f9), which refuses a copy that uses any other. The two
#: file kinds join its kinds by copy (plan 038 T047, T054), so no contract here
#: may step outside them.
OPENDOX_VALIDATOR_KEYWORDS = frozenset({
    "const", "dependentRequired", "enum", "format", "maxItems", "maxLength",
    "maxProperties", "maximum", "minItems", "minLength", "minProperties",
    "minimum", "pattern", "required", "type", "uniqueItems",
    "$ref", "additionalProperties", "allOf", "anyOf", "contains", "if", "items",
    "not", "oneOf", "properties", "propertyNames", "then",
    "$defs", "$id", "$schema", "contract_schema_version", "description",
    "title", "x-rule", "x-rules"})


class Violation(NamedTuple):
    """One broken rule: its id (from `x-rule`, or a reference check's), a JSON
    pointer into the instance ("" is the root), the keyword that failed
    ("reference" for a reference rule), and what was found."""

    rule: str
    where: str
    keyword: str
    detail: str


def _pointer(parts: Any) -> str:
    return "".join("/" + str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def _not_bool(test: Callable[[Any], bool]) -> Callable[[Any], bool]:
    """JSON's true and false are not the numbers 1 and 0."""
    return lambda value: not isinstance(value, bool) and test(value)


#: JSON Schema's seven types, as predicates over a value `json` read. A float
#: with no fraction is an integer, as JSON Schema 2020-12 has it.
_TYPES: dict[str, Callable[[Any], bool]] = {
    "object": lambda value: isinstance(value, dict),
    "array": lambda value: isinstance(value, list),
    "string": lambda value: isinstance(value, str),
    "null": lambda value: value is None,
    "boolean": lambda value: isinstance(value, bool),
    "number": _not_bool(lambda value: isinstance(value, (int, float))),
    "integer": _not_bool(lambda value: isinstance(value, int)
                         or (isinstance(value, float) and value.is_integer())),
}


def _is_type(value: Any, name: str) -> bool:
    return _TYPES[name](value)


def _canon(value: Any) -> Any:
    """JSON equality as JSON Schema defines it: true is not 1, 1 is 1.0, and an
    object's key order is noise."""
    match value:
        case bool():
            return ("boolean", value)
        case int() | float():
            return ("number", value)
        case None:
            return ("null",)
        case str():
            return ("string", value)
        case list():
            return ("array", tuple(map(_canon, value)))
        case _:
            return ("object", tuple(sorted((key, _canon(item)) for key, item in value.items())))


def _resolve(schema: dict[str, Any], ref: str) -> dict[str, Any]:
    assert ref.startswith("#/"), f"only local references are part of a contract: {ref!r}"
    node: Any = schema
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def _extra(value: dict[str, Any], node: dict[str, Any]) -> list[str]:
    """The keys of `value` that `node`'s `properties` do not name."""
    return [key for key in value if key not in node.get("properties", {})]


#: Each keyword that can fail, as a judge of (its argument, the value, the
#: subschema) that names what it found, once per failure. A keyword that
#: applies only to strings, numbers or objects passes every other value.
_JUDGES: dict[str, Callable[[Any, Any, dict[str, Any]], list[str]]] = {
    "type": lambda arg, value, node: [] if any(
        _is_type(value, name) for name in (arg if isinstance(arg, list) else [arg])
    ) else [f"{value!r} is not of type {arg}"],
    "const": lambda arg, value, node: [] if _canon(value) == _canon(arg) else [
        f"{value!r} is not {arg!r}"],
    "enum": lambda arg, value, node: [] if _canon(value) in set(map(_canon, arg)) else [
        f"{value!r} is not one of {arg}"],
    "minLength": lambda arg, value, node: [
        f"{len(value)} characters, fewer than {arg}"] if isinstance(value, str)
        and len(value) < arg else [],
    "maxLength": lambda arg, value, node: [
        f"{len(value)} characters, more than {arg}"] if isinstance(value, str)
        and len(value) > arg else [],
    "pattern": lambda arg, value, node: [
        f"{value!r} does not match the rule's pattern"] if isinstance(value, str)
        and not re.search(arg, value) else [],
    "minimum": lambda arg, value, node: [
        f"{value!r} is less than {arg}"] if _is_type(value, "number") and value < arg else [],
    "required": lambda arg, value, node: [
        f"{key!r} is required" for key in arg if key not in value
    ] if isinstance(value, dict) else [],
    "dependentRequired": lambda arg, value, node: [
        f"{key!r} needs {needs}" for key, needs in arg.items()
        if key in value and any(need not in value for need in needs)
    ] if isinstance(value, dict) else [],
    "minProperties": lambda arg, value, node: [
        f"{len(value)} keys, fewer than {arg}"] if isinstance(value, dict)
        and len(value) < arg else [],
    "additionalProperties": lambda arg, value, node: [
        f"keys this contract does not name: {_extra(value, node)}"] if arg is False
        and isinstance(value, dict) and _extra(value, node) else [],
}


def _check(root: dict[str, Any], value: Any, node: dict[str, Any],
           where: str) -> Iterator[Violation]:
    """Every violation of `node` by `value`, located at `where`."""
    rule = node.get("x-rule", "<no rule named>")
    if "$ref" in node:
        yield from _check(root, value, _resolve(root, node["$ref"]), where)
    for keyword, judge in _JUDGES.items():
        if keyword in node:
            for detail in judge(node[keyword], value, node):
                yield Violation(rule, where, keyword, detail)
    if "not" in node and _passes(root, value, node["not"]):
        yield Violation(rule, where, "not", f"{value!r} is what this rule refuses")
    yield from _applied(root, value, node, where)


def _applied(root: dict[str, Any], value: Any, node: dict[str, Any],
             where: str) -> Iterator[Violation]:
    """The violations of the subschemas `node` applies to `value` or its parts."""
    if isinstance(value, list) and "items" in node:
        for index, item in enumerate(value):
            yield from _check(root, item, node["items"], f"{where}/{index}")
    if isinstance(value, dict):
        for key, sub in node.get("properties", {}).items():
            if key in value:
                yield from _check(root, value[key], sub, where + _pointer([key]))
        if isinstance(node.get("additionalProperties"), dict):
            for key in _extra(value, node):
                yield from _check(root, value[key], node["additionalProperties"],
                                  where + _pointer([key]))
        # A key is judged where its object is, as JSON Schema reports it.
        for key in (value if "propertyNames" in node else ()):
            yield from _check(root, key, node["propertyNames"], where)
    for sub in node.get("allOf", ()):
        yield from _check(root, value, sub, where)
    # `if` is a test, never a failure: it only chooses whether `then` applies.
    if "if" in node and "then" in node and _passes(root, value, node["if"]):
        yield from _check(root, value, node["then"], where)


def _passes(root: dict[str, Any], value: Any, node: dict[str, Any]) -> bool:
    return next(_check(root, value, node, ""), None) is None


def shape_violations(contract: str, instance: Any) -> list[Violation]:
    schema = SCHEMAS[contract]
    return list(_check(schema, instance, schema, ""))


# ---------------------------------------------------------------------------
# the id rule, and the reference rules no JSON Schema keyword can state
# ---------------------------------------------------------------------------

def id_key(identity: Any, kind: str, pack_id: str, path: str) -> bytes:
    """The bytes the id hashes (decision N-13, refined by ADV-07): the JSON of
    {identity, kind, pack_id, path} with sorted keys, no whitespace, and every
    character as itself, in UTF-8."""
    key = {"identity": identity, "kind": kind, "pack_id": pack_id, "path": path}
    return json.dumps(key, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def finding_id(identity: Any, kind: str, pack_id: str, path: str) -> str:
    h16 = hashlib.sha256(id_key(identity, kind, pack_id, path)).hexdigest()[:16]
    return f"{pack_id}.{kind}.{h16}"


def _admits(contract: str, pointer: str, value: Any) -> bool:
    """Whether the subschema at `pointer` admits `value`: a reference rule
    judges only parts whose own shape rules hold, as each shape rule says why
    the others do not."""
    schema = SCHEMAS[contract]
    return _passes(schema, value, _resolve(schema, pointer))


def _finding_parts(finding: Any) -> tuple[str, str, str, str] | None:
    if not isinstance(finding, dict):
        return None
    parts = (finding.get("id"), finding.get("kind"), finding.get("pack_id"), finding.get("path"))
    pointers = ("#/properties/id", "#/properties/kind", "#/properties/pack_id",
                "#/properties/path")
    if all(p is not None and _admits(FINDING, ptr, p) for p, ptr in zip(parts, pointers)):
        return parts  # type: ignore[return-value]
    return None


def _id_names_its_pack_and_kind(finding: Any) -> Iterator[Violation]:
    parts = _finding_parts(finding)
    if parts is None:
        return
    fid, kind, pack_id, _path = parts
    named_pack, named_kind, _h16 = fid.split(".")
    if (named_pack, named_kind) != (pack_id, kind):
        yield Violation("id-names-its-pack-and-kind", "/id", "reference",
                        f"{fid!r} names {named_pack!r} and {named_kind!r}, and the finding "
                        f"is {pack_id!r}'s {kind!r}")


def _id_is_the_hash_of_its_key(finding: Any) -> Iterator[Violation]:
    """Judged only over a key whose every part its own shape rules admit, the
    identity whole, so a malformed identity is reported once, by its own rule,
    and a string UTF-8 cannot encode never reaches the hash."""
    parts = _finding_parts(finding)
    if parts is None or not _admits(FINDING, "#/properties/identity", finding.get("identity")):
        return
    fid, kind, pack_id, path = parts
    want = finding_id(finding["identity"], kind, pack_id, path).rsplit(".", 1)[1]
    have = fid.rsplit(".", 1)[1]
    if have != want:
        yield Violation("id-is-the-hash-of-its-key", "/id", "reference",
                        f"the hash is {have}, and the finding's key hashes to {want}")


def _locator_span_is_ordered(finding: Any) -> Iterator[Violation]:
    locator = finding.get("locator") if isinstance(finding, dict) else None
    if not isinstance(locator, dict):
        return
    start, end = locator.get("line_start"), locator.get("line_end")
    if _is_type(start, "integer") and _is_type(end, "integer") and end < start:
        yield Violation("locator-span-is-ordered", "/locator/line_end", "reference",
                        f"the span ends at {end}, before it starts at {start}")


def _pack_ids_are_unique(manifest: Any) -> Iterator[Violation]:
    packs = manifest.get("packs") if isinstance(manifest, dict) else None
    seen: set[str] = set()
    for i, entry in enumerate(packs if isinstance(packs, list) else []):
        pid = entry.get("id") if isinstance(entry, dict) else None
        if isinstance(pid, str):
            if pid in seen:
                yield Violation("ids-are-unique", f"/packs/{i}/id", "reference",
                                f"{pid!r} is already an entry's id")
            seen.add(pid)


REFERENCE_CHECKS: dict[str, dict[str, Callable[[Any], Iterator[Violation]]]] = {
    FINDING: {
        "id-names-its-pack-and-kind": _id_names_its_pack_and_kind,
        "id-is-the-hash-of-its-key": _id_is_the_hash_of_its_key,
        "locator-span-is-ordered": _locator_span_is_ordered,
    },
    PACKS: {"ids-are-unique": _pack_ids_are_unique},
    DISPOSITIONS: {},
}


def violations(contract: str, instance: Any) -> list[Violation]:
    found = shape_violations(contract, instance)
    for check in REFERENCE_CHECKS[contract].values():
        found.extend(check(instance))
    return found


def _lines(found: list[Violation]) -> str:
    return "; ".join(f"[{v.rule}] {v.where or '<root>'}: {v.detail}" for v in found)


# ---------------------------------------------------------------------------
# walking a schema
# ---------------------------------------------------------------------------

def _subschemas(node: Any, at: str = "", *, tests: bool = False
                ) -> Iterator[tuple[str, dict[str, Any]]]:
    """Every subschema that can produce a failure, with its location. An `if`
    and a `not` are tests whose own failures are never reported, so they and
    what is inside them are skipped, unless `tests` asks for them too (to check
    that every keyword is one evaluated)."""
    if not isinstance(node, dict):
        return
    yield at, node
    for key in ("properties", "$defs"):
        for name, sub in node.get(key, {}).items():
            yield from _subschemas(sub, f"{at}/{key}/{name}", tests=tests)
    single = ("items", "then", "propertyNames", "additionalProperties")
    for key in (*single, "if", "not") if tests else single:
        if isinstance(node.get(key), dict):
            yield from _subschemas(node[key], f"{at}/{key}", tests=tests)
    for i, sub in enumerate(node.get("allOf", ())):
        yield from _subschemas(sub, f"{at}/allOf/{i}", tests=tests)


def _can_fail(node: dict[str, Any]) -> bool:
    return bool(CONSTRAINING & set(node)) or node.get("additionalProperties") is False


def _catalog(contract: str) -> dict[str, dict[str, Any]]:
    return {rule["id"]: rule for rule in SCHEMAS[contract]["x-rules"]}


def _expected_failure(path: Path) -> str:
    header = read(path)[0]
    named = [m.group(1) for line in header
             if (m := re.fullmatch(r"# expected_failure: (\S+)\s*", line))]
    assert len(named) == 1, f"{path.name} must name exactly one expected_failure: {named}"
    return named[0]


# ---------------------------------------------------------------------------
# each contract says what plan 038 asks of it
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_schema_identifies_itself(contract: str) -> None:
    schema = SCHEMAS[contract]
    assert schema["$schema"] == DIALECT
    assert schema["$id"] == SCHEMA_PATHS[contract].name
    assert schema["contract_schema_version"] == 1


@pytest.mark.parametrize("contract", FILE_KINDS)
def test_a_file_kind_names_itself(contract: str) -> None:
    """The manifest and the exceptions file are documents: each carries
    schema_version 1 and a `kind` constant that is its contract's own id, so a
    file of another kind at its path is refused by name."""
    properties = SCHEMAS[contract]["properties"]
    assert properties["schema_version"]["const"] == 1
    assert properties["kind"]["const"] == contract
    assert {"schema_version", "kind"} <= set(SCHEMAS[contract]["required"])


def test_the_finding_is_a_shape_and_not_a_file_kind() -> None:
    """Decision N-15. A finding carries no schema_version, and its `kind` is its
    family, a pattern and never a constant, so no `kind` can name this schema
    and openDox's validator validates no instance against it. The engine reads
    it, through openDox-code's copy."""
    properties = SCHEMAS[FINDING]["properties"]
    assert "schema_version" not in properties
    assert "const" not in properties["kind"] and "enum" not in properties["kind"]
    assert properties["kind"]["pattern"] == properties["pack_id"]["pattern"]


def test_the_finding_carries_14_5s_fields() -> None:
    """14.5: `health list --json` emits one object per finding with id,
    resolution_class, path, severity, evidence, pack_id and pack_version. The
    contract adds kind, identity and message, and lets locator and
    baseline_class be absent."""
    required = set(SCHEMAS[FINDING]["required"])
    assert {"id", "resolution_class", "path", "severity", "evidence", "pack_id",
            "pack_version"} <= required
    assert required == {"id", "kind", "pack_id", "pack_version", "path", "identity",
                        "severity", "resolution_class", "message", "evidence"}
    assert set(SCHEMAS[FINDING]["properties"]) == required | {"locator", "baseline_class"}


def test_the_closed_values_are_the_contracts() -> None:
    properties = SCHEMAS[FINDING]["properties"]
    assert properties["resolution_class"]["enum"] == ["auto-fix", "assisted", "human-only"]
    assert properties["severity"]["enum"] == ["error", "warning", "info"]
    assert properties["baseline_class"]["enum"] == ["new", "pack-upgrade", "persistent"]
    digest = SCHEMAS[PACKS]["$defs"]["digest"]["properties"]
    assert digest["algorithm"]["const"] == "sorted-ls-tree-r-v1"


def test_an_entry_carries_exactly_15_1as_fields() -> None:
    """15.1a: id, version, source and digest, and commit for a git URL only.
    No budget and no bound: those are the engine's (15.6, OQ-H15-5)."""
    entry = SCHEMAS[PACKS]["$defs"]["entry"]
    assert entry["required"] == ["id", "version", "source", "digest"]
    assert set(entry["properties"]) == {"id", "version", "source", "commit", "digest"}
    assert entry["additionalProperties"] is False


@pytest.mark.parametrize("contract", CONTRACTS)
def test_every_named_object_is_closed(contract: str) -> None:
    """Unlike the snapshot, these contracts are CLOSED. A finding's unnamed
    field would be a channel around R2Q25's bounds, a manifest's would let the
    corpus steer the engine, and an exception's could pass for a downgrade.
    identity and evidence name no keys, and bound every key they hold."""
    open_objects = [at or "<root>" for at, node in _subschemas(SCHEMAS[contract])
                    if node.get("type") == "object" and "properties" in node
                    and node.get("additionalProperties") is not False]
    assert not open_objects, f"objects that admit keys they do not name: {open_objects}"


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_evaluator_knows_every_keyword(contract: str) -> None:
    unknown = {(at, key) for at, node in _subschemas(SCHEMAS[contract], tests=True)
               for key in node if key not in CONSTRAINING | CARRYING}
    assert not unknown, f"keywords this module does not evaluate: {sorted(unknown)}"


@pytest.mark.parametrize("contract", CONTRACTS)
def test_every_keyword_is_one_opendoxs_validator_evaluates(contract: str) -> None:
    used = {key for _at, node in _subschemas(SCHEMAS[contract], tests=True) for key in node}
    assert used <= OPENDOX_VALIDATOR_KEYWORDS, sorted(used - OPENDOX_VALIDATOR_KEYWORDS)


# ---------------------------------------------------------------------------
# every rule has an identifier, and each catalog is the rules
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("contract", CONTRACTS)
def test_every_rule_in_the_catalog_is_declared_once(contract: str) -> None:
    ids = [rule["id"] for rule in SCHEMAS[contract]["x-rules"]]
    assert len(ids) == len(set(ids)), "a rule id is catalogued twice"
    for rule in SCHEMAS[contract]["x-rules"]:
        assert set(rule) == {"id", "class", "says"}, rule
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", rule["id"]), rule["id"]
        assert rule["class"] in ("shape", "reference"), rule
        assert rule["says"].strip(), rule


@pytest.mark.parametrize("contract", CONTRACTS)
def test_every_subschema_that_can_fail_names_a_catalogued_shape_rule(contract: str) -> None:
    catalog = _catalog(contract)
    for at, node in _subschemas(SCHEMAS[contract]):
        if _can_fail(node):
            assert "x-rule" in node, f"{at or '<root>'} can fail and names no rule"
        if "x-rule" in node:
            assert node["x-rule"] in catalog, f"{at}: {node['x-rule']!r} is not catalogued"
            assert catalog[node["x-rule"]]["class"] == "shape", (
                f"{at}: {node['x-rule']!r} is a reference rule; no keyword enforces it")


@pytest.mark.parametrize("contract", CONTRACTS)
def test_every_shape_rule_is_enforced_somewhere(contract: str) -> None:
    enforced = {node["x-rule"] for _at, node in _subschemas(SCHEMAS[contract])
                if "x-rule" in node}
    shape = {rid for rid, rule in _catalog(contract).items() if rule["class"] == "shape"}
    assert shape == enforced


@pytest.mark.parametrize("contract", CONTRACTS)
def test_every_reference_rule_is_checked_here(contract: str) -> None:
    reference = {rid for rid, rule in _catalog(contract).items() if rule["class"] == "reference"}
    assert reference == set(REFERENCE_CHECKS[contract])


# ---------------------------------------------------------------------------
# the examples
# ---------------------------------------------------------------------------

POSITIVE_NAMES = {
    FINDING: ["broken-link", "identity-collision", "no-sandbox", "orphan", "pack-upgrade"],
    PACKS: ["empty", "ssh-sources", "two-sources"],
    DISPOSITIONS: ["empty", "two-exceptions"],
}
POSITIVE = [(c, p) for c in CONTRACTS for p in _positive(c)]
NEGATIVE = [(c, p) for c in CONTRACTS for p in _negative(c)]


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_examples_exist(contract: str) -> None:
    assert [p.name for p in _positive(contract)] == [
        f"{contract}-{name}.example.yaml" for name in POSITIVE_NAMES[contract]]
    assert len(_negative(contract)) == len(_catalog(contract))


@pytest.mark.parametrize("contract, path", POSITIVE, ids=lambda v: getattr(v, "name", ""))
def test_a_positive_example_breaks_no_rule(contract: str, path: Path) -> None:
    found = violations(contract, read(path)[1])
    assert not found, _lines(found)


@pytest.mark.parametrize("contract, path", NEGATIVE, ids=lambda v: getattr(v, "name", ""))
def test_a_negative_example_breaks_its_rule_and_no_other(contract: str, path: Path) -> None:
    expected = _expected_failure(path)
    assert path.name == f"{contract}-{expected}.negative.yaml"
    found = violations(contract, read(path)[1])
    assert {v.rule for v in found} == {expected}, f"{path.name} names {expected!r} and breaks {_lines(found)}"
    assert len({v.where for v in found}) == 1, f"{path.name} breaks its rule in two places"


@pytest.mark.parametrize("contract", CONTRACTS)
def test_every_rule_has_a_negative_example(contract: str) -> None:
    assert sorted(_expected_failure(p) for p in _negative(contract)) == sorted(_catalog(contract))


# ---------------------------------------------------------------------------
# the id rule
# ---------------------------------------------------------------------------

def _finding_example(name: str) -> dict[str, Any]:
    return read(EXAMPLES / f"{FINDING}-{name}.example.yaml")[1]


def test_the_id_hashes_exactly_the_key_the_contract_names() -> None:
    """The contract's own example, byte for byte: the four fields, sorted, no
    whitespace. Its printed id was illustrative; this is the id the rule
    computes, and the broken-link example carries it."""
    finding = _finding_example("broken-link")
    key = id_key(finding["identity"], finding["kind"], finding["pack_id"], finding["path"])
    assert key == (b'{"identity":{"target":"../old/brief.md"},"kind":"broken-link",'
                   b'"pack_id":"opendox","path":"notes/plan.md"}')
    assert hashlib.sha256(key).hexdigest()[:16] == "546cd2aacb1a6738"
    assert finding["id"] == "opendox.broken-link.546cd2aacb1a6738"


@pytest.mark.parametrize("name", POSITIVE_NAMES[FINDING])
def test_every_example_id_is_the_id_the_rule_computes(name: str) -> None:
    finding = _finding_example(name)
    assert finding["id"] == finding_id(finding["identity"], finding["kind"],
                                       finding["pack_id"], finding["path"])


def test_the_id_hashes_each_character_as_itself() -> None:
    """The contract says UTF-8. The pack-upgrade example's path holds a
    character outside ASCII, and its id is the hash of that character's own
    bytes; the \\u-escaped reading of the same key would give another id."""
    finding = _finding_example("pack-upgrade")
    assert not finding["path"].isascii()
    key = {"identity": finding["identity"], "kind": finding["kind"],
           "pack_id": finding["pack_id"], "path": finding["path"]}
    escaped = json.dumps(key, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    escaped_h16 = hashlib.sha256(escaped.encode("utf-8")).hexdigest()[:16]
    assert finding["id"].endswith(
        "." + hashlib.sha256(id_key(**key)).hexdigest()[:16])
    assert not finding["id"].endswith("." + escaped_h16)


@pytest.mark.parametrize("change", ["moves the span down", "moves the span up",
                                    "adds a target", "drops the locator"])
def test_an_edit_above_moves_the_locator_and_keeps_the_id(change: str) -> None:
    """Line ranges are display only (N-13, ADV-07): a finding whose locator
    moved is the same finding, under the same id, so an exception keyed by
    that id keeps suppressing it (requirement 15)."""
    finding = _finding_example("broken-link")
    moved = dict(finding)
    if change == "moves the span down":
        moved["locator"] = {"line_start": 40, "line_end": 40}
    elif change == "moves the span up":
        moved["locator"] = {"line_start": 1, "line_end": 1}
    elif change == "adds a target":
        moved["locator"] = {**finding["locator"], "target": "../old/brief.md"}
    else:
        del moved["locator"]
    assert not violations(FINDING, moved), _lines(violations(FINDING, moved))


@pytest.mark.parametrize("field, value", [
    ("identity", {"target": "../old/brief-2.md"}),
    ("kind", "orphan"),
    ("pack_id", "house-style"),
    ("path", "notes/plan-2.md"),
])
def test_each_part_of_the_key_moves_the_id(field: str, value: Any) -> None:
    finding = _finding_example("broken-link")
    changed = {**finding, field: value}
    rules = {v.rule for v in violations(FINDING, changed)}
    assert "id-is-the-hash-of-its-key" in rules or "id-names-its-pack-and-kind" in rules, rules
    recomputed = {**changed, "id": finding_id(changed["identity"], changed["kind"],
                                               changed["pack_id"], changed["path"])}
    assert recomputed["id"] != finding["id"]
    assert not violations(FINDING, recomputed), _lines(violations(FINDING, recomputed))


def _example_ids() -> list[str]:
    ids = [_finding_example(name)["id"] for name in POSITIVE_NAMES[FINDING]]
    for path in _positive(DISPOSITIONS):
        ids += [e["finding"] for e in read(path)[1]["exceptions"]]
    return sorted(set(ids))


def test_every_finding_id_is_a_git_branch_name() -> None:
    """R2Q10 (a): an id is a valid ref-name component, so a finding's fix draft
    is the branch health-fix-<id>. git itself is asked, for every id an example
    carries."""
    git = shutil.which("git")
    if git is None:
        pytest.skip("git is not installed")
    refused = [fid for fid in _example_ids()
               if subprocess.run([git, "check-ref-format", "--branch", f"health-fix-{fid}"],
                                 capture_output=True).returncode != 0]
    assert not refused, f"git refuses these as branch names: {refused}"


def test_every_exception_example_names_a_finding_example() -> None:
    """The exceptions example accepts two of the finding examples, by id."""
    named = {e["finding"] for p in _positive(DISPOSITIONS) for e in read(p)[1]["exceptions"]}
    ids = {_finding_example(name)["id"] for name in POSITIVE_NAMES[FINDING]}
    assert named and named <= ids, named - ids


def test_one_id_pattern_and_one_name_pattern_across_the_three() -> None:
    """A finding id is spelled one way in the finding and in the exceptions
    file, and a pack id one way in the finding and in the manifest."""
    finding = SCHEMAS[FINDING]["properties"]
    exception = SCHEMAS[DISPOSITIONS]["$defs"]["exception"]["properties"]
    assert exception["finding"]["pattern"] == finding["id"]["pattern"]
    name = SCHEMAS[PACKS]["$defs"]["pack_id"]["allOf"][0]["pattern"]
    assert finding["pack_id"]["pattern"] == finding["kind"]["pattern"] == name
    assert finding["id"]["pattern"] == r"^[a-z0-9-]+\.[a-z0-9-]+\.[0-9a-f]{16}$(?!\n)"


# ---------------------------------------------------------------------------
# the bounds on what a finding may carry (R2Q25 (a))
# ---------------------------------------------------------------------------

_SHORT = "x" * 200
_LONG = "x" * 201
#: A lone surrogate, as `os.fsdecode` gives one for a file name byte that is
#: not UTF-8, and as JSON spells one ("\udc80"). UTF-8 cannot encode it.
_LONE = "\udc80"
_EVIDENCE_TEXT = "evidence-strings-are-short-text"
_IDENTITY_TEXT = "identity-strings-are-short-text"


@pytest.mark.parametrize("field, value, where, rule", [
    ("evidence", {}, None, None),
    ("evidence", {"span": [3, 4], "ok": True, "none": None, "digest": "ab" * 32}, None, None),
    ("evidence", {"a": _SHORT}, None, None),
    ("evidence", {_SHORT: "a"}, None, None),
    ("evidence", {"a": "\U0001f50e caf\u00e9"}, None, None),
    ("evidence", {"a": _LONG}, "/evidence/a", _EVIDENCE_TEXT),
    ("evidence", {"a": {"b": [_LONG]}}, "/evidence/a/b/0", _EVIDENCE_TEXT),
    ("evidence", {_LONG: "a"}, "/evidence", _EVIDENCE_TEXT),
    ("evidence", {"a": {_LONG: 1}}, "/evidence/a", _EVIDENCE_TEXT),
    ("evidence", {"a": f"notes/{_LONE}.md"}, "/evidence/a", _EVIDENCE_TEXT),
    ("evidence", {"a": [{_LONE: 1}]}, "/evidence/a/0", _EVIDENCE_TEXT),
    ("evidence", {"quote": "a"}, "/evidence", "evidence-names-no-text"),
    ("evidence", {"a": [{"content": "a"}]}, "/evidence/a/0", "evidence-names-no-text"),
    ("evidence", {"Text": "a", "excerpts": "a", "context": "a"}, None, None),
    ("evidence", ["a"], "/evidence", "evidence-is-an-object"),
    ("identity", {}, None, None),
    ("identity", {"pair": ["a.md", "b.md"], "anchor": None, "flag": False}, None, None),
    ("identity", {"target": "\U0001f50e caf\u00e9.md"}, None, None),
    ("identity", {"line": 12}, "/identity/line", "identity-holds-no-number"),
    ("identity", {"at": {"n": 1.5}}, "/identity/at/n", "identity-holds-no-number"),
    ("identity", {"pair": ["a.md", 2]}, "/identity/pair/1", "identity-holds-no-number"),
    ("identity", {"a": _LONG}, "/identity/a", _IDENTITY_TEXT),
    ("identity", {_LONG: "a"}, "/identity", _IDENTITY_TEXT),
    ("identity", {"target": f"../{_LONE}.md"}, "/identity/target", _IDENTITY_TEXT),
    ("identity", {_LONE: "a"}, "/identity", _IDENTITY_TEXT),
    ("identity", {"excerpt": "a"}, "/identity", "identity-names-no-text"),
    ("identity", "../old/brief.md", "/identity", "identity-is-an-object"),
], ids=lambda v: v if isinstance(v, str) and v.isascii() and len(v) < 40 else "")
def test_identity_and_evidence_are_bounded_at_every_depth(
        field: str, value: Any, where: str | None, rule: str | None) -> None:
    """Every string, key or value, at any depth, is at most 200 characters with
    no lone surrogate, and no key at any depth is named excerpt, text, content
    or quote, exactly as the contract spells them. identity holds no number.
    A changed identity that is admitted gets its id computed again, so only the
    bound under test can break; a refused one is never hashed."""
    finding = {**_finding_example("broken-link"), field: value}
    if field == "identity" and rule is None:
        finding["id"] = finding_id(value, finding["kind"], finding["pack_id"], finding["path"])
    found = violations(FINDING, finding)
    if rule is None:
        assert not found, _lines(found)
    else:
        assert {(v.rule, v.where) for v in found} == {(rule, where)}, _lines(found)


@pytest.mark.parametrize("field, value, rule", [
    ("pack_version", f"0.2.0{_LONE}", "pack-version-is-text"),
    ("path", f"notes/{_LONE}.md", "path-is-corpus-relative"),
    ("message", f"no file named {_LONE}", "message-is-one-bounded-line"),
    ("locator", {"target": f"../{_LONE}.md"}, "locator-target-is-short-text"),
    ("identity", {"target": _LONE}, _IDENTITY_TEXT),
    ("identity", {_LONE: "x"}, _IDENTITY_TEXT),
    ("evidence", {"candidate": _LONE}, _EVIDENCE_TEXT),
    ("evidence", {_LONE: "x"}, _EVIDENCE_TEXT),
], ids=["pack_version", "path", "message", "locator target", "identity value",
        "identity key", "evidence value", "evidence key"])
def test_no_string_a_finding_carries_holds_a_lone_surrogate(field: str, value: Any,
                                                             rule: str) -> None:
    """UTF-8 cannot encode a lone surrogate, so the id could not hash a key
    holding one, and no store or JSON reader could take the finding. Each is
    refused by its own rule, and the id rule is never asked to hash it: the
    finding keeps its old id, and only the one rule breaks."""
    finding = {**_finding_example("broken-link"), field: value}
    found = violations(FINDING, finding)
    assert {v.rule for v in found} == {rule}, _lines(found)
    with pytest.raises(UnicodeEncodeError):
        _LONE.encode("utf-8")


def test_every_bound_is_the_contracts_200_characters() -> None:
    """The contract bounds message and every string of evidence at 200
    characters, and this schema bounds identity and locator.target alike."""
    bounds = {node["maxLength"] for _at, node in _subschemas(SCHEMAS[FINDING], tests=True)
              if "maxLength" in node}
    assert bounds == {200}


@pytest.mark.parametrize("message, admitted", [
    ("x" * 200, True),
    ("x" * 201, False),
    ("", False),
    ("é" * 200, True),
    ("\U0001f50e" * 200, True),
    ("\U0001f50e" * 201, False),
], ids=["200", "201", "empty", "200 accented", "200 astral", "201 astral"])
def test_a_message_is_one_line_of_at_most_200_characters(message: str, admitted: bool) -> None:
    """Characters are code points, as JSON Schema counts them: a character
    outside the Basic Multilingual Plane is one, not two."""
    finding = {**_finding_example("broken-link"), "message": message}
    found = violations(FINDING, finding)
    assert (not found) is admitted, _lines(found)
    assert {v.rule for v in found} <= {"message-is-one-bounded-line"}


@pytest.mark.parametrize("locator, rules", [
    ({"line_start": 1, "line_end": 1}, set()),
    ({"target": "../a.md"}, set()),
    ({"line_start": 3, "line_end": 5, "target": "../a.md"}, set()),
    ({"line_start": 3.0, "line_end": 5}, set()),
    ({}, {"locator-keys"}),
    ({"line_end": 5}, {"locator-keys"}),
    ({"line": 5}, {"locator-keys"}),
    ({"target": "../a.md", "text": "a"}, {"locator-keys"}),
    ({"line_start": True, "line_end": 5}, {"locator-line-is-a-line-number"}),
    ({"line_start": "3", "line_end": 5}, {"locator-line-is-a-line-number"}),
    ({"line_start": 2.5, "line_end": 5}, {"locator-line-is-a-line-number"}),
    ({"target": ""}, {"locator-target-is-short-text"}),
    ({"target": _SHORT}, set()),
    ({"target": _LONG}, {"locator-target-is-short-text"}),
    ({"line_start": 5, "line_end": 4}, {"locator-span-is-ordered"}),
], ids=repr)
def test_a_locator_is_a_span_a_target_or_both(locator: dict[str, Any], rules: set[str]) -> None:
    finding = {**_finding_example("broken-link"), "locator": locator}
    assert {v.rule for v in violations(FINDING, finding)} == rules


@pytest.mark.parametrize("path, resolution_class, rules", [
    ("", "human-only", set()),
    ("", "assisted", {"pathless-finding-is-human-only"}),
    ("", "auto-fix", {"pathless-finding-is-human-only"}),
    ("notes/plan.md", "auto-fix", set()),
], ids=repr)
def test_a_finding_that_names_no_document_is_human_only(
        path: str, resolution_class: str, rules: set[str]) -> None:
    finding = {**_finding_example("no-sandbox"), "path": path,
               "resolution_class": resolution_class}
    finding["id"] = finding_id(finding["identity"], finding["kind"], finding["pack_id"], path)
    assert {v.rule for v in violations(FINDING, finding)} == rules


# ---------------------------------------------------------------------------
# the pattern rules, value by value
# ---------------------------------------------------------------------------

def _pattern_at(contract: str, pointer: str) -> str:
    return _resolve(SCHEMAS[contract], pointer)["pattern"]


#: (rule, contract, the subschema's pointer). Each is read here, and again
#: through a browser's regex engine below.
PATTERNS: dict[str, tuple[str, str]] = {
    "id-is-well-formed": (FINDING, "#/properties/id"),
    "kind-is-a-family-name": (FINDING, "#/properties/kind"),
    "pack-version-is-text": (FINDING, "#/properties/pack_version"),
    "path-is-corpus-relative": (FINDING, "#/properties/path"),
    "message-is-one-bounded-line": (FINDING, "#/properties/message"),
    "pack-id-is-a-name": (PACKS, "#/$defs/pack_id/allOf/0"),
    "source-is-a-git-url-or-corpus-path": (PACKS, "#/$defs/entry/properties/source/allOf/0"),
    "source-carries-no-credential": (PACKS, "#/$defs/entry/properties/source/allOf/1"),
    "git-source-test": (PACKS, "#/$defs/entry/allOf/0/if/properties/source"),
    "corpus-source-test": (PACKS, "#/$defs/entry/allOf/1/if/properties/source"),
    "commit-is-40-hex": (PACKS, "#/$defs/entry/properties/commit"),
    "digest-value-is-64-hex": (PACKS, "#/$defs/digest/properties/value"),
    "finding-is-a-finding-id": (DISPOSITIONS, "#/$defs/exception/properties/finding"),
    "reason-is-text": (DISPOSITIONS, "#/$defs/exception/properties/reason"),
    "version-is-text": (PACKS, "#/$defs/entry/properties/version"),
    "locator-target-is-short-text": (FINDING, "#/properties/locator/properties/target"),
    "identity-strings-are-short-text": (FINDING, "#/$defs/identity_value/allOf/1"),
    "evidence-strings-are-short-text": (FINDING, "#/$defs/evidence_value"),
}

_H16 = "0123456789abcdef"
PATTERN_CASES: list[tuple[str, str, bool]] = [
    ("id-is-well-formed", f"opendox.broken-link.{_H16}", True),
    ("id-is-well-formed", f"house-style.heading-case.{_H16}", True),
    ("id-is-well-formed", f"opendox.broken-link.{_H16.upper()}", False),
    ("id-is-well-formed", f"opendox.broken-link.{_H16[:15]}", False),
    ("id-is-well-formed", f"opendox.broken-link.{_H16}0", False),
    ("id-is-well-formed", f"opendox.broken_link.{_H16}", False),
    ("id-is-well-formed", f"opendox.broken.link.{_H16}", False),
    ("id-is-well-formed", f"broken-link.{_H16}", False),
    ("id-is-well-formed", f"opendox.broken-link.{_H16}\n", False),
    ("id-is-well-formed", "broken-link", False),
    ("kind-is-a-family-name", "broken-link", True),
    ("kind-is-a-family-name", "stage-location-mismatch", True),
    ("kind-is-a-family-name", "Broken-link", False),
    ("kind-is-a-family-name", "broken.link", False),
    ("kind-is-a-family-name", "broken-link\n", False),
    ("kind-is-a-family-name", "", False),
    ("pack-version-is-text", "0.2.0", True),
    ("pack-version-is-text", "1.0.0-rc.2", True),
    ("pack-version-is-text", "0.2.0\n", False),
    ("pack-version-is-text", "0.2\u00850", False),
    ("path-is-corpus-relative", "notes/plan.md", True),
    ("path-is-corpus-relative", "", True),
    ("path-is-corpus-relative", "notes/caf\u00e9.md", True),
    ("path-is-corpus-relative", "a..b/c.md", True),
    ("path-is-corpus-relative", "/notes/plan.md", False),
    ("path-is-corpus-relative", "../plan.md", False),
    ("path-is-corpus-relative", "notes/../plan.md", False),
    ("path-is-corpus-relative", "notes/..", False),
    ("path-is-corpus-relative", "notes\\plan.md", False),
    ("path-is-corpus-relative", "C:/plan.md", False),
    ("path-is-corpus-relative", "notes/plan.md\n", False),
    ("path-is-corpus-relative", "notes/a\u007fb.md", False),
    ("message-is-one-bounded-line", "link target does not exist", True),
    ("message-is-one-bounded-line", "one line\nand another", False),
    ("message-is-one-bounded-line", "one line\r", False),
    ("message-is-one-bounded-line", "a\tb", False),
    ("message-is-one-bounded-line", "one line\u2028and another", False),
    ("message-is-one-bounded-line", "one paragraph\u2029and another", False),
    ("message-is-one-bounded-line", "a\u0085b", False),
    ("message-is-one-bounded-line", "caf\u00e9 \u2014 fine", True),
    ("pack-id-is-a-name", "house-style", True),
    ("pack-id-is-a-name", "opendox", True),
    ("pack-id-is-a-name", "house_style", False),
    ("pack-id-is-a-name", "house.style", False),
    ("pack-id-is-a-name", "House-style", False),
    ("pack-id-is-a-name", "house-style\n", False),
    ("source-is-a-git-url-or-corpus-path", "tools/packs/house-style", True),
    ("source-is-a-git-url-or-corpus-path", "packs", True),
    ("source-is-a-git-url-or-corpus-path", "tools/my packs/house-style", True),
    ("source-is-a-git-url-or-corpus-path", "https://example.invalid/packs/a.git", True),
    ("source-is-a-git-url-or-corpus-path", "ssh://git@example.invalid:443/packs/a.git", True),
    ("source-is-a-git-url-or-corpus-path", "git@example.invalid:packs/a.git", True),
    ("source-is-a-git-url-or-corpus-path", "file:///srv/packs/a", False),
    ("source-is-a-git-url-or-corpus-path", "ext::sh -c touch% /tmp/pwned", False),
    ("source-is-a-git-url-or-corpus-path", "http://example.invalid/packs/a.git", False),
    ("source-is-a-git-url-or-corpus-path", "git://example.invalid/packs/a.git", False),
    ("source-is-a-git-url-or-corpus-path", "example.invalid:packs/a.git", False),
    ("source-is-a-git-url-or-corpus-path", "https://example.invalid", False),
    ("source-is-a-git-url-or-corpus-path", "https://example.invalid/a b.git", False),
    ("source-is-a-git-url-or-corpus-path", "/srv/packs/a", False),
    ("source-is-a-git-url-or-corpus-path", "../shared/packs/a", False),
    ("source-is-a-git-url-or-corpus-path", "tools/../../packs/a", False),
    ("source-is-a-git-url-or-corpus-path", "C:/packs/a", False),
    ("source-is-a-git-url-or-corpus-path", "tools\\packs\\a", False),
    ("source-is-a-git-url-or-corpus-path", "tools/packs/a\n", False),
    ("source-is-a-git-url-or-corpus-path", "", False),
    ("source-carries-no-credential", "https://example.invalid/packs/a.git", True),
    ("source-carries-no-credential", "https://example.invalid/packs/a@v1.git", True),
    ("source-carries-no-credential", "ssh://git@example.invalid:443/packs/a.git", True),
    ("source-carries-no-credential", "ssh://example.invalid:443/packs/a.git", True),
    ("source-carries-no-credential", "git@example.invalid:packs/a.git", True),
    ("source-carries-no-credential", "tools/packs/a", True),
    ("source-carries-no-credential", "https://token@example.invalid/packs/a.git", False),
    ("source-carries-no-credential", "https://user:pass@example.invalid/packs/a.git", False),
    ("source-carries-no-credential", "https://example.invalid/packs/a.git?token=x", False),
    ("source-carries-no-credential", "ssh://user:pass@example.invalid/packs/a.git", False),
    ("git-source-test", "https://example.invalid/packs/a.git", True),
    ("git-source-test", "ssh://example.invalid/packs/a.git", True),
    ("git-source-test", "git@example.invalid:packs/a.git", True),
    ("git-source-test", "tools/packs/a", False),
    ("git-source-test", "file:///srv/packs/a", False),
    ("git-source-test", "git\u001c@example.invalid:packs/a.git", False),
    ("corpus-source-test", "tools/packs/a", True),
    ("corpus-source-test", "https://example.invalid/packs/a.git", False),
    ("corpus-source-test", "git@example.invalid:packs/a.git", False),
    ("corpus-source-test", "../packs/a", False),
    ("corpus-source-test", "", False),
    ("commit-is-40-hex", "96abd3ea4dc5bf1c2faf8ab0f89baeb0bd80d098", True),
    ("commit-is-40-hex", "96abd3e", False),
    ("commit-is-40-hex", "96ABD3EA4DC5BF1C2FAF8AB0F89BAEB0BD80D098", False),
    ("commit-is-40-hex", "96abd3ea4dc5bf1c2faf8ab0f89baeb0bd80d098\n", False),
    ("digest-value-is-64-hex", "ab" * 32, True),
    ("digest-value-is-64-hex", "ab" * 31, False),
    ("digest-value-is-64-hex", "AB" * 32, False),
    ("digest-value-is-64-hex", "ab" * 32 + "\n", False),
    ("finding-is-a-finding-id", f"opendox.orphan.{_H16}", True),
    ("finding-is-a-finding-id", "orphan", False),
    ("finding-is-a-finding-id", f"opendox.orphan.{_H16}\n", False),
    ("reason-is-text", "kept as an unlinked appendix on purpose", True),
    ("reason-is-text", "two lines\nof reason", True),
    ("reason-is-text", "", False),
    ("reason-is-text", "   ", False),
    ("reason-is-text", "\t\n", False),
    ("reason-is-text", "\ufeff", False),
    ("reason-is-text", "\u001c\u0085", False),
    ("reason-is-text", "\u00a0\u3000", False),
    # a lone surrogate, which UTF-8 cannot encode, in every string a finding
    # carries; an astral character, which is one code point, is text
    ("pack-version-is-text", "0.2.0\udc80", False),
    ("version-is-text", "1.4.0", True),
    ("version-is-text", "1.4.0\udc80", False),
    ("version-is-text", "1.4\n", False),
    ("path-is-corpus-relative", "notes/\udc80.md", False),
    ("path-is-corpus-relative", "notes/\U0001f50e.md", True),
    ("message-is-one-bounded-line", "no file named \udc80", False),
    ("message-is-one-bounded-line", "a \U0001f50e b", True),
    ("source-is-a-git-url-or-corpus-path", "tools/\udc80/a", False),
    ("git-source-test", "git@example.invalid:packs/\udc80.git", False),
    ("corpus-source-test", "tools/\udc80/a", False),
    ("locator-target-is-short-text", "../old/brief.md", True),
    ("locator-target-is-short-text", "../\ud800.md", False),
    ("locator-target-is-short-text", "../\U0001f50e.md", True),
    ("identity-strings-are-short-text", "../old/brief.md", True),
    ("identity-strings-are-short-text", "\ud800", False),
    ("identity-strings-are-short-text", "a\udfff", False),
    ("identity-strings-are-short-text", "\U0001f50e", True),
    ("evidence-strings-are-short-text", "\udbff", False),
    ("evidence-strings-are-short-text", "\U0010ffff", True),
]


@pytest.mark.parametrize("rule, value, admitted", PATTERN_CASES)
def test_a_pattern_admits_and_refuses(rule: str, value: str, admitted: bool) -> None:
    """Each pattern guards its own tail, with `$(?!\\n)` or by refusing every
    control character, because a Python `$` also matches before a final
    newline and an ECMA-262 `$` does not."""
    contract, pointer = PATTERNS[rule]
    assert bool(re.search(_pattern_at(contract, pointer), value)) is admitted


#: Every character where Python's and a browser's regex engines could part,
#: as in the snapshot's test: every control, every character either engine
#: counts as whitespace, the invisible neighbours of those, and two letters;
#: and, for the lone-surrogate rules, both ends of each surrogate half and two
#: astral characters, which each engine reads as one code point.
_EDGE_CHARACTERS = [*range(0x00, 0xA1), 0x1680, 0x180E, *range(0x2000, 0x2010),
                    *range(0x2028, 0x2030), 0x205F, 0x2060, 0x3000,
                    0xD800, 0xDBFF, 0xDC00, 0xDC80, 0xDFFF, 0xFEFF, 0xFFFE, 0x1F50E, 0x10FFFF]


def test_a_browser_reads_every_pattern_as_python_does() -> None:
    """A JSON Schema pattern is an ECMA-262 regular expression, and a pack
    author's tool or a view may well run one in JavaScript. Node's RegExp with
    the `u` flag reads the pattern table, and a sweep of the edge characters
    through every pattern, and must give Python's verdict every time."""
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed; validate.yml installs it")
    cases = [(_pattern_at(*PATTERNS[rule]), value) for rule, value, _admitted in PATTERN_CASES]
    for code in _EDGE_CHARACTERS:
        ch = chr(code)
        for contract, pointer in PATTERNS.values():
            pattern = _pattern_at(contract, pointer)
            cases += [(pattern, v) for v in (ch, f"a{ch}", f"{ch}a", f"a{ch}b",
                                             f"https://h{ch}/a", f"u{ch}@h:p", f"p/a{ch}b")]
    script = ("const c = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
              "process.stdout.write(JSON.stringify(c.map(([p, v]) => new RegExp(p, 'u').test(v))));")
    run = subprocess.run([node, "-e", script], input=json.dumps(cases), capture_output=True,
                         text=True, check=True)
    theirs = json.loads(run.stdout)
    parted = [(p[:24], v, ours) for (p, v), ours, js in
              zip(cases, (bool(re.search(p, v)) for p, v in cases), theirs) if ours is not js]
    assert not parted, f"Python and a browser read these differently: {parted[:10]}"


# ---------------------------------------------------------------------------
# where a pack lives decides its commit (15.1a)
# ---------------------------------------------------------------------------

_SOURCES = sorted({value for rule, value, _ok in PATTERN_CASES
                   if rule in ("source-is-a-git-url-or-corpus-path", "source-carries-no-credential",
                               "git-source-test", "corpus-source-test")})


@pytest.mark.parametrize("source", _SOURCES, ids=repr)
def test_an_admitted_source_is_exactly_one_of_git_and_corpus(source: str) -> None:
    """The two commit rules test the same two forms the source rule admits, so
    an admitted source is a git URL or a corpus path and never both, and one
    of the two commit rules always applies to it."""
    git = bool(re.search(_pattern_at(*PATTERNS["git-source-test"]), source))
    corpus = bool(re.search(_pattern_at(*PATTERNS["corpus-source-test"]), source))
    assert not (git and corpus), source
    if re.search(_pattern_at(*PATTERNS["source-is-a-git-url-or-corpus-path"]), source):
        assert git or corpus, source


_COMMIT = "96abd3ea4dc5bf1c2faf8ab0f89baeb0bd80d098"


@pytest.mark.parametrize("source, commit, rules", [
    ("tools/packs/a", None, set()),
    ("tools/packs/a", _COMMIT, {"corpus-source-carries-no-commit"}),
    ("https://example.invalid/packs/a.git", _COMMIT, set()),
    ("https://example.invalid/packs/a.git", None, {"git-source-carries-a-commit"}),
    ("ssh://git@example.invalid/packs/a.git", None, {"git-source-carries-a-commit"}),
    ("git@example.invalid:packs/a.git", None, {"git-source-carries-a-commit"}),
    ("git@example.invalid:packs/a.git", _COMMIT, set()),
    ("file:///srv/packs/a", None, {"source-is-a-git-url-or-corpus-path"}),
    ("file:///srv/packs/a", _COMMIT, {"source-is-a-git-url-or-corpus-path"}),
    ("/srv/packs/a", None, {"source-is-a-git-url-or-corpus-path"}),
], ids=repr)
def test_where_a_pack_lives_decides_its_commit(source: str, commit: str | None,
                                               rules: set[str]) -> None:
    manifest = read(EXAMPLES / f"{PACKS}-two-sources.example.yaml")[1]
    entry = {k: v for k, v in manifest["packs"][0].items() if k != "commit"}
    entry["source"] = source
    if commit is not None:
        entry["commit"] = commit
    manifest["packs"] = [entry]
    assert {v.rule for v in violations(PACKS, manifest)} == rules


def test_the_digest_is_taken_over_the_tree_the_source_names() -> None:
    """OQ-H15-12, as plan 038's manifest contract states it: a corpus-relative
    source's digest is over the subtree <corpus-commit>:<source>, and a git
    URL's over the fetched repository's root tree at its commit, never over a
    tree-ish holding the URL. The header is where a reader learns which."""
    header = "\n".join(read(SCHEMA_PATHS[PACKS])[0])
    assert "<corpus-commit>:<source>" in header
    assert "<commit>^{tree}" in header
    assert "The URL is never part of a tree-ish." in header
    assert "<commit>:<source>" not in header


@pytest.mark.parametrize("key", ["timeout", "budget", "memory", "pids", "nproc", "cpu"])
def test_no_entry_sets_a_budget_or_a_bound(key: str) -> None:
    """15.6 and OQ-H15-5: the budget and the bounds are the engine's, never read
    from the corpus. Any such key, at the entry or at the top, is refused."""
    manifest = read(EXAMPLES / f"{PACKS}-two-sources.example.yaml")[1]
    in_entry = {**manifest, "packs": [{**manifest["packs"][0], key: 60}]}
    at_top = {**manifest, key: 60}
    assert {v.rule for v in violations(PACKS, in_entry)} == {"entry-keys"}
    assert {v.rule for v in violations(PACKS, at_top)} == {"envelope-keys"}


# ---------------------------------------------------------------------------
# the reader
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("body", ['{"a": NaN}', '{"a": Infinity}', '{"a": -Infinity}',
                                  '{"a": 1, "a": 2}'],
                         ids=["NaN", "Infinity", "-Infinity", "a repeated key"])
def test_the_reader_refuses_what_json_does_not_mean(tmp_path: Path, body: str) -> None:
    path = tmp_path / "body.yaml"
    path.write_text(f"# a header line\n{body}\n", encoding="utf-8")
    with pytest.raises(ValueError):
        read(path)


# ---------------------------------------------------------------------------
# held to the real thing, where the real thing is installed
# ---------------------------------------------------------------------------

_ALL_FILES = [*SCHEMA_PATHS.values(), *(p for _c, p in POSITIVE), *(p for _c, p in NEGATIVE)]


def test_pyyaml_reads_every_file_as_the_same_object() -> None:
    """Every loader in the family reads these files with PyYAML, and this
    module reads them with `json`: the two must see one object per file."""
    yaml = pytest.importorskip("yaml")
    differ = [p.name for p in _ALL_FILES
              if yaml.safe_load(p.read_text(encoding="utf-8")) != read(p)[1]]
    assert not differ, f"PyYAML and json read these files differently: {differ}"


def test_jsonschema_agrees_rule_for_rule() -> None:
    """`jsonschema` names each failing subschema (`error.schema`), so its
    verdict reads in rule identifiers. It must find the same rules at the same
    places as this module's evaluator, over every example. The reference rules
    are not JSON Schema, so their negatives must pass it."""
    jsonschema = pytest.importorskip("jsonschema")
    validator_class = jsonschema.Draft202012Validator
    for contract in CONTRACTS:
        validator_class.check_schema(SCHEMAS[contract])
        validator = validator_class(SCHEMAS[contract])
        for path in [*_positive(contract), *_negative(contract)]:
            instance = read(path)[1]
            theirs = {(e.schema.get("x-rule"), _pointer(e.absolute_path))
                      for e in validator.iter_errors(instance)}
            ours = {(v.rule, v.where) for v in shape_violations(contract, instance)}
            assert theirs == ours, f"{path.name}: jsonschema {sorted(theirs)} != {sorted(ours)}"
