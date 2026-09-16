---
Status: draft
Re-homed-from: openxFactory `openspec/changes/add-doxchat-model-intake`, closed as re-homed 2026-09-16 under RULING Q6
Ratified-in-openxFactory: 2026-08-21 by Brett Heap — in-session, verbatim: "proposal approved", after the proposal landed on PR #236. The five Open Questions were ruled the same day in a follow-up in-session multiple-choice round (all five recommendations adopted).
code_surface: openDox-code (the doxBench chat rail's model selector and its intake affordance, the workbench model view's rungs, the catalog transport, the pending-declaration surface and approval gate action beside the model port, the proposed-vs-approved distinction in the model module, and the tests that prove all of it — as they arrive with the carve)
Depends-on: add-model-provider-broker (the credential broker and the binding this flow writes into) — an openxFactory change, itself blocked on openProfiler, unbuilt
---

# Proposal: add-doxchat-model-intake

## Why

`add-doxchat-model-intake` was ratified in `opensoft/openxFactory` on 2026-08-21
from Brett's browser annotation on the live doxBench chat rail, and built there
at `contract-v1.45`. RULING Q6 (2026-09-04T17:49Z, `opensoft/openxFactory` issue
#656) froze it where it stood and re-homed it: the MODEL PLANE is openDox's under
DIRECTION Q5's three-layer test and RULING C2, and `tasks.md` § 6.3 of
`split-opendox-two-layer-product` names openDox as its destination in terms.

The substance, restated so this corpus can be read without the other one: a
workbench model catalog can be empty, and when it is, the selector offered
nothing and the human had no way in. Intake is that way in — the selector offers
it FIRST and defaults to it when nothing is approved; the credential goes to the
broker and only a BINDING comes back; and approval stays a recorded human act
rather than a side effect of proposing a model.

## What changes

**One `## MODIFIED` block and four `## ADDED` requirements, carried
BYTE-IDENTICAL from the openxFactory delta** at openxFactory `main` `cb2d3a2c` —
`sha256 3168ad8f6f31c8dbacdc772d933508943f7b2c7cf373de2357eb8958d4bebee1`, 16,813
bytes, the digest this repository's `specs/ideation-dashboard/spec.md` carries.
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
carried because byte-fidelity is the property being preserved. The preamble's
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
  `action` enum member in `contracts/schemas/gate-action-record.schema.yaml` is
  ALREADY openxFactory contract bytes at `contract-v1.45`, and `tasks.md` § 6.3
  says it STAYS. Nothing here adds it, moves it, or reverts it, and
  `contract-v1.45` stays true as published.
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
