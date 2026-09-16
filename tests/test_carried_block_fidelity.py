"""The carriage claim, made checkable from inside this repository.

`carry-doxbench-chat-turn-v2-family` asserts that its two requirement blocks are
carried VERBATIM from openxFactory's `retire-doxbench-chat-turn-v1` delta. Until
this file existed that assertion was prose: the proposal named a short commit and
truncated digests, and a reader here had no way to re-derive either without
cloning another repository and guessing where one block stops and the next
begins. Copilot's review of openDox-spec #15 said so, and this is that reading
taken.

WHAT THIS CAN AND CANNOT PROVE. It re-derives the digests from THIS repository's
carried file and compares them to the pinned values — so an edit here, after the
carriage, fails. It cannot reach openxFactory, so it cannot re-verify the SOURCE;
that half was measured once, at carriage, and is recorded in `tasks.md` § 1.1.
The pinned digests are the shared number between the two halves: openxFactory's
own suite pins the same values against its archived packet, so an edit on either
side breaks a test on that side rather than going unnoticed.

THE EXTRACTION BOUNDARY IS THE WHOLE DIFFICULTY and is therefore stated rather
than left to a reader's judgement. A requirement block runs from its
`### Requirement: ` line to the next `### Requirement: ` line OR the next `## `
section heading, WHICHEVER COMES FIRST, with trailing blank lines trimmed to a
single newline. The "whichever comes first" is not decoration: the ADDED block
here is the last requirement of its section, so a rule that looked only for the
next `### Requirement: ` would swallow the `## MODIFIED Requirements` heading and
report 4,176 bytes for a 4,150-byte block. Two honest readers with two unstated
rules get two digests for the same bytes, which is exactly the failure this file
removes.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

CARRIED_DELTA = (
    ROOT / "openspec/changes/carry-doxbench-chat-turn-v2-family"
         / "specs/ideation-dashboard/spec.md")

#: (title, FULL sha256 of the block, byte length) — full, never a prefix:
#: a truncated digest in a provenance claim is a weaker claim than it looks,
#: which is half of what Copilot's review of this change was about. Measured at carriage against
#: openxFactory's delta at `cb2d3a2c` — the same file now archived there at
#: `openspec/changes/archive/2026-09-16-retire-doxbench-chat-turn-v1/specs/`
#: `ideation-dashboard/spec.md` — and re-measured on both sides on 2026-09-16.
CARRIED_BLOCKS = (
    ("An unrecognized chat-turn kind is refused in the SURVIVING family, "
     "never coerced into a removed one",
     "a16607edf70f89855d6f2b1c55ae87d3de1dd844cc9b623aec414716e0cd5127",
     4150),
    ("The chat-turn contract release carries the bound buffer and the model",
     "e7ce5310f2e17f7440abe810b41c364fdcfd926fa594f6baf807f70f30349737",
     5858),
)

#: The requirement openxFactory's delta carries that this change deliberately
#: does NOT: openDox removes nothing, so it makes no claim about a removal.
DOES_NOT_TRAVEL = (
    "The doxBench chat-turn v1 envelope family is REMOVED at contract-v3.0")

_BLOCK_START = re.compile(r"^### Requirement: ", re.M)
_BLOCK_END = re.compile(r"^(?:### Requirement: |## )", re.M)


def _blocks(text: str) -> dict[str, bytes]:
    """Every requirement block, keyed by title, under the stated boundary."""
    out: dict[str, bytes] = {}
    for match in _BLOCK_START.finditer(text):
        start = match.start()
        end_match = _BLOCK_END.search(text, start + 1)
        end = end_match.start() if end_match else len(text)
        chunk = text[start:end].rstrip("\n") + "\n"
        title = chunk.split("\n", 1)[0][len("### Requirement: "):]
        out[title] = chunk.encode("utf-8")
    return out


@pytest.fixture(scope="module")
def carried() -> dict[str, bytes]:
    """Read BYTES and decode them, never `read_text()`.

    `Path.read_text()` opens in universal-newline mode, so a checkout or an edit
    that turned the carried file's line endings into CRLF would be translated
    back to LF before the digest was taken — and a test whose whole claim is
    "byte-for-byte" would pass over bytes it never saw. `decode()` performs no
    such translation, so a CRLF file fails here, which is the point. (Found by
    Copilot's review of openDox-spec #15; the digests are unchanged, because the
    file is LF today — what changed is whether the test could tell.)
    """
    assert CARRIED_DELTA.is_file(), f"no carried delta at {CARRIED_DELTA}"
    return _blocks(CARRIED_DELTA.read_bytes().decode("utf-8"))


@pytest.mark.parametrize("title,digest,size", CARRIED_BLOCKS,
                         ids=["added-unrecognized-kind", "modified-release"])
def test_a_carried_block_still_has_the_bytes_it_arrived_with(
        carried: dict[str, bytes], title: str, digest: str, size: int) -> None:
    assert title in carried, (
        f"the carried delta no longer holds a requirement titled {title!r}; "
        f"it holds {sorted(carried)}")
    body = carried[title]
    actual = hashlib.sha256(body).hexdigest()
    assert (actual, len(body)) == (digest, size), (
        f"{title!r} was carried as sha256 {digest} / {size} bytes and now "
        f"reads sha256 {actual} / {len(body)} bytes. CARRIAGE IS NOT "
        "AUTHORING: this block is openxFactory's ratified text, re-homed under "
        "RULING Q6, and openDox's own amendments belong in a change of its own "
        "rather than in the copy. If the edit is deliberate, it is a new act "
        "and needs one.")


def test_the_block_that_does_not_travel_did_not(
        carried: dict[str, bytes]) -> None:
    """openDox removes nothing, so it carries no removal requirement."""
    assert DOES_NOT_TRAVEL not in carried, (
        f"{DOES_NOT_TRAVEL!r} is in this corpus. It is openxFactory's "
        "statement about openxFactory's own released contract surface, it is "
        "promoted THERE by openxFactory PR #1066, and openDox restating it "
        "would claim an act this repository never performed.")


def test_the_carried_delta_holds_exactly_the_two_blocks(
        carried: dict[str, bytes]) -> None:
    """Not a count — the set is named, so an arrival nobody declared fails."""
    assert set(carried) == {title for title, _d, _s in CARRIED_BLOCKS}, (
        f"the carried delta holds {sorted(carried)}; this change carries "
        "exactly the two blocks named in CARRIED_BLOCKS and a third would be "
        "an undeclared arrival")
