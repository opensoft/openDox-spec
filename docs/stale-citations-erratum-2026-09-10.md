# Ideation-Dashboard Session Runbook — Stale-Citation Erratum

Status: record
Kind: report
Captured: 2026-09-10
Repository context: openDox-spec
Corrects: `docs/ideation-dashboard-session-runbook.md`
Summary: Names the source-path citations in the arrived runbook that the carve left stale, and their live targets, without mutating the frozen document.
Topics: opendox, carve, ideation-dashboard, session-runbook, stale-citation

## Why this is a separate document, not an edit

`docs/ideation-dashboard-session-runbook.md` arrived at carve commit
`b075fd91dc8fced8e1373825ba80220c33536bae` (tag `opendox-carve-0`) as a
`moved_with_declared_edit` row of `docs/opendox-carve-manifest.yaml`
(`opensoft/openxFactory`, FLOOR PART 1). Its only touchable lines are the
six the manifest declares — the `python3 src/opendox/cli.py …` CLI-path
constants at lines 566, 774, 782, 789, 795 and 801 — already applied when
carve leg 2 landed (`opensoft/openDox-spec#4` → `fc67332d`). Every citation
below sits on a different line: touching any of them would be an undeclared
edit, and `scripts/verify-carve-arrival.py --phase B` (run from an
`opensoft/openxFactory` checkout against this repository) refuses any such
diff with `arrival-undeclared-edit`. Fixing them in place therefore needs a
Q-L1-family manifest amendment in `opensoft/openxFactory` (recorded on
`opensoft/openxFactory#656`, comment `5619228392`) — outside this
document's authority. This erratum is the correction of record until that
amendment lands, in the pattern already established by openxFactory's own
`docs/doxbench-runtime-refresh-dogfood-erratum.md`: it corrects without
mutating.

## The citations

Measured against `docs/opendox-carve-manifest.yaml` at `opensoft/openxFactory`
main (`85fb85622a2c83cca909d3bda7cae9be4ad6a713`, 2026-09-10) and the arrived
runbook's own text. None of the citations below is an import or an exec
edge — the runbook is prose, not code, so nothing executes against a stale
path; each is a documentation pointer a reader would otherwise follow to
nothing.

| runbook line(s) | cites | why it is stale | live target |
| ---: | --- | --- | --- |
| 5 | `Repository context: openxFactory` | self-referential header; the document now lives in this repository | `Repository context: openDox-spec` |
| 462–466 | `scripts/reserve-dashboard.sh` | no `docs/opendox-carve-manifest.yaml` row moves this script anywhere; it exists only in `opensoft/openxFactory` | `opensoft/openxFactory`'s `scripts/reserve-dashboard.sh` |
| 487 | `scripts/systemd/xfactory-dashboard.service` | no manifest row; openxFactory-only | `opensoft/openxFactory`'s `scripts/systemd/xfactory-dashboard.service` |
| 536, 998 | `ideation/dashboard/gate-records/` | `ideation/` is out of the carve's scope entirely; openxFactory-only | `opensoft/openxFactory`'s `ideation/dashboard/gate-records/` |
| 642 | `openxFactory/scripts/validate-ideation-dashboard-contracts.py` | the manifest moved this script to the openXdox-code leg | `opensoft/openXdox-code`'s `scripts/validate-ideation-dashboard-contracts.py` |
| 746, 777 | `ideation/staging/<topic-id>/` | openxFactory-only | `opensoft/openxFactory`'s `ideation/staging/<topic-id>/` |
| 751 | `ideation/brainstorm/` | openxFactory-only | `opensoft/openxFactory`'s `ideation/brainstorm/` |
| 884–886, 967, 969 | `scripts/sync-notebooklm-books.py` | no manifest row; openxFactory-only | `opensoft/openxFactory`'s `scripts/sync-notebooklm-books.py` |
| 1089 | `tests/ideation-dashboard/session_fixtures.py::build_scratch_repo` | the manifest moved this fixture to the openDox-code leg (also replicated at openXdox-code) | `opensoft/openDox-code`'s `tests/session_fixtures.py` |
| 1100 | `tests/ideation-dashboard/tools/playwright-smoke.py`, including the sentence "now lives IN THIS REPO at …" | the manifest moved this tool to the openXdox-code leg; the "in this repo" claim is now false here | `opensoft/openXdox-code`'s `tests/tools/playwright-smoke.py` |

Citations correctly attributed to a third repository already (for example
`docs/check-matrix.md` and `docs/pr-admission-merge-readiness.md`, both
explicitly named as codexFactory's) are not listed above: codexFactory was
not touched by this carve, so those citations remain live.

## Disposition

Owed: a manifest amendment (Q-L1-family) declaring the lines above so a
future commit B at `opensoft/openDox-spec` can correct them in place.
Recorded for the BUILD-arc register (`opensoft/openxFactory#656`).
