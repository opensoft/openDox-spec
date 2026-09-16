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

CHANGE_ID = "carry-doxbench-chat-turn-v2-family"
DELTA_SUBPATH = "specs/ideation-dashboard/spec.md"


def _carried_delta() -> Path:
    """The carried delta, WHEREVER THE LIFECYCLE HAS PUT IT.

    A hard-coded `openspec/changes/<id>/` path is a test that breaks on a
    correct act: archiving moves the packet to
    `openspec/changes/archive/<date>-<id>/`, and a fixture pinned to the
    in-flight location would then fail for no reason but the move. Pointing it
    at the PROMOTED spec instead is not the repair either — promotion merges the
    delta into the capability's own spec, and the exact-two-block assertion
    below is about the DELTA, so it would start failing against a file that is
    legitimately larger. So the in-flight path is tried first and the archive
    second, and only the absence of BOTH is an error. This keeps the carriage
    claim checkable across the one transition it is guaranteed to outlive.
    (Found by Copilot's review at `e6a143c8`.)
    """
    live = ROOT / "openspec/changes" / CHANGE_ID / DELTA_SUBPATH
    if live.is_file():
        return live
    archived = sorted(
        (ROOT / "openspec/changes/archive").glob(f"*-{CHANGE_ID}/{DELTA_SUBPATH}"))
    if len(archived) == 1:
        return archived[0]
    if len(archived) > 1:
        raise AssertionError(
            f"{CHANGE_ID} is archived more than once: "
            f"{[str(a.relative_to(ROOT)) for a in archived]}")
    raise AssertionError(
        f"no carried delta for {CHANGE_ID}: neither "
        f"{live.relative_to(ROOT)} nor any "
        f"openspec/changes/archive/*-{CHANGE_ID}/{DELTA_SUBPATH}")


#: (title, FULL sha256 of the block, byte length) — full, never a prefix:
#: a truncated digest in a provenance claim is a weaker claim than it looks,
#: which is half of what Copilot's review of this change was about. Measured at
#: carriage against openxFactory's delta at the PINNED COMMIT `cb2d3a2c`, file
#: `openspec/changes/retire-doxbench-chat-turn-v1/specs/ideation-dashboard/`
#: `spec.md`, and re-measured there on 2026-09-16. openxFactory PR #1066
#: PROPOSES to archive that packet unchanged at
#: `openspec/changes/archive/2026-09-16-retire-doxbench-chat-turn-v1/…`; that PR
#: is still OPEN, so the pinned commit — which does not move — is the source
#: this file's numbers rest on, and the archive is named as a destination only.
#: This test reads the LOCAL carried file alone and reaches neither.
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
    """Every requirement block, keyed by title, under the stated boundary.

    A REPEATED TITLE IS REFUSED rather than overwritten. Keying by title is what
    makes the exact-set assertion below readable, but a plain `out[title] = …`
    made the dictionary lossy in exactly the direction that matters: a second
    copy of a carried requirement — identical or not — replaced the first, the
    key set was unchanged, and `test_the_carried_delta_holds_exactly_the_two_blocks`
    passed over a file holding three blocks. A test whose whole claim is "exactly
    these two" must not be satisfiable by a delta that holds an extra one, so the
    duplicate fails HERE, where the file is being read, with both offsets named.
    (Found by Copilot's review at `e6a143c8`.)
    """
    out: dict[str, bytes] = {}
    seen_at: dict[str, int] = {}
    for match in _BLOCK_START.finditer(text):
        start = match.start()
        end_match = _BLOCK_END.search(text, start + 1)
        end = end_match.start() if end_match else len(text)
        chunk = text[start:end].rstrip("\n") + "\n"
        title = chunk.split("\n", 1)[0][len("### Requirement: "):]
        if title in out:
            raise AssertionError(
                f"the delta holds MORE THAN ONE requirement titled {title!r} "
                f"(character offsets {seen_at[title]} and {start}). A repeated "
                "title is a defect in the delta whether or not the two copies "
                "agree: `openspec` addresses a requirement by its title, so a "
                "second copy makes the addressed text ambiguous, and keying "
                "blocks by title would otherwise hide the extra one behind the "
                "first.")
        seen_at[title] = start
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
    return _blocks(_carried_delta().read_bytes().decode("utf-8"))


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
