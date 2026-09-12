# The Front-End Package Boundary openDox Has To Invent

Status: draft
Amended: 2026-09-12 (#1) — the five open questions RULED (#656 comment
5642758731); 2026-09-12 (#2) — five corrections and a sixth open question, Q6
(#656 comment 5647678655). The full record is § 7.
Kind: architecture
Repository context: openDox-spec
Realizes: `split-opendox-two-layer-product` `tasks.md` § 3.4 (`opensoft/openxFactory`)
Closes-design-for: the front-end half of the two-layer split — `design.md` § D3's
last paragraph and risk 7
Purpose: settle WHERE the line through `src/opendox/web/` runs, WHAT test puts a
file on each side, and HOW the line is held in code without forking the bundle —
so that § 3.4's code half is a mechanical set of moves against a written boundary
rather than an invented one.
Topics: opendox, openxdox, front-end, package-boundary, ruling-c2, split-opendox

> **This note designs; it does not build.** No file under `src/opendox/web/`
> moves with it, no route binding changes, and no test is written by it. What it
> adds is a census, a rule, a mechanism and an ordered slice list. § 6 carries
> the questions a ruling must settle before the first slice starts — **and,
> since amendment #2, one (Q6) that a ruling must settle before the LAST slice
> can start.** § 7 is the note's own amendment record.

**Everything measured here was read live on 2026-09-11 at these heads:**
`opensoft/openDox-code` `main` `a99eba03e31a0aee1cc15a061fdf718cc88a2c44`,
`opensoft/openXdox-code` `main` `af15f71207797214ffd6340267b5cb2ecb40bf6a`,
`opensoft/openxFactory` `main`. Every path in the census was verified present at
that openDox-code head; every line number was read at it. **The census tree is
still `a99eba03`** and amendment #2 did not re-measure it: every `views/*.js`
line this note cites is a line at that commit, and amendment #2 re-verified the
three it newly names (`app.js`:45, `dispose.js`:396, `wheel.js`:140–146) there.

**Amendment #2 (2026-09-12) additionally read, and cites by their own sha:**
`opensoft/openDox-code` `build/s3-view-registry`
`a497d7156f63a920a750171dfe9b9bd1fc06e8d7` and its later head
`e176947dd3691fa96b285575910989ed77e09181` (slice S3, PR #14, OPEN — the tree
the § 4.1 registry actually exists on); `opensoft/openXdox-spec`
`docs/gate-loop-view-contract.md` `d73767b7`; `opensoft/openxFactory` `main` at
`177ba8196e16097e30aeb3f946ca8291b9ba4e92`, whose two documents this note cites
by line are `docs/opendox-carve-manifest.yaml` (blob
`e6c3925a08e51802598f4f9f421228b203d664ca`, last moved by openxFactory `#1002`
`b3cc0181`) and `docs/opendox-cutover-runbook.md` (blob
`ef1d439b5a39afc66036e1833f8d96f8eb9bf551`, last moved by `972b484a`) — **pinned
because `main` moves**, and a line number in either is reproducible at that
commit and at those blobs and nowhere else by guarantee. **A
citation at one of those shas is NOT a census measurement**, and each is marked
with the sha it was read at, because the shell has moved under this note twice
since 2026-09-11 and a line number carried across a head is a false citation.

---

## 1. Why a boundary must be INVENTED

`design.md` § D3 ends on the sentence this note exists to act on:

> **The web tier is where a student-usable openDox is won or lost, and it was
> not measured for this split.** 40 files, 30,410 lines, and NO package boundary
> at all today — so its boundary must be INVENTED rather than discovered.

`tasks.md` § 3.4 makes it its own task, and risk 7 names the mitigation: *"The
front end has no package boundary to discover. Mitigation: § 3.4 makes inventing
one its own task, and names it as where a student-usable openDox is won or
lost."*

### 1.1 The tree, measured

At openDox-code `a99eba03`, `src/opendox/web/` carries **42 blobs — 40
hand-authored files and 2 vendored — totalling 30,585 lines, of which 30,583 are
hand-authored.** The shape is three files at the root of `web/` (`index.html`
119, `app.js` 1,155, `styles.css` 2,574), 37 files under `web/views/`, and
`web/vendor/` (`.gitkeep` 0 lines; `markdown-it.min.js` 2 lines / 123,618 bytes).

**Reconciling the packet's figure.** `tasks.md` § 3.4 and `design.md` § D3 both
say *"40 files, 30,410 lines"*. The tree those were measured against —
openxFactory's `scripts/ideation_dashboard/web/` at the carve commit
`b075fd91dc8fced8e1373825ba80220c33536bae` (tag `opendox-carve-0`) — carried
**43 blobs**, i.e. 41 hand-authored. The live openDox-code tree carries 40
hand-authored because exactly one file did not travel: `views/intent-feed.js`
(483 lines), RULED `not_moved / stays_openxfactory_adapter`
(`docs/opendox-carve-manifest.yaml`:1807–1810, under RULED OQ-F). The packet's
count is a pre-carve measurement the tree has since moved past; it is recorded
here, not corrected here — a packet figure is amended in the packet (§ 5, S7).

### 1.2 There is no boundary — four measurements that say so

**(a) The bundle is a flat directory with one import graph.** `index.html` loads
exactly one module (`<script type="module" src="./app.js">`); `app.js` imports 20
sibling modules by relative path; those import each other. There is no
subdirectory, no manifest, no naming convention, no lint rule and no test that
says which module may import which. `views/` is 37 files in one folder.

**(b) One import in that graph is already dangling.** `views/dispose.js`:26 and
`views/wheel.js`:75–76 both `import … from "./intent-feed.js"` — a module RULED
to stay at openxFactory and therefore absent from this leg. `app.js`:34 imports
`wheel.js`, so the shell's own module graph does not resolve at
`openDox-code` `main` today. The carve did not do this wrongly: the manifest row
is a deliberate ruling, and the two importers are `moved_verbatim` rows. **The
defect is that nothing in the front end could express the edge**, which is
exactly what "no package boundary" means. `styles.css`:1278–1295 styles the same
absent module's chips. *(Amended 2026-09-12 (#2): "does not resolve … today" was
the measurement at `a99eba03`. Q5 is RULED and slice S2 has LANDED —
openDox-code `#15` → `main` `c7ab3d87`, the chips now an optional contributed
binding at `views/intent-binding.js`. § 4.1's finding records what S2's landing
left declared but unhosted.)*

**(c) Thirteen route constants — and one COMPUTED route the constants grep
cannot see — in five openDox view files address a prefix openXdox owns.**
`openxdox/serve_gate.py`:55 declares
`ACTIONS_GATE_PREFIX = "/actions/gate/"` and contributes it as a POST prefix
binding (`serve_gate.py`:238–243). Every one of these sits under it:

| file:line | constant | value |
| --- | --- | --- |
| `views/dispose.js`:28 | `GATE_DISPOSE_ROUTE` | `/actions/gate/dispose-possible` |
| `views/dispose.js`:29 | `GATE_PROPOSE_ROUTE` | `/actions/gate/propose` |
| `views/gate.js`:120 | `GATE_RATIFY_ROUTE` | `/actions/gate/ratify` |
| `views/lens-model.js`:1036 | `LENS_SAVE_ROUTE` | `/actions/gate/lens-save-recipe` |
| `views/lens-model.js`:1037 | `LENS_CLUSTER_ROUTE` | `/actions/gate/lens-add-as-cluster` |
| `views/repo-selector.js`:39 | `ACTIONS_CREATE_PROJECT_ROUTE` | `/actions/gate/create-project` |
| `views/repo-selector.js`:43 | `ACTIONS_EDIT_PROJECT_ROUTE` | `/actions/gate/edit-project` |
| `views/staging-workbench-model.js`:543 | `CREATE_ROUTE` | `/actions/gate/create-document` |
| `views/staging-workbench-model.js`:817 | `EDIT_DOCUMENT_ROUTE` | `/actions/gate/edit-document` |
| `views/staging-workbench-model.js`:818 | `OPEN_PR_ROUTE` | `/actions/gate/open-pr` |
| `views/staging-workbench-model.js`:821 | `FIRST_EDIT_ROUTE` | `/actions/gate/first-edit` |
| `views/staging-workbench-model.js`:822 | `ABANDON_SESSION_ROUTE` | `/actions/gate/abandon-session` |
| `views/staging-workbench-model.js`:826 | `SHARE_SESSION_ROUTE` | `/actions/gate/share-session` |

**Amended 2026-09-12 (#2) — a FOURTEENTH site, and it is not a constant.**
`views/dispose.js`:396 posts to `"/actions/gate/" + verb`, with the four verbs
supplied by its caller: `views/wheel.js`:140–146 mounts
`promote-to-staging`, `research-brief`, `derive-possibles` and `demote` through
one generic mounter (both read at the census tree `a99eba03`). The counterpart
note found it (openXdox-spec `docs/gate-loop-view-contract.md` § 8 Q12 @
`d73767b7`, measuring the same two lines at S3's `a497d715`). The thirteen above
are what a grep for a route LITERAL returns; this one is a concatenation, so it
is invisible to that grep and to every check built on one — including § 4.5's own
assertion 2, which is why the measurement is recorded here rather than only
there. **The count that holds is therefore: thirteen declared constants and
FOURTEEN gate-route SITES**, the fourteenth reaching four routes. What the note
does NOT do here is decide how the site declares itself — the counterpart's Q12
recommends the binding ENUMERATE the four as literals, and that question is
openXdox-spec's and is OPEN.

`views/viewer.js` and `views/wheel.js`:97 address `/source/`, and
`views/repo-selector.js`:33 addresses `/snapshot-index.json` — both declared by
`openxdox/serve_projection.py` (`SOURCE_PREFIX`:57, `SNAPSHOT_INDEX_ROUTE`:56),
so **the read-only document viewer, the most obviously student-usable surface in
the tree, cannot render a document without the consumer layer serving the
route.** *(That was the measurement at `a99eba03`, and it is what § 6's Q4 was
asked about. Q4 is RULED and slice S6 is realizing it — § 3.3 carries the
amended ownership and the two pull requests. The `/snapshot-index.json` half is
untouched by Q4 and stands.)*

**(d) The tests that hold the bundle are split across two repositories and
neither half runs.** 25 test files at openDox-code `tests/` name a
`views/<name>.js` path; **23 at openXdox-code do too, and every one of them
resolves it under `REPO_ROOT / "src" / "openxdox" / "web"`** — a directory
openXdox-code does not have (`tests/test_renderer.py`:39,
`test_wheel_model.py`:78, `test_staging_workbench.py`:49,
`test_gate_console.py`:58, `test_canvas.py`:45 …). The carve's `import rewrites`
edit class rewrote the path constant and pointed the tests at the wrong leg.
Neither set runs today: openDox-code's `validate` executes exactly
`tests/test_leg_shape.py tests/test_consumer_reach.py
tests/test_profile_registration.py --noconftest` (RULED Q-L5 (b′)), and
openXdox-code's is narrowed on the same grounds (RULED Q-L8 (b′)). **When those
narrowings lift, 48 test files have to know which leg owns the bundle — and
today nothing tells them.**

### 1.3 What follows

(b), (c) and (d) are three spellings of ONE fact: the web tier's cross-column
edges exist, they are load-bearing, and the front end has no vocabulary for
them while the Python side has three (`route_extension.RouteBinding`,
`consumer_reach`, `domain_profile.register`). The boundary this note invents is
that vocabulary.

---

## 2. The principle

### 2.1 Three destination classes

`tasks.md` § 3.4 states them: *"Account menu, canvas, editor, chat, docs tile and
theme controls are openDox; the gate console and drill-in are the gate loop; the
wheel, funnel and lens regions carry stage names."* Written as classes, with
`design.md` § D3's own Q5 test applied to a FILE rather than a module:

**Class A — openDox core.** The file renders a surface someone with no notion of
factories, gates or tenants would use. **The test:** it names no governance
status or stage word, and it addresses no route another column declares. It
ships in `openDox-code` and a descendant never touches it.

**Class B — the gate loop.** The file's subject IS a gate act: it addresses a
route under `serve_gate.ACTIONS_GATE_PREFIX`, or it builds the descriptor for a
gate verb (`demote` / `edit` / `ratify` / `kickoff`). **The test:** delete the
gate column and the file has nothing left to render. Its BINDING belongs to
`openXdox-code` through the seam § 4 describes; by RULING C2's own logic a
student install must come up without it, and must not 404 on it.

**Class C — a stage-named region.** The file's STRUCTURE is neutral — a wheel, a
funnel, a bullseye, a column strip, a sectioned outline — and its NAMES are one
domain's mapping. **The test:** replace every governance word in it with a
placeholder and the file still renders correctly. **A class-C file stays in
`openDox-code` and is PARAMETERIZED**: its vocabulary comes from the registered
domain profile, never from a literal. This is RULING C2 applied one tier out —
*"a clinician using `MedxDox` never sees the word 'requirement'"* — and the
openXdox-spec note `docs/domain-profile-design-note.md` already settles the
profile's shape and its "resolve by ROLE, not by string" rule.

### 2.2 The three rules that fall out

1. **A class-A or class-C file may not name a route ANOTHER COLUMN declares.**
   Not "a class-B route": class B is the gate-loop subset, and § 3.3 measures
   three route owners, so the rule has to be stated over ownership or it misses
   two of the three kinds of breach the census actually found. In scope: every
   route under `serve_gate.ACTIONS_GATE_PREFIX` (class-B, 13 constants — and,
   amended 2026-09-12 (#2), ONE COMPUTED SITE reaching four more, § 1.2(c)),
   openXdox's PROJECTION routes (`/snapshot-index.json` and the three
   `/projections/*`; `/source` and `/source/` stood in this list as landed and
   left it with RULED Q4 — § 3.3), and openxFactory's adapter lanes
   (`/actions/dtn-seed`, `/actions/staging-seed`,
   `/actions/apply-register-edits`) — the last of which no class can ever own,
   because RULING DQ-1 keeps that column at openxFactory. That is what makes
   § 1.2(c) and § 3.3 defects rather than layout choices. `views/viewer.js` is
   the one census row that breaks the rule while staying class A, and it breaks
   it on a PROJECTION route, not a gate one: § 6's Q4 is the ruling that
   discharges it — by moving the route, not the file (slice S6). **Q4 is RULED
   and S6 is IN FLIGHT (§ 3.3), so the rule is unchanged and the breach it names
   closes when the two pull requests land — the rule did not become wrong, the
   OWNERSHIP it is read against moved.**
2. **A class-C file may not carry a governance word as a literal.** That is
   RULING C2, and it is why class C is a class rather than a footnote on class A:
   11,854 lines sit in it (2026-09-12: 14 files, after Q2 moved `explorer.js`
   into class C, #656 comment 5642758731).
3. **A SNAPSHOT SCHEMA KEY is not a stage name; a RENDERED WORD or a CORPUS PATH
   is.** Without this the rule is unusable, because the snapshot's own field
   names (`documents`, `clusters`, `possibles`, `staged_topics`, `changes`,
   `keyword_index`) appear in files that render no governance word at all. A
   class-A file MAY read a schema key; it may NOT carry a word it renders or a
   corpus path it walks.

   **Three class-A rows carry a rendered tail and are declared as such** in
   § 3.2 — `views/docs.js`:18 (`AREA_ORDER`, corpus paths), `views/grouping.js`
   :34–41 and :51–52 (`TALLY_FIELDS`' rendered labels, and two `status ===`
   literals), `views/repo-selector-model.js`:517–522 (`STATIONS`' rendered
   labels). They are parameterized with class C in slice S7, and the `(C tail)`
   marker on their row is what says so.

   **Two are declared EXEMPT, with the reason on the record** —
   `views/composed-model.js`:107–110 (`COMPOSED_COLLECTIONS`, six snapshot field
   names, never rendered) and `views/doxbench-state.js`:37 (`SCOPE_KINDS`, the
   three tile kinds a workbench session may be scoped to, a state key and not a
   label). § 4.5's assertion 4 carries them as a DECLARED exemption list with
   these reasons: an exemption that is silence is how a literal survives a
   vocabulary sweep.

### 2.3 What this note does NOT claim

It does not claim the three classes are three DIRECTORIES. Where the line is
drawn in the filesystem — one `web/` with a declared manifest, or `web/core/` +
`web/regions/` + a contributed `web/gate/` — is § 6's Q3, and the mechanism in
§ 4 works under either.

---

## 3. The census

Every file under `src/opendox/web/` at `a99eba03`, with its line count from that
tree. `LOC` is `wc -l`. `class` is A / B / C / `?` per § 2, plus **SPLIT** — a
file the 2026-09-12 ruling (§ 6) resolves into more than one destination but
that has not yet been physically divided in code. `evidence` names the
import or identifier that decided it.

### 3.1 Totals

| class | files | lines |
| --- | ---: | ---: |
| **A — openDox core** | 20 (18 hand-authored + 2 vendored) | 11,702 (11,700 hand-authored) |
| **B — the gate loop** | 4 | 1,597 |
| **C — stage-named region** | 14 | 11,854 |
| **SPLIT — ruled, not yet built (§ 6)** | 3 | 3,908 |
| **? — undecided (§ 6)** | 1 | 1,524 |
| **total** | **42 (40 hand-authored)** | **30,585 (30,583 hand-authored)** |

**Amended 2026-09-12 — four of the five `?` rows are now RULED** (Brett Heap,
#656 comment 5642758731, by interactive multi-choice). `views/explorer.js`
(279 lines) moves wholly to class C (Q2) — the totals above move it out of `?`
and into C in full. `views/repo-selector.js` (889), `views/staging-workbench-model.js`
(1,949) and `views/lens-model.js` (1,070) are RULED **SPLIT** (Q3): each keeps
its class-A (or class-A/C) substance in place and its class-B route constants
travel with the contributed binding that calls them, never with the model that
declares them. No code has moved yet — this note designs, it does not build —
so the three SPLIT files are counted here in their own transitional bucket
(3 files / 3,908 lines) rather than folded into A/B/C, and their own class(es)
will be re-derived from real line counts once S4 executes the split. Only
`views/lens.js` (1,524 lines) stays `?`: none of Q1–Q5 rules on its two
openxFactory-lane routes (`DTN_SEED_ROUTE`, `STAGING_SEED_ROUTE`), so its
tail's destination remains undecided pending a future ruling. Previously (at
landing, before this ruling): A 20 / 11,702; B 4 / 1,597; C 13 / 11,575;
`?` 5 / 5,711; total 42 / 30,585 — the same total lines and file count hold
now, re-bucketed.

### 3.2 The rows

| file | LOC | what it renders | class | evidence |
| --- | ---: | --- | :-: | --- |
| `app.js` | 1155 | the shell: the ONE snapshot fetch, the tab strip wiring, the seam bundle, cross-view navigation | A | imports 20 view modules; **TWO of them are class B** (amended 2026-09-12 (#2) — as landed this row said "its only class-B import is `gate.js`"): `gate.js` at :43 (`isGateBearing`, `mountGateBar`) and `swb-session.js` at :45 (`firstEditTransport`, called at :1015). § 4.1 and § 4.5 assertion 3 carry both |
| `index.html` | 119 | the page skeleton: header, seven tab buttons, seven view mounts, two overlay roots | C | the seven tab LABELS are stage names ("realization funnel", "the wheel", "pipeline board", "cluster canvas", "keyword lens", "doc list", "lineage & readiness"); mounts are `id="view-funnel"` … `id="view-lineage"` |
| `styles.css` | 2574 | every surface's styling, light and dark | C | defines four status colour tokens `--st-brainstorm` / `--st-staged` / `--st-proposal` / `--st-realized` (16 definitions, 164 uses); 104 distinct class selectors carry a stage or region name and 355 of its 2,574 lines mention one; :1278–1295 styles `intent-feed`, a module RULED to stay at openxFactory |
| `vendor/markdown-it.min.js` | 2 | the vendored MIT Markdown renderer (123,618 bytes) | A | `viewer.js`'s only external dependency; `html` option disabled |
| `vendor/.gitkeep` | 0 | — | A | directory keeper |
| `views/account-menu.js` | 181 | the header 👤 menu: signed-in name, derived access level, hosted logout | A | only import is `helpers.js`; reads `/capabilities` (openDox `serve.py`); `LOGOUT_ROUTE` :59 is answered by the hosted gateway, not by the app |
| `views/board.js` | 247 | the pipeline board's four lifecycle columns | C | the four column keys ARE lifecycle statuses; 25 governance literals |
| `views/bullseye.js` | 398 | the shared match-count bullseye SVG (rings, sectors, dots) | A | "PURE of view state… issues no network call of any kind"; only import is `lens-model.js`'s `GEOM`; zero governance literals |
| `views/canvas-model.js` | 215 | the pure cluster-canvas derivation: member pane, evidence board, possibles rail | C | exports `listCanvasClusters`, `supersedePlan`, `supersedeReason`, `DRAFTS_DIR` — cluster/possible/supersede are governance nouns |
| `views/canvas.js` | 404 | the cluster canvas's three panes | C | renders `canvas-model.js`'s output; 7 governance literals |
| `views/composed-model.js` | 329 | the multi-repository composed-snapshot derivation (cluster union, shared view, scoping) | A *(declared exempt)* | repository / project / membership nouns — RULING Q1's identity-and-coordination half, which is openDox's; `COMPOSED_COLLECTIONS` :107–110 is six SNAPSHOT FIELD NAMES, never rendered (§ 2.2 rule 3) |
| `views/dispose.js` | 427 | the gate dispose tray and its refusal panel | **B** | `GATE_DISPOSE_ROUTE` :28 and `GATE_PROPOSE_ROUTE` :29 both sit under `serve_gate.ACTIONS_GATE_PREFIX`; :396 COMPUTES four more under the same prefix from a caller-supplied verb (§ 1.2(c)); mounts on `actions.gate` capability |
| `views/doc-wheel.js` | 491 | the docs-pane wheel — one reel, no chrome | C | imports `wheel-model.js`; exports `DOC_TILE_VERBS` |
| `views/docs.js` | 189 | the doc list, grouped by area, with Topics chips | A *(C tail)* | zero governance literals — but `AREA_ORDER` :18 hardcodes `ideation/brainstorm` and `ideation/staging`, openxFactory's own corpus layout (§ 6 Q1) |
| `views/doxbench-chat-model.js` | 1097 | pure browser-session chat state | A | import-free by design; zero governance literals |
| `views/doxbench-chat.js` | 1828 | the doxBench chat rail: subject, model selector, transcript, composer | A | imports ONLY the pure chat model; transports injected from `app.js` |
| `views/doxbench-editor.js` | 2966 | the doxBench authoring canvas: Outline + Document buffers, preview, switch guard | A | imports `viewer.js` and `doxbench-state.js` only; the largest single file in the tree |
| `views/doxbench-save.js` | 509 | the ordered Save orchestration | A | import-free; one injected transport |
| `views/doxbench-state.js` | 1049 | buffer primitives, UTF-8 bounds, content identity | A *(declared exempt)* | import-free; `SCOPE_KINDS` :37 is the three tile kinds a session may be scoped to — a state key, never a label (§ 2.2 rule 3) |
| `views/edit.js` | 48 | the select-to-edit transport | A | `ACTIONS_EDIT_ROUTE` :5 = `/actions/edit`, answered by openDox's own `serve.py` |
| `views/explorer.js` | 279 | the drill-down explorer: a staged/proposal/realized tile opened as its artifact folder | C | `classifyChangeFile`; reads `staged_topics[].files` / `changes[].files`; 5 governance literals — a projection whose only domain content is the artifact-folder vocabulary. RULED Q2, not class B: § 3.4's "drill-in" is `dispose.js`'s refusal panel, already class B (Brett Heap, 2026-09-12, #656 comment 5642758731) |
| `views/funnel.js` | 538 | the realization funnel's six columns and its hand-drawn edges | C | imports `model.js`'s `COLUMN_KEYS`; 10 governance literals |
| `views/gate.js` | 184 | the human gate-console bar | **B** | `GATE_ACTIONS = ["demote","edit","ratify","kickoff"]` :11; `GATE_RATIFY_ROUTE` :120 under the gate prefix; its Python counterpart `gate_console.py` is openXdox's |
| `views/grouping.js` | 246 | the project / project-group roll-up bar | A *(C tail)* | a pure renderer-side roll-up over already-resolved snapshot fields — but `TALLY_FIELDS` :34–41 pairs each schema key with a RENDERED label (`docs`, `clusters`, `possibles`, `staged`, `proposals`, `realized`) and :51–52 test `c.status === "active"` / `"archived"` (§ 2.2 rule 3; parameterized in S7) |
| `views/helpers.js` | 58 | `el()` / `txt()` / `basename()` / heat bands — the textContent-first DOM discipline | A | no import, no literal, no route |
| `views/lens-model.js` | 1070 | lens geometry, matching, co-occurrence, label layout | **SPLIT** | pure and import-free (class A substance) — `LENS_SAVE_ROUTE` :1036 and `LENS_CLUSTER_ROUTE` :1037 are class-B tails that travel with the binding that calls them, never with the model (RULED Q3, Brett Heap, 2026-09-12, #656 comment 5642758731); not yet built — the two constants stay in-file until S4 |
| `views/lens.js` | 1524 | the keyword-lens set-builder surface | **?** | `VOCABULARIES` :57 is a class-C vocabulary table; `DTN_SEED_ROUTE` :41 and `STAGING_SEED_ROUTE` :45 are answered ONLY by openxFactory's `scripts/ideation_dashboard/serve_openxfactory_lanes.py` — a THIRD column (§ 3.3). Stays `?`: none of Q1–Q5 rules on this file (Brett Heap, 2026-09-12, #656 comment 5642758731) |
| `views/lineage.js` | 140 | the stats strip and the cluster lineage / readiness-heat overlay | C | 10 governance literals; readiness rendered verbatim from cluster fields |
| `views/model.js` | 126 | the snapshot → funnel view-model | C | `COLUMN_KEYS = ["docs","clusters","possibles","staged","proposals","realized"]` :15 — 28 governance literals in 126 lines, the densest file in the tree |
| `views/notebook.js` | 109 | the "open in NotebookLM" tile action | A | `/capabilities` :12 and `/actions/notebook` :13, both openDox's `serve.py` |
| `views/outline-model.js` | 404 | the staged-topic outline model: sections, gaps, insertion | C | `REQUIRED_SECTIONS`, `QUESTION_SUBFIELDS`, `TEMPLATE_ORDER` — the section vocabulary of one domain's staging template, plus its `xspec:` marker grammar |
| `views/repo-selector-model.js` | 537 | the roster derivation over the snapshot index | A *(C tail)* | repository / ref / project nouns, which are openDox's — but `STATIONS` :517–522 pairs each schema key with a RENDERED label ("ideation documents", "topic clusters", "possibles", "staged topics", "OpenSpec changes") (§ 2.2 rule 3; parameterized in S7) |
| `views/repo-selector.js` | 889 | the header project picker, repo filter and refresh affordance | **SPLIT** | addresses all THREE columns from one file: `/project-register.json` :38 (openDox) · `/snapshot-index.json` :33 (openXdox) · `/actions/gate/create-project` :39 and `/actions/gate/edit-project` :43 (openXdox) · `/actions/apply-register-edits` :46 (openxFactory's lanes) · `/actions/refresh` :34 (both legs declare a handler). RULED Q3 (Brett Heap, 2026-09-12, #656 comment 5642758731): SPLIT — picker + refresh stay class A; `:39`/`:43` become a contributed binding at S4/S5; `:46` leaves the bundle entirely; not yet built |
| `views/settings.js` | 234 | the ⚙ panel and the theme/`localStorage` preference store | A | "PURE FRONTEND: no data path of any kind"; imports `wheel-model.js` only for `DRUM` geometry |
| `views/staging-workbench-model.js` | 1949 | the pure workbench scope derivation and its route table | **SPLIT** | pure derivation (class-A/C substance) carrying SIX class-B route constants :543, :817, :818, :821, :822, :826 (travel with the binding that calls them, never with the model — RULED Q3, Brett Heap, 2026-09-12, #656 comment 5642758731) plus `STATUS_BRAINSTORM` / `BRAINSTORM_AREA` / `STAGING_AREA` (class-C); not yet built — the six constants stay in-file until S4 |
| `views/staging-workbench.js` | 3315 | the full-screen workbench scoped to one topic-bearing tile | C | its scope is "a cluster, a possible, or a staged topic"; composes `doxbench-editor` + `doxbench-chat` + `bullseye` + `doc-wheel` |
| `views/swb-create.js` | 372 | the create-document dialog and its transport | **B** | `CREATE_ROUTE` = `/actions/gate/create-document` (`staging-workbench-model.js`:543); the module exists because the workbench view is pinned transport-free |
| `views/swb-model-intake.js` | 364 | the model-intake dialog and its transport | A | `/workbench/model-intake` and `/actions/workbench/model-intake` / `model-approval`, all answered by openDox's `serve_workbench.py` |
| `views/swb-session.js` | 614 | the three live branch-session verbs and their CLI descriptors | **B** | `FIRST_EDIT_ROUTE` / `ABANDON_SESSION_ROUTE` / `SHARE_SESSION_ROUTE` / `OPEN_PR_ROUTE`, all under the gate prefix |
| `views/viewer.js` | 403 | the read-only Markdown viewer over a source file | A *(the route moved to openDox at S6 — IN FLIGHT)* | pure render plus the vendored `markdown-it`; its content comes from `/source/` :314, which at the census tree `a99eba03` was declared by `openxdox/serve_projection.py`:57 — the one § 2.2 rule 1 breach the census carried. **RULED Q4** and being realized by slice S6: openXdox-code PR #17 (`00b69de7`) drops the two projection bindings and openDox-code PR #16 (`7dd0ba5a`) declares the fixed core arm — **both DRAFT and unlanded**, so this row is clean by the ruling and not yet by the tree (§ 3.3) |
| `views/wheel-model.js` | 1300 | the snapshot → wheel view-model, geometry and alignment | C | `WHEEL_KEYS` :25 and `WHEEL_LABELS` :27–34 — the six stage names, spelled twice |
| `views/wheel.js` | 1702 | THE WHEEL: the funnel-navigation deck | C *(B + openxFactory imports)* | imports `dispose.js` :73–74 (class B) and `intent-feed.js` :75–76 (absent, RULED openxFactory; discharged by S2, landed `#15` → openDox-code `main` `c7ab3d87` as `views/intent-binding.js`); `SOURCE_ROUTE` :97 — **RULED Q4**, openDox's own route once S6 lands (both legs DRAFT, § 3.3); :140–146 supplies the four verbs `dispose.js`:396 concatenates into a gate route (§ 1.2(c)) |

### 3.3 The third column the front end does not know about

`design.md` § D3 assigns THREE columns — openDox, openXdox, and **openxFactory's
own engineering adapter, which RULING DQ-1 keeps at openxFactory**. The web tier
reflects that, and nothing in it says so. Route ownership as landed was measured
at the three live heads; **amended 2026-09-12 (#2), the table below now shows the
RULED ownership, which the two in-flight pull requests under it are realizing**:

| owner | routes |
| --- | --- |
| **openDox** (`serve.py`, `serve_wire.py`, `serve_workbench.py`, `serve_project.py`) | `/snapshot.json` · `/capabilities` · `/project-register.json` · `/actions/edit` · `/actions/notebook` · `/actions/refresh` · `/workbench/model-catalog` · `/workbench/thread` · `/workbench/model-intake` · `/actions/workbench/chat-turn` · `/actions/workbench/document-abstract` · `/actions/workbench/model-intake` · `/actions/workbench/model-approval` · **`/source`** · **`/source/`** (prefix) — the two moved here by RULED Q4, as FIXED CORE ARMS, S6 IN FLIGHT |
| **openXdox** (contributed through `route_extension`) | `/actions/gate/` (POST prefix) · `/snapshot-index.json` · `/projections/evidence` · `/projections/workbench` · `/projections/role-authority` |
| **openxFactory's adapter** (`scripts/ideation_dashboard/serve_openxfactory_lanes.py`) | `/actions/apply-register-edits` · `/actions/dtn-seed` · `/actions/staging-seed` |

**Amended 2026-09-12 (#2) — `/source` and `/source/` changed owner.** As landed
(2026-09-11, at the three heads above) both sat in openXdox's row. **RULED Q4**
(Brett Heap, 2026-09-12, #656 comment `5642758731`): *"`/source/` is openDox's,
and openXdox's projection binding keeps only `/snapshot-index.json` and the three
`/projections/*` routes."* Slice S6 realizes it across both code legs, and at
this amendment **both pull requests are DRAFT and unlanded**:

| leg | pull request | head | what it does |
| --- | --- | --- | --- |
| openXdox-code | [#17](https://github.com/opensoft/openXdox-code/pull/17) DRAFT | `00b69de787975a663d9fb8985a6e38fc54945150` | `serve_projection.py` drops `SOURCE_PREFIX`, `BARE_SOURCE_ROUTE`, both `RouteBinding`s and the three handlers; `ProjectionRoutesExtension.routes()` becomes one binding, `/snapshot-index.json` |
| openDox-code | [#16](https://github.com/opensoft/openDox-code/pull/16) DRAFT | `7dd0ba5a07484a2fb2715d1de4e08e7c4b68be08` | `serve.py` declares the pair as two FIXED core arms — exact `/source` above prefix `/source/`, both above the § 2.4 contributed consult, so a contributed binding can no longer take the route back by arriving first |

**The three `/projections/*` routes were never declared in
`serve_projection.py`** — each travels with the surface that answers it — so
Q4 leaves all three where they are, exactly as it says. This table therefore
shows the RULED ownership; the TREE reaches it when #16 and #17 land, and
until then § 3.2's `views/viewer.js` and `views/wheel.js` rows are clean by the
ruling and not yet by the tree.

**What that means for § 4.5 assertion 2, stated here so the two are not read as
contradicting each other.** Assertion 2 greps in-scope files against "the § 3.3
ownership table", and its 18-site count still carries the four `/source/` sites
as openXdox breaches cleared at S6. That count is right: **a route is another
column's until that column stops declaring it**, so the assertion consumes the
ownership SNAPSHOT this table was measured against — the landed one, with
`/source` and `/source/` under openXdox — and takes the ruled table as its input
at the slice that REALIZES the ruling. openDox-code #16 does exactly that, in
the same pull request that moves the routes. § 4.5 assertion 2 carries the same
statement in full.

Two openDox view files address the third column: `views/lens.js` (:41, :45) and
`views/repo-selector.js` (:46). Under RULING DQ-1 those routes never move to a
descendant, so a front end that hardcodes them ships one repository's lanes to
every install. They are the front-end twin of the Python column that "never
leaves the repository it reads".

---

## 4. The mechanism

The Python side solved this three times and the front end can reuse all three
shapes rather than invent a fourth.

### 4.1 A view registry, mirroring `route_extension.collect_bindings`

`src/route_extension.py` already states the rule in its own words: *"A
contributed route is the profile; a second copy of the dispatch is the fork."*
`serve.build_server(route_extensions=…)` flattens a tuple of extensions into one
consult order and REFUSES a collision, a non-conforming object, and an exact
pattern declared under an already-claimed prefix (RULING A, 2026-09-07).

The front-end analogue, stated as a contract and not yet built:

- A **`ViewBinding`** — `{ id, region, mount(root, ctx), requires }` — is the
  front-end's `RouteBinding`. `region` names a mount point declared by the shell
  (`index.html`'s `view-*` sections and the two overlay roots are already
  exactly that); `requires` names the capability or profile facet the binding
  needs.
- A **`collectViewBindings(extensions)`** flattens contributed bindings into one
  order and refuses two bindings claiming one `region` + `id` slot — the same
  refusal, for the same reason: *"a declared route silently unreachable"* becomes
  *"a declared panel silently unmounted"*.
- `app.js` stops importing class-B modules directly. **There are TWO such
  imports, not one** (amended 2026-09-12 (#2) — as landed this bullet named only
  the first):
  - **:43**, `import { isGateBearing, mountGateBar } from "./views/gate.js"` —
    becomes a lookup in the collected bindings, and a shell built with no gate
    binding registered renders the tab strip **without** the gate bar rather
    than failing to load. *(Slice S3 has done exactly this: at
    `build/s3-view-registry` the import is gone and the shell resolves
    `gate.bar` by id — openXdox-spec `docs/gate-loop-view-contract.md` § 1 @
    `d73767b7`, measuring `app.js`:980 at `a497d715`.)*
  - **:45**, `import { firstEditTransport } from "./views/swb-session.js"`,
    called at `app.js`:1015 — both read at the census tree `a99eba03`; the same
    import is `app.js`:57 called at `:1134` at S3's `a497d715`, which is where
    the counterpart note found it (`docs/gate-loop-view-contract.md` § 8 Q10 @
    `d73767b7`). S3 did NOT remove it, because it is not a panel: a
    `ViewBinding` binds a panel at a REGION, and a transport is a function.

  **How the second one travels is OPEN, and this note does not decide it.** The
  counterpart's Q10 RECOMMENDS it travel as a DECLARED NON-MOUNT EXPORT of the
  workbench's contributed binding — its Q2's `exports` tuple, validated exactly
  as `entry` is — reached by `resolveView` at that one call site, with the
  doxBench Save falling back to a refusal-shaped transport when no gate column
  is registered; the alternative it names and argues against is a second,
  region-free extension point for contributed FUNCTIONS, which would be a second
  seam this section's whole argument is against. **That question is openXdox-spec's
  (§ 5.1) and is for Brett Heap.** What is settled here is only the
  MEASUREMENT: the shell has two class-A→class-B imports, S5 must carry both,
  and § 4.5 assertion 3 and § 5's S5 row now name both.

**FINDING, recorded 2026-09-12 (#2) — two declared regions that nothing hosts
and nothing reads.** The registry S3 built declares its mount points in two
mirrored tables, and `wheel-intent` and `dispose-intent` are declared in both —
`src/opendox/view_extension.py`:174–175 and
`src/opendox/web/views/view_extension.js`:80–81, both `"shell"`, at S3's
`a497d715` and still at its later head `e176947` — **and they appear nowhere
else in the bundle.** No host element declares one, no binding names one, and no
reader consults one. They were provisioned for slice S2's intent chips, and S2
landed differently: as `views/intent-binding.js` (openDox-code `#15` → `main`
`c7ab3d87`), with the chips rendering into a `span.intentchips` the dispose tray
creates — § 4.2's own account of why the chips were never going to be a
`ViewBinding` is the reason. **A contributed binding naming either region today
mounts into nothing, silently.** The counterpart's Q9 RECOMMENDS keeping both
declared and recording that they are unhosted and unread — *"declaring a region
costs nothing and refuses nothing; an undeclared one costs a slice"*, and S5 is
not the slice to retire S2's provision — and this paragraph is that record on
this side of the seam. **It is a RECOMMENDATION and it is OPEN**
(`docs/gate-loop-view-contract.md` § 8 Q9 @ `d73767b7`, for Brett Heap); the
census, the classes and the four assertions are unaffected either way, because a
region is not a file.

### 4.2 Reaching the consumer late, mirroring `consumer_reach`

`src/opendox/consumer_reach.py` is the ruled shape for the direction problem:
*"It makes a surviving reach LATE, NAMED and REFUSABLE instead of an import-time
dependency on the consumer"*, and `route_column()` is its forwarder for a class
that lives in the consumer.

The front end needs the identical thing in one place: **the class-B route table
must not be a literal in an openDox module.** A contributed binding brings its
own routes with it, so `GATE_DISPOSE_ROUTE` and its twelve siblings travel to the
binding that uses them, and an openDox module that still needs a gate verb asks
the VIEW REGISTRY (§ 4.1) and gets a refusal — naming the layering — when no
gate column is registered. This is the gate loop's own mechanism: it needs
§ 4.1's `collectViewBindings` to exist first, which is why the gate loop is
contributed at S5, after S3 builds the registry.

**`intent-feed.js` (§ 1.2(b)) reaches the same "late, named, refusable" shape a
slice earlier, at S2, without the view registry.** `dispose.js`'s tray mounts
per-tile — inside whichever view renders that tile, not at a region of its
own — and `wheel.js` already mounts at its own region (`index.html`'s
`view-wheel`). Either way the chips are a fragment inside an already-mounted
view, never a region needing a binding of their own: they were never going to
be a `ViewBinding` (§ 4.1 binds at the region grain — a whole tab or overlay —
not a fragment a view renders internally). S2 instead gives each importer a
small, local, late-and-refusable guard directly against the module's own
presence — an optional resolve in place of the import-time
`from "./intent-feed.js"` — present, the chips mount; absent, `dispose.js` and
`wheel.js` render without them. That guard is what turns § 1.2(b)'s dangling
import into a first-class, testable outcome (assertion 3), independently of —
and a slice before — § 4.1's registry.

### 4.3 Names from the profile, mirroring `domain_profile` + `profile_proxy`

RULING ASK-2's LAZY PROXY is already implemented at this leg:
`src/opendox/domain_profile.py` holds the ONE registration
(`register()` / `is_registered()` / `current()`,
`REGISTRATION_CALL = "opendox.domain_profile.register(<the host's profile>)"`),
`src/opendox/profile_proxy.py` is the accessor (`profile_openxfactory`, a
`_LateProfile` resolved at first attribute access), and `build_server()` reads
`ROUTE_EXTENSIONS` through it and **refuses when nothing is registered** — ASK-2's
"REFUSAL, NOT A DEFAULT". The runbook is
`openDox-code` `docs/profile-registration-runbook.md`.

Class C reads its names the same way, and the browser needs one extra hop
because the profile lives in the Python process:

1. The host registers its profile at process start, unchanged.
2. `serve.py` exposes the profile's **display facet** — the stage keys with
   their labels, the status vocabulary, the artifact-folder words — on the
   existing `/capabilities` payload (already fetched once at load by
   `views/notebook.js`'s `probeCapabilities`), so no new route and no second
   fetch.
3. `app.js` puts that facet in the context object every binding already receives.
4. A class-C module resolves **by ROLE, not by string** — the openXdox-spec
   note's own rule. `WHEEL_LABELS` becomes a lookup of the profile's ordered
   stage roles; `model.js`'s `COLUMN_KEYS` becomes the same list; `board.js`'s
   four columns become the profile's board roles; `docs.js`'s `AREA_ORDER`
   becomes the profile's declared source areas; `styles.css`'s four `--st-*`
   tokens become profile-keyed custom properties set on `:root` at boot.
5. **Refusal, not a default.** A class-C module with no profile registered
   renders its region empty with a named reason, exactly as `build_server()`
   refuses. A fallback to today's words is how the literals survive the refactor
   invisibly.

### 4.4 The vendor policy

`web/vendor/` holds one file and it is the whole policy: **vendored, MIT,
`html` disabled, no CDN, no external font, no remote script** — a boundary
openXdox-code's `tests/test_renderer.py::test_no_external_urls_anywhere_in_bundle`
already grep-proves over the bundle. The boundary work must NOT change it. The
one thing to state explicitly, because the census makes it possible to get wrong:
**`web/vendor/` belongs to class A and a contributed class-B binding may not add
to it.** A column that needs a library vendors it in its own leg and ships it
with its binding, or it does without; otherwise "no fork of the server" is
observed in Python and broken in JavaScript.

### 4.5 The test that holds the boundary

A census test, in the shape openDox-code's `tests/test_consumer_reach.py` and
openXdox-code's `tests/test_dependency_direction.py` already use — a SHAPE
assertion that parses the tree and imports nothing:

`openDox-code/tests/test_web_boundary.py`, four assertions.

1. **The census is complete, and `?` and `SPLIT` are BOTH TRANSITIONAL.**
   Every file under `src/opendox/web/` appears exactly once in a declared
   census (a small YAML or a table in the test), with a class. A new file
   with no row fails. This is the ratchet: it is what makes the boundary
   survive the next feature. **`?` and `SPLIT` are classes the census may
   carry only until S4, with one declared exception:** after S4 the assertion
   fails on any row still `?` OR still `SPLIT` — EXCEPT `views/lens.js`'s `?`,
   named here — the same idiom assertion 4 uses for its two schema-key
   exemptions (§ 2.2 rule 3) — because none of Q1–Q5 rules on its two
   openxFactory-lane routes (§ 6): it is out of scope for this ruling round,
   not undecided by omission, and it stays `?` until a future ruling names its
   destination. A `SPLIT` row carries no such exception: S4 is the slice that
   splits all three of them (§ 5), so a `SPLIT` row still standing after S4
   fails the assertion exactly like an undeclared `?` row would. A permanent
   UNDECLARED "undecided" is an escape hatch, not a boundary; a permanent
   DECLARED one, cited to the ruling gap that causes it, is how this census
   stays honest about what it does not yet know.
2. **No file OUTSIDE class B names a route another column declares** (§ 2.2
   rule 1, stated over OWNERSHIP and not over class B alone). Scope is every
   census row whose class is not B — class A, class C AND the transitional `?`,
   which is where most of the breaches actually sit and why the assertion cannot
   be scoped to A/C alone. Class B is exempt by construction: a gate-loop file
   naming a gate route is the boundary working. Grep each in-scope file against
   the § 3.3 ownership table: the gate prefix, openXdox's five projection
   routes, and openxFactory's three lane routes. Today it fails on **18 sites**:

   | owner | sites | where | cleared by |
   | --- | ---: | --- | --- |
   | gate prefix | 10 | `lens-model.js`:1036/:1037, `repo-selector.js`:39/:43, `staging-workbench-model.js`:543/:817/:818/:821/:822/:826 — all now RULED **SPLIT** rows (Q3, 2026-09-12, #656 comment 5642758731) | S4 |
   | openxFactory lanes | 1 | `repo-selector.js`:46 (RULED **SPLIT**, Q3 — leaves the bundle) | S4 |
   | openxFactory lanes | 2 | `lens.js`:41/:45 (the one true `?` row — ruled-later, none of Q1–Q5 rules on it) | future ruling |
   | openXdox projection | 1 | `repo-selector.js`:33 (`/snapshot-index.json`) — now a RULED **SPLIT** row (Q3) | S4 |
   | openXdox projection | 4 | `app.js`:183/:184, `viewer.js`:314, `wheel.js`:97 (`/source/`) — class A and class C | S6 |

   Fourteen of the eighteen sit in the three files the 2026-09-12 ruling
   named: twelve clear AT S4, now that they are RULED **SPLIT**
   (`lens-model.js`, `repo-selector.js`, `staging-workbench-model.js` — Q3);
   the other two are `lens.js`'s sites and do NOT clear at S4 — none of Q1–Q5
   rules on them, so they stand as the declared, ruled-later exception this
   assertion shares with assertion 1 (above), rather than clearing on any
   slice's schedule. The remaining four are the `/source/` sites Q4 rules on,
   cleared at S6.

   **`lens.js`'s two openxFactory-lane sites are this assertion's own
   standing, declared exception** — the same idiom assertion 4 uses for its
   two schema-key exemptions (§ 2.2 rule 3): named here, with the reason
   beside it, excluded from the in-scope grep until a future ruling folds
   `lens.js` back in. This is why S5's and S6's `xfail(strict=True)` removal
   still leaves the test green: the marker comes off because every OTHER site
   it was tolerating is fixed, not because `lens.js`'s two sites started
   passing the grep — they never entered it. A THIRD undeclared `?` or
   unresolved SPLIT row appearing later still fails immediately, the same
   ratchet assertion 1 enforces.

   The three gate constants declared in class-B files (`dispose.js`:28/:29,
   `gate.js`:120) are NOT in the count: they are exempt now and travel with
   the binding at S5. § 1.2(c)'s "13 gate route constants" measures the TREE;
   this row measures the ASSERTION, and the three in class-B files are the
   difference.

   **Amended 2026-09-12 (#2) — WHICH ownership table this assertion consumes.**
   § 3.3's table now shows the ownership RULED Q4 establishes, with `/source`
   and `/source/` under openDox; the 18-site table above still counts their four
   sites (`app.js`:183/:184, `viewer.js`:314, `wheel.js`:97) as openXdox
   breaches cleared at S6, and that is CORRECT and not a contradiction —
   **the assertion greps against the ownership the TREE has, never against the
   ownership a ruling has decided but no slice has yet realized.** A route is
   another column's until that column stops declaring it, and until
   openXdox-code #17 and openDox-code #16 land, `openxdox/serve_projection.py`
   still declares the pair. **The assertion's input is therefore the ownership
   SNAPSHOT this table was measured against — § 3.3's table as landed, with
   `/source` and `/source/` under openXdox — and the amended table becomes its
   input at the SLICE that realizes the ruling**, which is exactly what S6
   already does at the code: openDox-code #16 drops the two routes from
   assertion 2's owner pattern in the same pull request that moves them
   (`20 → 16` sites there, on that branch's own re-derived arithmetic).
   Implementing this assertion against § 3.3's RULED table before S6 lands would
   stop counting four live breaches and would take the `xfail(strict=True)`
   marker green for a defect that still stands, which is the exact rot
   `strict=True` exists to prevent. The site counts above are not restated here
   in either case: S4 is in flight and re-derives them.

   **Amended 2026-09-12 (#2) — what this assertion MEASURES WITH, and the one
   site that measurement cannot see.** The assertion's mechanism is stated above
   as *"grep each in-scope file against the § 3.3 ownership table"*, and a grep
   for a route literal cannot see `views/dispose.js`:396's
   `"/actions/gate/" + verb` (§ 1.2(c)). Three things follow, and only the first
   two are settled here. **(i)** The site is not in this row's count and never
   was — not because it is exempt, but because it was not visible to the
   instrument; `dispose.js` is class B and therefore out of scope anyway, so the
   arithmetic above is unaffected and is NOT restated (S4 is in flight and
   re-derives it). **(ii)** The gap is in the INSTRUMENT, not in this file: the
   moment a computed gate route appears in a class-A or class-C file, assertion 2
   passes it silently — so the assertion's implementation must grep for the
   PREFIX in a concatenation as well as for whole-route literals, and that is
   openDox-code's to build at the slice that owns the assertion. **(iii) OPEN —
   how a binding DECLARES a route it computes.** The counterpart's Q12
   RECOMMENDS the binding ENUMERATE the four as literals, on the argument that
   they are a closed set the caller already spells out and that enumerating them
   keeps a `routes:` declaration an ownership claim rather than a pattern
   language (the alternative — admitting a prefix on the DECLARING side — would
   let one binding claim a whole namespace). That is openXdox-spec's question
   and is for Brett Heap (`docs/gate-loop-view-contract.md` § 8 Q12 @
   `d73767b7`); this note records the site and the consequence and decides
   neither.
3. **Every relative import resolves**, and no class-A/C file imports a class-B
   module. This catches § 1.2(b) — `intent-feed.js` — as a test failure rather
   than a blank page, and it is the assertion that should have existed before the
   carve. **The shell breaches it TWICE, not once** (amended 2026-09-12 (#2)):
   `app.js` is class A and statically imports `views/gate.js` at :43 AND
   `views/swb-session.js` at :45 (`firstEditTransport`, called at :1015; the same
   import is :57 / :1134 at S3's `a497d715`, where the counterpart note found
   it — § 4.1). As landed this assertion's prose named only the first, through
   § 4.1's own single-line bullet; the ASSERTION ITSELF is unchanged and always
   covered both, because it is stated over the class pair and not over a line.
   **Both must be gone for this assertion to go green, so S5 carries both** —
   and HOW the second one travels is OPEN (the counterpart's Q10, § 4.1). This
   amendment does not restate the assertion's measured site count: slice S4 is
   in flight and re-derives it at its landing.
4. **No class-C file — and no declared class-A tail — carries a governance
   literal.** A closed word list (the registered profile's vocabulary, plus the
   eight controlled `Status:` words) grep-proven absent, mirroring
   openXdox-code's `tests/test_no_hardcoded_status_words.py`. Scope is the 14
   class-C files (2026-09-12: including `explorer.js`, RULED Q2), the three
   class-A tails of § 2.2 rule 3, and `styles.css`
   (its four `--st-*` token NAMES included). The two schema-key EXEMPTIONS —
   `composed-model.js`:107–110 and `doxbench-state.js`:37 — are carried in the
   test as a declared list with the reason beside each, never as silence: an
   undeclared exemption is how a literal survives a vocabulary sweep.

**How this lands without a red required check.** openDox-code's `validate` runs
an explicit file list with `--noconftest` (§ 1.2(d)), so a new test file is not
run until the workflow names it — and naming it while three of its four
assertions are known-red would put the required check red for the duration of
the arc. Slice S1 therefore lands the file, adds it to that list in the SAME
commit, and marks those three `@pytest.mark.xfail(strict=True)` with the defect
and this note cited in the reason. `strict=True` is the whole point: the check is
green while the defect stands, and goes RED the moment a slice fixes the defect
without removing the marker, so the measurement cannot rot into a permanently
tolerated failure. **Assertion 1 is unmarked from the start** — the census is complete the moment
it is written, and an unrowed new file must fail immediately or the ratchet does
not exist. **Assertions 2, 3 and 4 carry the marker at S1**, and each is unmarked
by the slice that discharges it: 3 by S2, 2 by S5 and S6, 4 by S7.

---

## 5. The slices

Ordered, each sized like the BUILD-arc slices already landing on this packet.
"Leg" names the repository whose pull request carries it.

| # | slice | files | seam | test | leg |
| --- | --- | --- | --- | --- | --- |
| **S1** | **Declare the census and measure the defect.** Land the census table of § 3.2 as data plus `tests/test_web_boundary.py` with all four assertions, add the file to `validate`'s explicit list in the SAME commit, and mark assertions 2, 3 and 4 `@pytest.mark.xfail(strict=True)` citing the defect each measures (§ 4.5). Assertion 1 is unmarked. No file moves, and the required check stays green. | +2 (census + test) + `validate.yml` | — | new | openDox-code |
| **S2** | **Resolve the `intent-feed` edge (§ 6 Q5).** **RULED** — keep the manifest row, fix the importers (Brett Heap, 2026-09-12, #656 comment 5642758731): S2 makes the intent chips an OPTIONAL contributed binding; absent, the wheel and the dispose tray render without them. S2 is the slice that makes `app.js`'s module graph resolve again. Its guard is independent of § 4.1's view registry — not yet built at this point in the landing order — per § 4.2's own account of the two mechanisms. | `dispose.js`, `wheel.js`, `styles.css`:1278–1295 | § 4.2 | assertion 3 green | openDox-code |
| **S3** | **The view registry.** `ViewBinding` + `collectViewBindings` + the shell's declared regions; `app.js`'s direct class-B imports become registry lookups; no VIEW is contributed to THIS registry yet — S2's intent-feed guard (§ 4.2) is a narrower, region-free mechanism outside it — so the shell renders exactly as today with an empty extension tuple. | `app.js`, new `views/view_extension.js`, `index.html` | § 4.1 | collision + empty-tuple refusal tests | openDox-code |
| **S4** | **Split the three RULED `SPLIT` files.** — the PRECONDITION for S5, not its sequel. Only 3 of the 13 gate-route constants are declared in class-B files (`dispose.js`:28/:29, `gate.js`:120); the other 10 are declared in `lens-model.js`, `repo-selector.js` and `staging-workbench-model.js`, and both `swb-create.js` and `swb-session.js` IMPORT theirs from the last of those. The gate loop cannot be contributed until its route table stops living outside class B. Each tail to its class per § 6's Q3 ruling: `lens-model.js`'s two routes, `repo-selector.js`'s five cross-column routes, `staging-workbench-model.js`'s six. **RULED Q3** (Brett Heap, 2026-09-12, #656 comment 5642758731) — `explorer.js` needs no split here: Q2 already resolved it wholly to class C (§ 3.2). `lens.js` is OUT OF SCOPE: none of Q1–Q5 rules on its two openxFactory-lane routes, so it stays `?` as assertion 1's one declared, ruled-later exception, and those two sites stand as assertion 2's own declared exception (§ 4.5) — not a temporary `xfail` — until a later ruling resolves `lens.js`. | 3 files | § 4.2 | assertion 2 green for the twelve SPLIT-file sites (not `lens.js`'s two openxFactory-lane sites) | openDox-code |
| **S5** | **Contribute the gate loop.** The four class-B files and all 13 route constants — now all declared in class-B files — move behind a binding openXdox supplies; a student install comes up with no gate bar, no dispose tray, no session verbs, and no 404. **Amended 2026-09-12 (#2): S5 carries BOTH of the shell's class-A→class-B imports, not one** — `app.js`:43 (`gate.js`, already discharged by S3's registry) AND `app.js`:45 (`firstEditTransport` from `swb-session.js`, called at :1015; :57 / :1134 at S3's `a497d715`) — and how the SECOND travels is OPEN, the counterpart's Q10 recommending a declared non-mount export (§ 4.1). Also S5's: the computed gate route `dispose.js`:396 must arrive DECLARED (§ 1.2(c); the counterpart's Q12 recommends four literals — open). **Needs an openXdox-spec counterpart, which now EXISTS** (§ 5.1). | `dispose.js`, `gate.js`, `swb-create.js`, `swb-session.js` | § 4.1 + § 4.2 | assertion 2 green outright; assertion 3 green on BOTH shell imports | openXdox-code (binding) + openDox-code (removal) |
| **S6** | **Re-home `/source/` per Q4** — the slice that discharges the census's one § 2.2 rule 1 breach. `openxdox/serve_projection.py` drops the `BARE_SOURCE_ROUTE` and `SOURCE_PREFIX` bindings (:57, :61, :375–384) and keeps `/snapshot-index.json` and the three `/projections/*` routes; openDox's `serve.py` declares the read-only pass-through as its own fixed core arm. `views/viewer.js` and `views/wheel.js`:97 become clean. **RULED Q4** (Brett Heap, 2026-09-12, #656 comment 5642758731). **IN FLIGHT (2026-09-12, #2):** openXdox-code [#17](https://github.com/opensoft/openXdox-code/pull/17) `00b69de7` (DRAFT) drops the bindings and openDox-code [#16](https://github.com/opensoft/openDox-code/pull/16) `7dd0ba5a` (DRAFT) declares the fixed core arm; § 3.3 carries the amended ownership table. | `serve_projection.py`, `serve.py` (+ their tests) | § 4.1 | assertion 2 green for `viewer.js` | openXdox-code + openDox-code |
| **S7** | **Parameterize class C.** The display facet on `/capabilities`, the context hop, and the vocabulary by ROLE across the 14 class-C files (2026-09-12: including `explorer.js`'s five governance literals, RULED Q2) PLUS the three declared class-A tails (`docs.js`:18, `grouping.js`:34–41/:51–52, `repo-selector-model.js`:517–522) — `wheel-model.js` and `model.js` first (they are the vocabulary the others import), `styles.css`'s four `--st-*` tokens last. Carries the § 1.1 packet-figure amendment. | 17 files + `serve.py` | § 4.3 | assertion 4 green; both exemptions declared | openDox-code (+ openxFactory for the packet row) |
| **S8** | **Re-home the 48 test files and un-narrow `validate`.** The 23 at openXdox-code pointing at an absent `web/` go to the leg the census says owns each bundle file; the narrowings (RULED Q-L5 (b′) / Q-L8 (b′)) lift for the web suites. All three `xfail(strict=True)` markers from S1 are already gone by S7 — 3 at S2, 2 at S5 and S6, 4 at S7 — so S8 starts from four unmarked assertions and carries none of its own; `lens.js`'s standing exceptions under assertions 1 and 2 (§ 4.5) are declared, not marked, and are not this slice's — or any slice's — to close, only a future ruling's. **BLOCKED on a ruling (2026-09-12, #2): § 6's Q6.** Re-homing a test file that ARRIVED at the wrong leg moves its carve-manifest row's `destination` / `destination_path`, and no form in the floor expresses that — S6 met the same wall on one file and withdrew rather than work round it. | 48 test files | — | both legs' `validate` | both |

**RULED, same sitting → S1–S3 START NOW** (Brett Heap, 2026-09-12, #656 comment
5642758731): none of the three needed a ruling to begin — S1 and S3 never did,
and S2's Q5 is RULED above. S4, S5 and S6 above are marked RULED and follow once
S1–S3 land. **Q-L1 binds every slice:** an edit to an ARRIVED file (a
`moved_verbatim` / `moved_with_declared_edit` row of
`docs/opendox-carve-manifest.yaml`) outside its declared lines is an undeclared
movement, so any slice that edits such a file pairs its leg PR with an
openxFactory row-annotation PR (the ASK-7 pattern) that lands FIRST; new files
are created, not arrived. Landing order among S1–S3: S1 → S2 → S3, the lane
merging main into each before landing.

### 5.1 The openXdox-spec counterpart this note does NOT author

**S5 needs one, and it is not written here.** The gate-loop column's VIEW
CONTRACT — what a contributed `ViewBinding` may assume about the shell (mount
points, the context object's shape, the capability probe's payload, the refusal
text when a binding's `requires` is unmet) — is a requirement ON openXdox, and by
the same reasoning that put the domain-profile note at openXdox-spec it belongs
at `opensoft/openXdox-spec` `docs/`. This note names the obligation and stops.
Everything S1–S4 needs is here.

**Amended 2026-09-12 (#2) — the counterpart EXISTS, and this note still does not
author it.** It landed as `opensoft/openXdox-spec`
[`docs/gate-loop-view-contract.md`](https://github.com/opensoft/openXdox-spec/blob/d73767b7/docs/gate-loop-view-contract.md)
→ `d73767b7`, `Status: draft`, titled *"The Gate Loop's View Contract
(openDox-spec § 5.1)"* and declaring this section verbatim as its obligation.
It measures the shell as slice S3 actually leaves it (openDox-code PR #14,
`a497d715`, OPEN at the time of writing and since moved to `e176947`), and it
records three things S5 needs that S3 did NOT deliver: nothing generically
mounts a contributed binding, nothing publishes the server-side view manifest,
and nothing READS `requires`.

**Its § 8 carries TWELVE open questions for Brett Heap, and they are S5's
precondition list.** None is written there as decided; each carries a RECOMMENDED
answer:

**Its numbering is its own** — the counterpart's Q1–Q12 are NOT this note's
Q1–Q6, and a citation must name the document:

| counterpart § 8 | what it asks |
| --- | --- |
| Q1 | does the shell MOUNT contributed bindings, or must every one have a named reader? |
| Q2 | is a binding's contract its `entry`, or its whole module namespace? |
| Q3 | what is a contributed binding's mount SIGNATURE? |
| Q4 | what may `requires` name, and what does the shell DO when it is unmet? |
| Q5 | where do a contributed module's BYTES come from? |
| Q6 | what may a contributed module IMPORT from the bundle? |
| Q7 | where does a contributed binding's CSS live? |
| Q8 | is a page-level host (`dispose.js`'s `document.body` refusal panel) inside the contract? |
| Q9 | do the two declared-but-unhosted `shell` regions stand? (§ 4.1's finding) |
| Q10 | how does the shell's remaining class-A→class-B import travel? (§ 4.1, § 4.5 assertion 3) |
| Q11 | what does a human see when the registry refuses? |
| Q12 | how does a binding declare a route it COMPUTES? (§ 1.2(c), § 4.5 assertion 2) |

Three of them are the open points amendment #2 carries above — its Q9 (§ 4.1's
unhosted-regions finding), its Q10 (§ 4.1 and § 4.5 assertion 3) and its Q12
(§ 1.2(c) and § 4.5 assertion 2) — and a fourth, its Q5, asks where a contributed
module's BYTES come from, which is the one thing § 4.4's vendor policy does not
reach. **They are openXdox-spec's
to hold and Brett Heap's to rule; nothing here pre-empts any of them.** S5 does
not start until they are settled, which is what "precondition, not sequel" means
on that side of the seam exactly as it does for S4 on this one.

---

## 6. Open questions for Brett Heap

Five as landed, each principle-level, each with a RECOMMENDED answer. The census
in § 3.2 is written to the recommendation and is redrawn on any other ruling.
**All five are RULED** (Brett Heap, 2026-09-12, #656 comment `5642758731`), and
each ruling is recorded under its question below.

**Amended 2026-09-12 (#2): a SIXTH, Q6, is added and is OPEN.** It was not
foreseeable when the five were written — it is a constraint slice S6 discovered
by hitting it — and it blocks slice S8 rather than S1–S6. It is written in the
same shape as the first five: the question, the constraint measured, a
RECOMMENDED answer with its argument, and the alternative rejected on the
record. **It is not decided here.**

**Q1 — Is the docs tile openDox's document list, or openxFactory's corpus
browser?** `views/docs.js` (189 lines) carries zero governance literals, which
reads as clean class A — but `AREA_ORDER` at :18 hardcodes `ideation/brainstorm`
and `ideation/staging`, which is openxFactory's own corpus layout, and
`views/doc-wheel.js` (491 lines) is the same tile's wheel. § 3.4's task text says
"docs tile … are openDox".
**RECOMMENDED: openDox, class A, with the area map parameterized.** The tile
lists documents; it is the FOLDER NAMES that are one domain's, and the profile
already has to carry an artifact-vocabulary axis for `outline-model.js`. Making
the tile itself openXdox would take the doc list away from the student, which is
the outcome § 3.4 exists to prevent.

**RULED — the recommended answer adopted: openDox, class A, with the area map
parameterized.** Brett Heap, 2026-09-12, #656 comment 5642758731, by
interactive multi-choice.

**Q2 — Is `views/explorer.js` the "drill-in" § 3.4 assigns to the gate loop?**
The task text says *"the gate console and drill-in are the gate loop"*. Two
things in the tree answer to "drill-in": `explorer.js` (279 lines, the drill-DOWN
explorer that opens a staged/proposal/realized tile as its artifact folder, pure
snapshot projection, no verb, no route) and the repository-lens DRILL-IN banner
(`index.html`'s `drillbanner`, D21, rendered by `views/repo-selector.js`).
**RECOMMENDED: neither is class B.** `explorer.js` is class C — it is a
projection whose only domain content is the artifact-folder vocabulary — and the
drill banner follows `repo-selector.js`'s own ruling (Q3 below). What § 3.4
means by "drill-in" is the gate console's own drill-in, which at this tree is the
dispose tray's refusal panel inside `dispose.js`, already class B.

**RULED — the recommended answer adopted: neither `explorer.js` nor the drill
banner is class B; `explorer.js` is class C.** Brett Heap, 2026-09-12, #656
comment 5642758731, by interactive multi-choice.

**Q3 — Does `views/repo-selector.js` split, or move whole?** One 889-line file
addresses all three columns (§ 3.2's row). Splitting it is real work; moving it
whole puts the project picker — the student's way to choose what they are
working on — behind the gate column.
**RECOMMENDED: split.** The picker and the refresh affordance are class A; the
two `/actions/gate/*` project commissions become a contributed binding with S4;
`/actions/apply-register-edits` is openxFactory's lane and leaves the bundle
entirely. The same ruling governs `staging-workbench-model.js`'s six route
constants and `lens-model.js`'s two: **a route constant travels with the binding
that calls it, never with the model that happens to declare it.**

**RULED — the recommended answer adopted: split.** Brett Heap, 2026-09-12,
#656 comment 5642758731, by interactive multi-choice.

**Q4 — `/source/` is openXdox's. Can a student read a document?** The read-only
Markdown viewer (`views/viewer.js`, class A) fetches document CONTENT from
`/source/`, which `openxdox/serve_projection.py`:57 declares. Under RULING OQ-2 a
student runs openDox alone, so today they would get a viewer that cannot load a
file.
**RECOMMENDED: `/source/` is openDox's, and openXdox's projection binding keeps
only `/snapshot-index.json` and the three `/projections/*` routes.** Reading a
file out of the pinned checkout is the neutral product's own read-only
pass-through; it predates the gate loop and nothing about it is a gate act.
This is a route-ownership correction at § 4.3 of the packet, not a new
capability, and it is slice **S6** — the recommendation is not left without an
owner: `openxdox/serve_projection.py` drops two bindings, openDox's `serve.py`
declares one fixed core arm, and both legs' tests move with them.

**RULED — the recommended answer adopted: `/source/` is openDox's.** Brett
Heap, 2026-09-12, #656 comment 5642758731, by interactive multi-choice.

**Q5 — `views/intent-feed.js` is RULED `not_moved` and two openDox files import
it.** The manifest row (`docs/opendox-carve-manifest.yaml`:1807–1810, RULED OQ-F)
says the committed-intent feed is RULING Q1's apply lane made visible and its
only reader is `serve_openxfactory_lanes.py`:412 — but `dispose.js`:26 and
`wheel.js`:75–76 are readers too, at a leg where the file does not exist.
**RECOMMENDED: keep the ruling, fix the importers.** The intent chips are one
domain's lane made visible, so the module is rightly openxFactory's; what is
wrong is that two class-B/C files import it unconditionally. S2 makes the chips
an OPTIONAL contributed binding — absent, the wheel and the tray render without
them — which is the same answer `build_server()` gives for an unregistered
profile. The alternative (re-point the manifest row to `opendox_code`) ships
openxFactory's lane to every install and contradicts OQ-F.

**RULED — the recommended answer adopted: keep the ruling, fix the
importers.** Brett Heap, 2026-09-12, #656 comment 5642758731, by interactive
multi-choice.

**Q6 — slice S8 needs a manifest RE-DESTINATION form, and the floor has none.**
*Added by amendment #2, 2026-09-12 (#656 comment `5647678655`). OPEN.*

§ 1.2(d) measured the defect S8 exists to repair: 23 test files at
`openXdox-code` name a `views/<name>.js` path and resolve it under
`REPO_ROOT / "src" / "openxdox" / "web"`, **a directory openXdox-code does not
have** — *"the carve's `import rewrites` edit class rewrote the path constant and
pointed the tests at the wrong leg."* § 5's S8 row says those files *"go to the
leg the census says owns each bundle file"*. **That sentence is a change of
DESTINATION on an already-arrived row, and nothing in the four-part floor can
express it.**

**The constraint, measured at `opensoft/openxFactory`
`177ba8196e16097e30aeb3f946ca8291b9ba4e92` on 2026-09-12** (every `:n` below is a
line of `docs/opendox-carve-manifest.yaml` at blob `e6c3925a`, or of
`docs/opendox-cutover-runbook.md` at blob `ef1d439b`, where it is named). A
row in `docs/opendox-carve-manifest.yaml` places a file with two fields —
`destination`, a key CLOSED to the five of `destinations:` (:188–197), and
`destination_path` — and declares what may DIFFER at that destination with
`edits: [{class, lines[]}]`, whose `edit_classes` are CLOSED at three by RULING
OQ-1 (:199–200, and the row grammar at :47–56). **An `edits[]` entry is a claim
about BYTES ON A LINE, never about placement** — the manifest says so in its own
amendment records, three times: *"a declared line is a claim about what may
differ AT THE DESTINATION"* (:279–280, :299–302, :320–322). So Q-L1's
declared-edit window — the mechanism § 5 binds every slice to, and the one every
slice from S2 onward has used — **cannot carry a re-destination at all.** It is
not a matter of finding the right class; there is no field.

The arrival verifier then refuses from both ends, with two codes a declared edit
cannot silence (`docs/opendox-cutover-runbook.md` § 2.1): at the LOSING leg the
row's `destination_path` has no file, which is **`arrival-missing`**; at the
GAINING leg the file sits under a declared root that no row places and no
admission rule admits, which is **`arrival-undeclared-file`**.

**Slice S6 met this exact wall and withdrew rather than work round it.** Moving
`/source` to openDox made `tests/test_source_dot_directories.py` an openDox test,
but its row —
`tests/ideation-dashboard/test_source_dot_directories.py`,
`moved_with_declared_edit`, `destination: openxdox_code`, `destination_path:
tests/test_source_dot_directories.py` (:3394–3405) — names the other leg. S6 put
the file back at openXdox-code `657c821b`, *"Q-L1 floor: keep
test_source_dot_directories.py here — its row names this leg"*. **One file
stopped one slice. S8 is forty-eight.**

**RECOMMENDED: a new DECLARED ACT — a `re_destined:` field on a moved row, gated
by the same two tools — and NOT a re-cut.**

The shape, argued rather than asserted. A moved row gains an OPTIONAL
`re_destined: {from, from_path, to, to_path, ruling, note}`, with `to` held to
the same CLOSED `destinations:` keys. **Nothing about the carve moves**: the row
keeps its `disposition`, its `sha256` and the `carve_commit` those are claims
about, because a digest is a claim about the SOURCE blob at `b075fd91…` and
where the file now lives says nothing about it.
`scripts/validate-carve-manifest.py` holds `to` to the destination keys, refuses
`re_destined` on a `not_moved` row (there is no arrival to re-place) and refuses
a chain (a row already re-destined is AMENDED in place, never re-destined twice,
so one row never needs two readings).
`scripts/verify-carve-arrival.py` reads the EFFECTIVE destination —
`re_destined.to` / `to_path` when present, else `destination` /
`destination_path` — and both refusals then answer correctly: the losing leg no
longer expects the file, and the gaining leg admits it BY NAME rather than by a
coincidence of bytes. `edits[].lines` stay bound to the source blob at
`carve_commit` and are untouched; an import rewrite that changes `openxdox.X` to
`opendox.X` at the new leg is an ORDINARY Q-L1 declared line under the existing
`import rewrites` class, so `edit_classes` stays closed at three.

**This is a grammar extension of exactly the kind already ruled once.** RULED
Q-L7 (a) (Brett Heap, 2026-09-10, #656 comment `5618683833`) added
`also_replicated_to:` to a moved row and `edits:` to a replica row — two FIELDS
that spell two facts the row grammar could not hold — *"neither of them a fourth
disposition and neither of them a placement"* (:87–119). `re_destined:` is the
third such field and the first that IS about placement, which is precisely why it
needs a ruling and cannot be assumed from that precedent.

**The alternative is a one-time RE-CUT, and it is measurably foreclosed.**
§ 11 of the runbook re-cuts at a NEW `carve_commit` with every digest
RECOMPUTED, and its step 4 re-emits the manifest *"at that commit, as the last
thing on that tree"*. The manifest is now `phase: post-shed` (:171; the § 5.2
shed landed at openxFactory `main` as `cc4ae9d3`, PR #940, 2026-09-11), which
means the 319 moved and deleted source paths are EXPECTED ABSENT at the source
and the validator CHECKS that absence (:157–164). Measured 2026-09-12 against
`177ba819`: `scripts/ideation_dashboard/serve.py` and
`tests/ideation-dashboard/test_source_dot_directories.py` are both gone, while
the replicated `scripts/route_extension.py` is present. **A manifest re-emitted
at a post-shed commit would carry no moved rows at all** — it would be a
different document, not a re-cut. Three further costs stand even if that were
solved: re-cutting is Brett Heap's own act (§ 12, act 5); § 11 step 6 re-verifies
EVERY already-arrived leg, because *"a leg whose arrival was proved against a
superseded referent is proved against nothing"*; and § 11's trigger is a
SOURCE-SIDE fact — *"if `main` moves under the carve"*, with the digests wrong.
S8's fact is destination-side and is a correction to a RULED placement: RULED
OQ-G's TEST HOMES rule (:69–76) placed 70 files at openXdox by a rule about
imports, and § 1.2(d) measured that 23 of them landed where nothing can run them.
**Correcting a ruled placement is a new ruling, and a new ruling is DECLARED, not
re-cut.** It also keeps the floor's own sentence true — *"a file in no row, or an
edit in no class, is an UNDECLARED MOVEMENT and the carve REFUSES"* (:5–6) —
because a re-homed file never leaves its row.

**What is unchanged either way, and should be stated so the ruling is not read
wider than it is:** `carve_commit`, `carve_tag`, all 318 `sha256` values, the
456 rows, the three `edit_classes`, the four `not_moved_reasons`, the five
`destinations:` keys, and the disposition list, which stays three. And the ASK-7
pairing is unchanged: S8's leg pull requests pair with ONE openxFactory
row-amendment pull request that lands FIRST, exactly as § 5 requires of every
slice.

**The scope question inside Q6, also open, with the same recommendation:**
whether `re_destined:` may be used for anything other than a RULED mis-placement
— for instance to re-home a file for convenience after both legs are green.
**RECOMMENDED: no.** Require a `ruling:` field naming the comment that ordered
it, validated present, so the form cannot become a quiet way to move a file
after the carve is closed.

---

## 7. The amendment record

What has changed in this note since it landed, in the shape the counterpart's
§ 9 uses: which amendment, when, what moved, and the claim that authorized it.
**Nothing is deleted by an amendment**; a superseded statement is marked in place
with what it said as landed, so a reader who cites this note from an older
revision can see what moved under them.

**Landed** — `a44ac06d` (openDox-spec [#8](https://github.com/opensoft/openDox-spec/pull/8)),
merged 2026-09-12T01:56Z. The census, the three classes, the mechanism, the eight
slices and five open questions. Measured on 2026-09-11 at openDox-code `main`
`a99eba03` and openXdox-code `main` `af15f712`.

**Amendment #1** — `61866d29` (openDox-spec [#9](https://github.com/opensoft/openDox-spec/pull/9)),
merged 2026-09-12T03:36Z. Carried the five rulings. Brett Heap RULED Q1–Q5 by interactive
multi-choice, every recommended answer adopted (`opensoft/openxFactory#656`
comment `5642758731`). § 6's five questions each closed with their ruling; § 3.1
re-bucketed (`explorer.js` `?` → C in full; three files RULED **SPLIT**;
`lens.js` alone left `?`); § 5 marked S2/S4/S6 RULED and S1–S3 START NOW, and
stated that Q-L1 binds every slice. `Status: draft` kept.

**Amendment #2** — this revision, 2026-09-12. Claim:
`opensoft/openxFactory#656` comment `5647678655`, lane
`openxfactory-4-opendox-extraction`. Five corrections and one new open question.
`Status: draft` kept, and the § 3 census TOTALS are deliberately NOT restated —
slice S4 is in flight and re-derives them at its landing.

| # | section(s) | what changed |
| --- | --- | --- |
| (a) | § 2.2 rule 1 · § 3.2 (`views/viewer.js`, `views/wheel.js`) · § 3.3 · § 5 (S6) | `/source` and `/source/` move from openXdox's row to openDox's per **RULED Q4**, as fixed core arms. Realized by slice S6, **IN FLIGHT**: openXdox-code [#17](https://github.com/opensoft/openXdox-code/pull/17) `00b69de7` drops the bindings, openDox-code [#16](https://github.com/opensoft/openDox-code/pull/16) `7dd0ba5a` declares the arms — both DRAFT. The ownership table shows the RULED state; the tree reaches it when both land |
| (b) | § 3.2 (`app.js`) · § 4.1 · § 4.5 assertion 3 · § 5 (S5) | the shell has **TWO** class-A→class-B imports, not one. As landed, § 4.1 and the `app.js` census row named only `app.js`:43 (`gate.js`). The second is `app.js`:45, `firstEditTransport` from `views/swb-session.js`, called at :1015 — measured at the census tree `a99eba03`; the counterpart note found it at S3's `a497d715` as :57 / :1134. **How it travels is OPEN** (the counterpart's Q10 recommends a declared non-mount export) |
| (c) | § 1.2(c) · § 2.2 rule 1 · § 3.2 (`views/dispose.js`, `views/wheel.js`) · § 4.5 assertion 2 | a FOURTEENTH gate-route site, which is not a constant: `views/dispose.js`:396 posts to `"/actions/gate/" + verb`, four verbs from `views/wheel.js`:140–146 (both at `a99eba03`). A route-literal grep cannot see it, which is a gap in assertion 2's INSTRUMENT. **How a binding declares a computed route is OPEN** (the counterpart's Q12 recommends enumerating the four as literals) |
| (d) | § 1.2(b) · § 4.1 | FINDING: the registry declares two `"shell"` regions, `wheel-intent` and `dispose-intent` (`view_extension.py`:174–175, `views/view_extension.js`:80–81, at S3's `a497d715` and still at `e176947`), which **no host element and no reader uses** — S2 landed instead as `views/intent-binding.js` (openDox-code `#15` → `main` `c7ab3d87`). A binding naming either mounts into nothing, silently. **OPEN** (the counterpart's Q9 recommends keeping both declared and recording that they are unhosted) |
| (e) | § 5.1 | the counterpart this note deliberately does not author now EXISTS: openXdox-spec `docs/gate-loop-view-contract.md` → `d73767b7`, with **twelve** open questions for Brett Heap listed there as S5's precondition list. The sentence that this note names the obligation and stops is kept |
| (f) | § 6 (**Q6**) · § 5 (S8) | a sixth open question: **S8 needs a manifest RE-DESTINATION form.** Re-homing the 48 test files moves rows' `destination` / `destination_path`, which Q-L1's `edits: [{class, lines[]}]` grammar cannot express — S6 met it on one file and withdrew (openXdox-code `657c821b`). Asked with a RECOMMENDED answer (a `re_destined:` row amendment gated by the same verifier, over a one-time re-cut) and **left OPEN for Brett Heap** |
| fix round | § 3.3 · § 4.5 assertion 2 · the measurement-heads block · § 6 Q6 | **two review findings taken on openDox-spec #10**, both accurate: (1) § 3.3's amended table and assertion 2's 18-site count read as contradicting each other, so both now state that the assertion consumes the ownership SNAPSHOT the tree has and takes the ruled table at the slice that realizes it; (2) the openxFactory citations named only `main`, which moves — now pinned to `177ba819` with both blob shas |
| (g) | header · the opening blockquote · the measurement-heads block · § 7 · `README.md` | this record; the `Amended:` line; the blockquote's note that Q6 gates the LAST slice rather than the first; the statement of WHICH shas amendment #2 read, so a citation added by it is never mistaken for a census measurement; and the README documentation-index row, which read "the five questions (RULED …)" and now reads six — Q1–Q5 ruled, Q6 open — on the precedent of amendment #1, which updated the same row |

**Measurement discipline across amendments.** The census tree is
`a99eba03` and amendment #2 did not re-measure it. Every citation amendment #2
adds is marked with the sha it was read at, because the shell has moved twice
since the note landed — slice S2 to openDox-code `main` `c7ab3d87` and slice S3
on `build/s3-view-registry` (`a497d715`, later `e176947`, PR #14 OPEN) — and a
line number carried across a head is a false citation. Where a fact is true at
both the census tree and a later head, both are named.

**Open points this note is carrying, collected.** Three of amendment #2's five
corrections end in a question that is NOT this note's to answer, and all three
belong to the openXdox-spec counterpart's § 8: Q10 (how the second shell import
travels), Q12 (how a computed route is declared) and Q9 (whether the two
unhosted regions stand). A fourth, **Q6**, is this note's own and is in § 6.
None of the four is written anywhere above as decided.
