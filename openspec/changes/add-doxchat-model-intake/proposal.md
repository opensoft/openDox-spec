---
Status: draft
Re-homed-from: openxFactory `openspec/changes/add-doxchat-model-intake`, closed as re-homed 2026-09-16 under RULING Q6
Ratified-in-openxFactory: 2026-08-21 by Brett Heap — in-session, verbatim: "proposal approved", after the proposal landed on PR #236. The five Open Questions were ruled the same day in a follow-up in-session multiple-choice round (all five recommendations adopted).
code_surface: openDox-code (the doxBench chat rail's model selector and its intake affordance, the workbench model view's rungs, the catalog transport, the pending-declaration surface and approval gate action beside the model port, the proposed-vs-approved distinction in the model module, and the tests that prove all of it — as they arrive with the carve)
Depends-on: add-model-provider-broker (the credential broker and the binding this flow writes into) — an openxFactory change, and DISCHARGED — archived 2026-08-27 at `opensoft/openxFactory` `openspec/changes/archive/2026-08-27-add-model-provider-broker` (archive commit `fff79620`, 2026-08-27T03:19:38Z, "The surface merged and ran green on main, so the broker's four requirements reach canon"), present under that path both at the frozen source `cb2d3a2c` and on today's openxFactory `main`. CORRECTED 2026-09-16 — this field previously read "itself blocked on openProfiler, unbuilt", which was the source packet's status from before that archive and is false now — it is corrected rather than carried because this field is re-authored prose in this corpus and not part of the carried delta, which is this change's `specs/ideation-dashboard/spec.md` alone
---

# Proposal: add-doxchat-model-intake

## Why

