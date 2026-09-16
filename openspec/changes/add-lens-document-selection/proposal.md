---
Status: draft
Re-homed-from: openxFactory `openspec/changes/add-lens-document-selection`, closed as re-homed 2026-09-16 under RULING Q6 and RULING DQ-1
Ratified-in-openxFactory: Brett's three annotations of 2026-08-08 — the unreadable relationship tiles and their unlabelled count, "this is taking up too much space. what value does it bring?", and "when I hover on one of these documents, the corresponding dot should light up. I should have a checkbox on each one to generate the seed from checked"
code_surface: openDox-code (the keyword lens's matrix selection and cross-view document highlight, the collapsed signature grid with its stated finding, the drafted-seed panel's chrome, and the theme-token guards — as they arrive with the carve). **NOT the drafter**: `doc_health.staging_seed` and its serve route STAY in openxFactory under RULING DQ-1, which is what makes this the one re-homed change whose content does not land in one place.
---

# Proposal: add-lens-document-selection

## Why

`add-lens-document-selection` was ratified in `opensoft/openxFactory` on
2026-08-08 from three annotations Brett made in one session on the keyword lens,
and built there. RULING Q6 (2026-09-04T17:49Z, `opensoft/openxFactory` issue
#656) froze it where it stood and re-homed it: the lens, its views and the
set-builder are openDox's under DIRECTION Q5's three-layer test and RULING C2.

**THIS IS THE ONE RE-HOMED CHANGE WHOSE CONTENT DOES NOT LAND IN ONE PLACE**, and
the split does not fall between requirements — it falls INSIDE one.
`split-opendox-two-layer-product` `tasks.md` § 6.5 and `design.md` § D9 say it in
the same words: the set-builder half comes here, and its
`doc_health.staging_seed` drafter and its serve route **STAY in openxFactory's
own adapter** under RULING DQ-1 (2026-09-04T22:14Z).

**EVERY `split-opendox-two-layer-product` CITATION IN THIS CHANGE IS THAT PACKET,
IN `opensoft/openxFactory`, AT `cb2d3a2c`** — it has no copy in this corpus and
never will, which is what makes this change its successor rather than its
continuation.

## What changes

The delta arrives **WHOLE and byte-identical** — all five `## ADDED`
requirements, 8,363 bytes, `sha256 48b9a60c…`, `diff`-verified against the
archived copy in openxFactory — and the narrowing the second requirement owes is
carried as a BLOCKED OPEN BOX (`tasks.md` § 2.1) rather than performed here.

| # | requirement | side |
| --- | --- | --- |
| 1 | *Every view of a document is one hover away from the others* | openDox |
| 2 | *A document selection drafts a staging-queue seed* | **BOTH — see § 2.1** |
| 3 | *A finding is stated before it is drawn* | openDox |
| 4 | *A panel in contested space carries one row of chrome* | openDox |
| 5 | *The theme owns every colour a view chooses* | openDox |

Requirement 2 states both halves in one sentence — *"The lens matrix SHALL let a
human select documents and SHALL draft a staging-queue fragment covering exactly
the selected set"* — and its drafting clauses are openxFactory's in terms: the
draft *"SHALL write nothing"*, the evidence *"SHALL be recomputed by the serving
side from its own snapshot"*, an unknown document *"SHALL be refused by name"*.
Those are obligations on the drafter and the route, not on the matrix.

**Why it travels whole rather than pre-split**, stated here because it is the one
judgement this arrival makes:

1. Splitting a ratified requirement's sentences is AUTHORING, not carriage, and
   RULING Q6 freezes the five where they stand. Every other § 6 closure moved
   ratified text unedited.
2. The openxFactory half has nowhere to land TODAY: under DQ-1 it belongs to
   openxFactory's own adapter, whose successor capability is
   `split-opendox-two-layer-product` § 5.2a — unbuilt — and `corpus-adapter-seam`
   is an unpromoted delta of that same packet.
3. Carrying whole loses nothing and is reversible. Dropping requirement 2 would
   lose it from every destination at once; ratifying it here as it stands would
   assert openDox owns a `doc_health` drafter DQ-1 says it does not — which is
   why § 2.2 bars exactly that until § 2.1 lands.

## Impact

- Affected specs: `ideation-dashboard` — **which does not exist in this corpus
  yet.** It arrives with `split-opendox-two-layer-product` § 5's shed, and until
  it does this change cannot archive (`tasks.md` § 1.2). `openspec validate
  --strict` passes and says so.
- Affected code: the lens's views and styles, as they arrive with the carve into
  `opensoft/openDox-code`. No code moves in this change.
- **Not affected, deliberately:** `doc_health/staging_seed.py` and
  `/actions/staging-seed`, which stay openxFactory's under RULING DQ-1.
- No schema, contract or register change.
