---
Status: draft
Re-homed-from: openxFactory `openspec/changes/add-composed-view-authoring`, closed as re-homed 2026-09-16 under RULING Q6
Ratified-in-openxFactory: Brett, 2026-08-08 — "yes, we need to draft from a project view", after the hand-off was found unavailable on every project-scoped view
code_surface: openDox-code (the serve declares its writable repository on its capabilities route; the lens's drafted-seed hand-off and the workbench's openDraft read the unstripped capability; tests)
---

# Proposal: add-composed-view-authoring

**THIS IS THE FIRST CHANGE IN THIS CORPUS.** `openspec/changes/` has held only
`.gitkeep` since the leg was scaffolded. It arrives here because
`split-opendox-two-layer-product` § 6.4 closes the openxFactory packet of the
same id AS RE-HOMED, and § 8.5 requires each of the five re-homed changes to
have "its destination named in the receiving repository". This is that naming.

## Why

`add-composed-view-authoring` was ratified in `opensoft/openxFactory` on
2026-08-08 and built there. RULING Q6 (2026-09-04T17:49Z, `opensoft/openxFactory`
issue #656) froze it where it stood and re-homed it: composed views and the
project object are openDox's — "the neutral app a student or a lab assistant
would use" — under DIRECTION Q5's three-layer test and RULING C2.

The packet's own per-requirement successor map says where this requirement goes
and in whose voice: *"the requirement is re-promoted in `opensoft/openDox`'s own
OpenSpec instance"* — the `Composed views are read-only with a repository jump`
row of `opensoft/openxFactory`
[`openspec/changes/split-opendox-two-layer-product/specs/ideation-dashboard/spec.md`](https://github.com/opensoft/openxFactory/blob/cb2d3a2c24e948d4cc2c10a97046a5cc03cf1f9a/openspec/changes/split-opendox-two-layer-product/specs/ideation-dashboard/spec.md)
at `cb2d3a2c` (blob `21fea062`). The openxFactory
disposition therefore promotes NOTHING into openxFactory canon — the packet says
so twice — and this change is where the delta actually lands.

**EVERY `split-opendox-two-layer-product` CITATION IN THIS CHANGE IS THAT
PACKET, IN `opensoft/openxFactory`, AT `cb2d3a2c` — never a local one.** It has
no copy in this corpus and never will: it is openxFactory's own packet, which is
what makes this change its successor rather than its continuation. Paths written
bare below (`tasks.md` § 5, § 6.4, § 8.5, and `design.md` § D9) are paths in THAT
repository at THAT revision, pinned because `main` moves and a section number is
reproducible there and nowhere else by guarantee. `design.md` is named in this
list explicitly: the sentence enumerated only the `tasks.md` references until
Copilot's reading of openDox-spec #12 pointed out that a reader following the
lone `design.md` citation would resolve it as a local file and fail, this corpus
having no such file either.

The substance is unchanged and is restated here only so this corpus can be read
without the other one: `Composed views are read-only with a repository jump`
stated its own reason as "a gate verb binds to one served checkout, and a
composed view has none". That is true of a verb bound to a TILE and false of
creating a NEW document, which binds to no tile and lands in the serve's own
checkout. The blanket rule made the one view where cross-repository convergence
is visible the one view unable to act on it.

## What changes

**One `## MODIFIED` block, carried BYTE-IDENTICAL from the openxFactory delta**
at openxFactory `main` `cb2d3a2c` —
`sha256 1754e5d3f9803ea80b4e8a177fda8359a96d6c4b1024fce69893ee3cb3d716e1`, 3,557
bytes, the same digest THIS CHANGE'S OWN
`openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md`
carries — written in full because a bare `specs/ideation-dashboard/spec.md` reads
as a repository-level path, and this corpus has no such file: the promoted
specification is openxFactory's and does not travel. The comparand in
openxFactory is the SOURCE DELTA'S OWN blob — openxFactory
`openspec/changes/add-composed-view-authoring/specs/ideation-dashboard/spec.md`
at `cb2d3a2c`, blob `b14869b2`, 3,557 bytes — and NOT blob `21fea062` cited in
§ Why, which is the 217,269-byte `split-opendox-two-layer-product` successor map,
a different file cited for a different purpose: a digest of that file cannot
verify anything about this one. The byte-fidelity claim is in fact stronger than a
digest match, and a reader can take it with one command: `git hash-object` over
this change's carried file returns `b14869b210c92a2d3e71300b4c53a33b95536511`,
which IS openxFactory's blob id — the same git object, not merely the same bytes.
So the claim is checkable against the change-local file and against that blob, and
against nothing else. NOT ONE CHARACTER WAS EDITED, deliberately: the carve's safety property
is fidelity, the requirement's subject is already the SERVE rather than a
repository name (so none of the prose edits `split-opendox-two-layer-product`
permits at the seam — "the subject `openxFactory SHALL` becomes the receiving
repository's" — is owed here), and an unedited block is the one a reviewer can
check with `sha256sum` instead of a reading.

Carried with it, and disclosed rather than silently dropped: the requirement body
ends with a `**Merged into … by add-composed-view-authoring (2026-08-27):**`
marker naming the scenario `Gate verbs hide on a composed view`. That marker is
openxFactory prose-tagging vocabulary recording a scenario rename inside the
openxFactory corpus. It is carried because it is part of the ratified requirement
text and byte-fidelity is the property being preserved; it is NOT a claim that
this corpus ever held the merged-from scenario.

## Impact

- Affected specs: `ideation-dashboard` (MODIFIED: `Composed views are read-only
  with a repository jump`)
- Affected code: `opensoft/openDox-code` — the capabilities route, `app.js`,
  `views/lens.js`, `views/staging-workbench.js`, as they arrive with the carve.
- **THIS CHANGE CANNOT ARCHIVE YET, AND THAT IS THE HONEST STATE RATHER THAN A
  DEFECT.** `openspec validate --strict` passes and says so in the same breath:
  *"Archive would refuse this delta: ideation-dashboard: target spec does not
  exist; only ADDED requirements are allowed for new specs."* The capability
  `ideation-dashboard` reaches this corpus with
  `split-opendox-two-layer-product` § 5's shed of openxFactory's promoted
  specification — 102 requirements, of which 71 are openDox's. A `## MODIFIED`
  block is the delta this change has always carried and re-homing does not
  convert it into an `## ADDED`; it waits for its base, which is exactly what
  "the five stop where they stand; their live deltas and open tasks re-home"
  (`design.md` § D9) describes.
- **Standing.** The requirement TEXT was ratified by Brett Heap in openxFactory
  on 2026-08-08 and that act is cited in this proposal's front matter, unedited.
  Its ratification IN THIS CORPUS is openDox's own owed act and is NOT claimed
  here: the packet says the content is "re-authored in the receiving repository",
  and a lane cannot manufacture a ratification in a corpus that has never held
  one. `Status: draft` is therefore the honest standing on arrival, not a
  downgrade of the openxFactory act.