`add-doxchat-model-intake` was ratified in `opensoft/openxFactory` on 2026-08-21
from Brett's browser annotation on the live doxBench chat rail, and built there
at `contract-v1.45`. RULING Q6 (2026-09-04T17:49Z, `opensoft/openxFactory` issue
#656) froze it where it stood and re-homed it: the MODEL PLANE is openDox's under
DIRECTION Q5's three-layer test and RULING C2, and § 6.3 of
`split-opendox-two-layer-product`'s task ledger names openDox as its destination
in terms. **Pinned, because `main` moves:** `opensoft/openxFactory`
`openspec/changes/split-opendox-two-layer-product/tasks.md` at
`cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, blob
`a3470096010d7279b38011e02cefaaada1d7b88f` (114,414 bytes), § 6.3 at line 1502 —
*"`add-doxchat-model-intake` → openDox. Built but unarchived; its code moves with
the carve as `moved_with_declared_edit` rows, its four ADDED requirements are
re-authored in openDox, and its one additive schema enum member is already
`openxFactory` contract bytes and STAYS."* That ledger has moved on `main` since
(amendment #3, openxFactory #1035), which is precisely why this cites the blob
and not a branch.

The substance, restated so this corpus can be read without the other one: a
workbench model catalog can be empty, and when it is, the selector offered
nothing and the human had no way in. Intake is that way in — the selector offers
it FIRST and defaults to it when nothing is approved; the credential goes to the
broker and only a BINDING comes back; and approval stays a recorded human act
rather than a side effect of proposing a model.

**`credential-contracts` is an openxFactory capability and THIS CORPUS DOES NOT
HOLD IT**, so the binding shape the carried requirements name is pinned rather
than assumed: `opensoft/openxFactory` `openspec/specs/credential-contracts/spec.md`
at `cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, blob
`36201e058d1f06bc88383473a2ec1ebc9f02ce28`, 65,999 bytes. An implementer reading
the required binding fields — provider, secret reference, owner, rotation policy —
reads them there, at that blob, and nowhere else by guarantee. Whether openDox
carries that contract, pins it, or keeps it an external dependency is an OWED
DECISION with a box of its own — **`tasks.md` § 1.5** — not a side effect of
ratification. (It pointed at § 1.4 until 2026-09-16; § 1.4 records only this
corpus's ratification act and would have let this change close with the contract
source still unnamed, which is the one outcome a carried requirement consuming an
external binding shape must not permit.) This change makes no claim to own the
contract and does not restate its fields, because a restatement in a corpus that
cannot validate it is a second source of truth.

## What changes

**One `## MODIFIED` block and four `## ADDED` requirements, carried
BYTE-IDENTICAL from the openxFactory delta.** THE SOURCE, in full and immutably:
`opensoft/openxFactory` at `cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, file
`openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md`,
blob `3de54f7ee6f24f890d8e305914b592340b53d274` — 16,813 bytes,
`sha256 3168ad8f6f31c8dbacdc772d933508943f7b2c7cf373de2357eb8958d4bebee1`. This
repository's copy carries that digest and that byte count, and — because git
names content — that same blob id: `git hash-object` reads `3de54f7e…` on BOTH
sides, so the two files are ONE GIT OBJECT rather than
two copies that happen to agree. **The copy is at
`openspec/changes/add-doxchat-model-intake/specs/ideation-dashboard/spec.md`**,
spelled from this repository's root, because that is the file a reader has to run
`sha256sum` over. A change's delta is conventionally written change-relative as
`specs/<capability>/spec.md`, and this sentence used to spell it that way while
saying "this repository's" — which points at a root-level `specs/` directory that
does not exist here, next door to `openspec/specs/`, the canon location, which
holds a different thing entirely. A hash instruction is the last place to leave
that ambiguity. The digest is of THAT FILE; it is not a claim
about every file of the packet (see § 5's preamble in `tasks.md`).
NOT ONE CHARACTER WAS EDITED. The seam permits one class of prose edit — "the
subject `openxFactory SHALL` becomes the receiving repository's" — and none is
owed: the string `openxFactory` does not occur in the delta at all (measured:
`grep -c openxFactory` → 0). Its subjects are the dashboard backend, the browser,
the selector and the adapter.

- MODIFIED: *doxBench model catalog and provider boundary* — one of the FOUR
  promoted titles the split packet's § THE SIBLING COLLISION table (a) names,
  with openDox as its destination.
- ADDED: *The model selector offers intake first and defaults to it when nothing
  is approved*, *Model intake hands the credential to the broker and keeps only a
  binding*, *Intake proposes a model; approval stays a recorded human act*, *The
  intake affordance ships with the flow behind it* — four of the TWELVE titles
  that table's (b) half records as "not in canon and NOT removed here", handled
  by the re-homing plan instead. **This is the first closure to exercise that
  half**, and it is why these four arrive as an authoring act here rather than
  as a promotion there.

Carried with it, and disclosed rather than silently dropped: the delta's preamble
declares itself relative to `add-doxbench-distilled-abstract` and cites
`release-realization/spec.md:64-74`. Both are openxFactory referents, and both are
carried because byte-fidelity is the property being preserved. **The carried
spelling is not reproducible from this corpus** — that relative path exists in
neither repository as written — so the referent is pinned HERE, beside the
disclosure, without touching the carried bytes: `opensoft/openxFactory`
`openspec/specs/release-realization/spec.md` at
`cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a`, blob
`5572301996e8e3714b0e79aa3d71474b266d88a6`, 47,106 bytes. Lines 64-74 are lines
of THAT blob and of no branch; `main` moves and the preamble's bare path does
not follow it. The preamble's
closing instruction — *"Re-verify this block against canon before archiving"* —
is now owed against OPENDOX's canon, and `tasks.md` § 1.3 carries it as an open
box rather than leaving it inside prose nobody re-reads.

## Impact

- Affected specs: `ideation-dashboard` (1 MODIFIED, 4 ADDED)
- Affected code: `opensoft/openDox-code`, as it arrives with the carve. The
  openxFactory packet's built code moves as `moved_with_declared_edit` rows of
  `docs/opendox-carve-manifest.yaml`; that is § 3's work and no code moves in
  this change.
- **THE ONE ADDITIVE SCHEMA ENUM MEMBER DOES NOT TRAVEL.** The approval act's
  `action` enum member is ALREADY openxFactory contract bytes at the published
  tag, and § 6.3 of the split packet's ledger (blob `a3470096…`, line 1502) says
  it STAYS. **Pinned — and here the pin is load-bearing, not decorative:**
  `opensoft/openxFactory` `contracts/schemas/gate-action-record.schema.yaml` at
  tag `contract-v1.45` (commit `7b7447da8f769c2884d7586959e5fecb4b6eeb00`), blob
  `7f95006f768fbc2f4422d49642ba5ca0afbbac7f`, 45,078 bytes. MEASURED 2026-09-16
  across four refs: PRESENT at `contract-v1.45`, PRESENT at `contract-v1.44`
  (blob `2e760dc811aa7f897dd3b9778996b6085486b9b5`, 36,157 bytes), and **ABSENT
  both at the frozen source `cb2d3a2c` AND on today's openxFactory `main`** — a
  code search over that repository returns zero hits for the filename. So a
  reader who checked the branch would conclude the file does not exist and this
  disposition is false; at the tag it is exactly where this says it is. That is
  what "already contract bytes at `contract-v1.45`" means, and why the tag rather
  than a branch is the only reference that can carry the claim. Nothing here
  adds it, moves it, or reverts it, and `contract-v1.45` stays true as published.
- **THIS CHANGE CANNOT ARCHIVE YET.** `openspec validate --strict` passes and
  says why: *"Archive would refuse this delta: ideation-dashboard: target spec
  does not exist; only ADDED requirements are allowed for new specs."* The
  capability reaches this corpus with `split-opendox-two-layer-product` § 5's
  shed. Re-homing does not convert a `## MODIFIED` block into an `## ADDED` one;
  it waits for its base.
- **Standing.** The requirement text was ratified by Brett Heap in openxFactory
  on 2026-08-21 and that act is cited unedited in the front matter. Its
  ratification IN THIS CORPUS is openDox's own owed act and is not claimed here:
  the packet says the content is "re-authored in the receiving repository", and a
  lane cannot manufacture a ratification in a corpus that has never held one.
