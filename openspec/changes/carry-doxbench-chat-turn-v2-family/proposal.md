---
Status: draft
Re-homed-from: openxFactory `openspec/changes/retire-doxbench-chat-turn-v1` — the FORWARD HALF only, under RULING Q6 (`split-opendox-two-layer-product` `tasks.md` § 6.2). The openxFactory packet is NOT closed as re-homed: it archives in openxFactory on its own evidence, and only the surviving family's requirements come here.
Ratified-in-openxFactory: Brett Heap, 2026-09-01, in session ("ratify #551 and #552"), at PR #552 tip `c5169476` — record `openspec/changes/retire-doxbench-chat-turn-v1/review/ratification-2026-09-01.md` in `opensoft/openxFactory`
code_surface: openDox-code (the doxBench chat-turn route's refusal path for an unrecognized kind, and the surviving `-v2` envelope family the workbench turn is carried by — as they arrive with the carve). **NOT the removal**: the v1 family's deletion is already openxFactory bytes at `contract-v3.0` and stays that repository's history.
---

# Proposal: carry-doxbench-chat-turn-v2-family

**THE ONE OF THE FIVE THAT IS NOT SIMPLY RE-HOMED.** `split-opendox-two-layer-product`
§ 6.2 and `design.md` § D9 both say so: `retire-doxbench-chat-turn-v1`
*"archives in `openxFactory` on its own evidence, and only its FORWARD half —
the surviving `-v2` family's requirements — re-homes to openDox."* This change is
that forward half, and it is deliberately NOT called `retire-doxbench-chat-turn-v1`:
openDox retires nothing here.

## Why

The openxFactory packet did three things and only two of them travel.

**What STAYS in openxFactory, as history rather than as a decision to re-take:**
the `## ADDED` requirement *The doxBench chat-turn v1 envelope family is REMOVED
at contract-v3.0*. That removal is REALIZED in openxFactory bytes — the `$defs`,
the top-level `oneOf` entries, the `deprecated_envelopes` block, the kind
constants, the packaged instances and the byte-identity baseline are gone there —
and `contract-v3.0` is a PUBLISHED openxFactory bundle tag
(`ff9ed815`, annotated tag object `59f4f51f`). A requirement about a removal
performed in another repository's released bundle cannot be re-promoted here
without claiming an act openDox never performed.

**What TRAVELS, because it is what the surviving family IS:**

- the `## ADDED` requirement *An unrecognized chat-turn kind is refused in the
  SURVIVING family, never coerced into a removed one* — the redesign the removal
  created, and a live obligation on the route openDox will own;
- the `## MODIFIED` requirement *The chat-turn contract release carries the bound
  buffer and the model* — one of the FOUR promoted titles the split packet's
  § THE SIBLING COLLISION table (a) names, destination openDox.

Both blocks are carried **verbatim**, and the claim is made auditable rather than
asserted. THE SOURCE, in full: `opensoft/openxFactory` at
`cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, file
`openspec/changes/retire-doxbench-chat-turn-v1/specs/ideation-dashboard/spec.md`
That pinned commit is the COMPLETED provenance and the only source this claim
rests on. openxFactory PR **#1066** PROPOSES to archive the same packet unchanged
at
`openspec/changes/archive/2026-09-16-retire-doxbench-chat-turn-v1/specs/ideation-dashboard/spec.md`,
and **that pull request is still OPEN** — measured 2026-09-16: `state=OPEN`, no
merge commit, the archive path returns 404 on openxFactory `main`, and the ACTIVE
packet still stands there at `openspec/changes/retire-doxbench-chat-turn-v1`.
An earlier draft of this paragraph named the archived path as a present fact; it
is a destination, and it is named here as one. Nothing in this change waits on it
— the digests are taken against `cb2d3a2c`, which does not move.

| block | bytes | `sha256` |
| --- | ---: | --- |
| ADDED *An unrecognized chat-turn kind is refused in the SURVIVING family…* | 4,150 | `a16607edf70f89855d6f2b1c55ae87d3de1dd844cc9b623aec414716e0cd5127` |
| MODIFIED *The chat-turn contract release carries the bound buffer and the model* | 5,858 | `e7ce5310f2e17f7440abe810b41c364fdcfd926fa594f6baf807f70f30349737` |

**THE EXTRACTION BOUNDARY IS STATED, because without it the digests are not
reproducible and two honest readers get two answers.** A block runs from its
`### Requirement: ` line to the next `### Requirement: ` line OR the next `## `
section heading, WHICHEVER COMES FIRST, with trailing blank lines trimmed to a
single newline. The "whichever comes first" is load-bearing: the ADDED block is
the last requirement of its section, so a rule that looked only for the next
`### Requirement: ` swallows the `## MODIFIED Requirements` heading and reports
4,176 bytes for a 4,150-byte block. That is not hypothetical — it is what a
re-derivation of this claim did before the rule was written down.

**AND IT IS CHECKED, not just described.** `tests/test_carried_block_fidelity.py`
re-derives both digests from the carried file on every run, asserts the third
requirement did NOT travel, and asserts the block set is exactly these two so an
undeclared arrival fails. It cannot reach openxFactory, so it cannot re-verify
the source half; that was measured at carriage and again on 2026-09-16, on both
sides, against the PINNED COMMIT.
**WITHDRAWN 2026-09-16, because it was not true:** this paragraph used to add
that "openxFactory's own suite pins the same numbers against its archived
packet — so an edit on either side breaks a test on that side." Both halves fail.
The archive does not exist (openxFactory PR #1066 is still OPEN; the path 404s on
that repository's `main`, where the ACTIVE packet still stands), and a full grep
of a fresh clone of openxFactory `main` finds NEITHER digest anywhere in the
repository — no test there pins them. So there is no mutual breakage, and this
change should not have claimed a guarantee it does not hold. What is true is the
narrower thing now written: the digests are pinned HERE, against the source at
`cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, and an edit on THIS side fails a test
on this side. An edit on the openxFactory side would be caught by re-running the
measurement against that pin, not by a test over there.

## What changes

- The surviving `-v2` chat-turn family's two live requirements arrive in openDox's
  corpus, where the route that must satisfy them is going.
- **Nothing is promoted in openxFactory by this change, and nothing here removes
  anything**: the v1 removal is already done, elsewhere, and is not restated.

## Impact

- Affected specs: `ideation-dashboard` — **which does not exist in this corpus
  yet.** It arrives with `split-opendox-two-layer-product` § 5's shed, and until
  then this change cannot archive.
- Affected code: the chat-turn route and the workbench turn's envelope handling,
  as they arrive with the carve into `opensoft/openDox-code`.
- No schema byte moves here. `xfactory-workbench-chat-turn.schema.yaml` and the
  `contract-v3.0` bundle are openxFactory's.
