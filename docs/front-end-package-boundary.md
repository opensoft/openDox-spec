# The Front-End Package Boundary openDox Has To Invent

Status: draft
Amended: 2026-09-12 — the five open questions RULED (#656 comment 5642758731)
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
> the questions a ruling must settle before the first slice starts.

**Everything measured here was read live on 2026-09-11 at these heads:**
`opensoft/openDox-code` `main` `a99eba03e31a0aee1cc15a061fdf718cc88a2c44`,
`opensoft/openXdox-code` `main` `af15f71207797214ffd6340267b5cb2ecb40bf6a`,
`opensoft/openxFactory` `main`. Every path in the census was verified present at
that openDox-code head; every line number was read at it.

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
absent module's chips.

**(c) Thirteen route constants in five openDox view files address a prefix
openXdox owns.** `openxdox/serve_gate.py`:55 declares
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

`views/viewer.js` and `views/wheel.js`:97 address `/source/`, and
`views/repo-selector.js`:33 addresses `/snapshot-index.json` — both declared by
`openxdox/serve_projection.py` (`SOURCE_PREFIX`:57, `SNAPSHOT_INDEX_ROUTE`:56),
so **the read-only document viewer, the most obviously student-usable surface in
the tree, cannot render a document without the consumer layer serving the
route.**

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
   route under `serve_gate.ACTIONS_GATE_PREFIX` (class-B, 13 constants),
   openXdox's PROJECTION routes (`/snapshot-index.json`, `/source`, `/source/`,
   the three `/projections/*`), and openxFactory's adapter lanes
   (`/actions/dtn-seed`, `/actions/staging-seed`,
   `/actions/apply-register-edits`) — the last of which no class can ever own,
   because RULING DQ-1 keeps that column at openxFactory. That is what makes
   § 1.2(c) and § 3.3 defects rather than layout choices. `views/viewer.js` is
   the one census row that breaks the rule while staying class A, and it breaks
   it on a PROJECTION route, not a gate one: § 6's Q4 is the ruling that
   discharges it — by moving the route, not the file (slice S6).
2. **A class-C file may not carry a governance word as a literal.** That is
   RULING C2, and it is why class C is a class rather than a footnote on class A:
   11,575 lines sit in it.
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
| `app.js` | 1155 | the shell: the ONE snapshot fetch, the tab strip wiring, the seam bundle, cross-view navigation | A | imports 20 view modules; its only class-B import is `gate.js` at :43 (`isGateBearing`, `mountGateBar`) |
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
| `views/dispose.js` | 427 | the gate dispose tray and its refusal panel | **B** | `GATE_DISPOSE_ROUTE` :28 and `GATE_PROPOSE_ROUTE` :29 both sit under `serve_gate.ACTIONS_GATE_PREFIX`; mounts on `actions.gate` capability |
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
| `views/viewer.js` | 403 | the read-only Markdown viewer over a source file | A *(B-owned route, discharged by S6)* | pure render plus the vendored `markdown-it`; but its content comes from `/source/`, declared by `openxdox/serve_projection.py`:57 — the one § 2.2 rule 1 breach the census carries, ruled by Q4 and moved by slice S6 |
| `views/wheel-model.js` | 1300 | the snapshot → wheel view-model, geometry and alignment | C | `WHEEL_KEYS` :25 and `WHEEL_LABELS` :27–34 — the six stage names, spelled twice |
| `views/wheel.js` | 1702 | THE WHEEL: the funnel-navigation deck | C *(B + openxFactory imports)* | imports `dispose.js` :73–74 (class B) and `intent-feed.js` :75–76 (absent, RULED openxFactory); `SOURCE_ROUTE` :97 |

### 3.3 The third column the front end does not know about

`design.md` § D3 assigns THREE columns — openDox, openXdox, and **openxFactory's
own engineering adapter, which RULING DQ-1 keeps at openxFactory**. The web tier
reflects that, and nothing in it says so. Route ownership at the three live
heads:

| owner | routes |
| --- | --- |
| **openDox** (`serve.py`, `serve_wire.py`, `serve_workbench.py`, `serve_project.py`) | `/snapshot.json` · `/capabilities` · `/project-register.json` · `/actions/edit` · `/actions/notebook` · `/actions/refresh` · `/workbench/model-catalog` · `/workbench/thread` · `/workbench/model-intake` · `/actions/workbench/chat-turn` · `/actions/workbench/document-abstract` · `/actions/workbench/model-intake` · `/actions/workbench/model-approval` |
| **openXdox** (contributed through `route_extension`) | `/actions/gate/` (POST prefix) · `/snapshot-index.json` · `/source` · `/source/` (prefix) · `/projections/evidence` · `/projections/workbench` · `/projections/role-authority` |
| **openxFactory's adapter** (`scripts/ideation_dashboard/serve_openxfactory_lanes.py`) | `/actions/apply-register-edits` · `/actions/dtn-seed` · `/actions/staging-seed` |

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
- `app.js` stops importing class-B modules directly. Its line 43
  (`import { isGateBearing, mountGateBar } from "./views/gate.js"`) becomes a
  lookup in the collected bindings, and a shell built with no gate binding
  registered renders the tab strip **without** the gate bar rather than failing
  to load.

### 4.2 Reaching the consumer late, mirroring `consumer_reach`

`src/opendox/consumer_reach.py` is the ruled shape for the direction problem:
*"It makes a surviving reach LATE, NAMED and REFUSABLE instead of an import-time
dependency on the consumer"*, and `route_column()` is its forwarder for a class
that lives in the consumer.

The front end needs the identical thing in one place: **the class-B route table
must not be a literal in an openDox module.** A contributed binding brings its
own routes with it, so `GATE_DISPOSE_ROUTE` and its twelve siblings travel to the
binding that uses them, and an openDox module that still needs a gate verb asks
the registry and gets a refusal — naming the layering — when no gate column is
registered. That refusal is § 1.2(b)'s dangling import turned into a first-class,
testable outcome.

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

1. **The census is complete, and `?` is TRANSITIONAL.** Every file under
   `src/opendox/web/` appears exactly once in a declared census (a small YAML or
   a table in the test), with a class. A new file with no row fails. This is the
   ratchet: it is what makes the boundary survive the next feature. **`?` is a
   class the census may carry only until S4**: after that slice a `?` row fails
   the assertion, because a permanent "undecided" is an escape hatch, not a
   boundary.
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
   | gate prefix | 10 | `lens-model.js`:1036/:1037, `repo-selector.js`:39/:43, `staging-workbench-model.js`:543/:817/:818/:821/:822/:826 — all `?` rows | S4 |
   | openxFactory lanes | 3 | `lens.js`:41/:45, `repo-selector.js`:46 — all `?` rows | S4 |
   | openXdox projection | 1 | `repo-selector.js`:33 (`/snapshot-index.json`) — a `?` row | S4 |
   | openXdox projection | 4 | `app.js`:183/:184, `viewer.js`:314, `wheel.js`:97 (`/source/`) — class A and class C | S6 |

   Fourteen of the eighteen are in `?` rows and clear at S4; the remaining four
   are the `/source/` sites Q4 rules on. The three gate constants declared in
   class-B files (`dispose.js`:28/:29, `gate.js`:120) are NOT in the count: they
   are exempt now and travel with the binding at S5. § 1.2(c)'s "13 gate route
   constants" measures the TREE; this row measures the ASSERTION, and the three
   in class-B files are the difference.
3. **Every relative import resolves**, and no class-A/C file imports a class-B
   module. This catches § 1.2(b) — `intent-feed.js` — as a test failure rather
   than a blank page, and it is the assertion that should have existed before the
   carve.
4. **No class-C file — and no declared class-A tail — carries a governance
   literal.** A closed word list (the registered profile's vocabulary, plus the
   eight controlled `Status:` words) grep-proven absent, mirroring
   openXdox-code's `tests/test_no_hardcoded_status_words.py`. Scope is the 13
   class-C files, the three class-A tails of § 2.2 rule 3, and `styles.css`
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
| **S2** | **Resolve the `intent-feed` edge (§ 6 Q5).** **RULED** — keep the manifest row, fix the importers (Brett Heap, 2026-09-12, #656 comment 5642758731): S2 makes the intent chips an OPTIONAL contributed binding; absent, the wheel and the dispose tray render without them. S2 is the slice that makes `app.js`'s module graph resolve again. | `dispose.js`, `wheel.js`, `styles.css`:1278–1295 | § 4.2 | assertion 3 green | openDox-code |
| **S3** | **The view registry.** `ViewBinding` + `collectViewBindings` + the shell's declared regions; `app.js`'s direct class-B imports become registry lookups; nothing is contributed yet, so the shell renders exactly as today with an empty extension tuple. | `app.js`, new `views/view_extension.js`, `index.html` | § 4.1 | collision + empty-tuple refusal tests | openDox-code |
| **S4** | **Split the five `?` files** — the PRECONDITION for S5, not its sequel. Only 3 of the 13 gate-route constants are declared in class-B files (`dispose.js`:28/:29, `gate.js`:120); the other 10 are declared in `lens-model.js`, `repo-selector.js` and `staging-workbench-model.js`, and both `swb-create.js` and `swb-session.js` IMPORT theirs from the last of those. The gate loop cannot be contributed until its route table stops living in `?` files. Each tail to its class per § 6's rulings: `lens-model.js`'s two routes, `lens.js`'s two openxFactory routes, `repo-selector.js`'s five cross-column routes, `staging-workbench-model.js`'s six, `explorer.js` whole. **RULED Q1, Q2, Q3** (Brett Heap, 2026-09-12, #656 comment 5642758731). | 5 files | § 4.2 | assertion 2 green for the openxFactory routes | openDox-code |
| **S5** | **Contribute the gate loop.** The four class-B files and all 13 route constants — now all declared in class-B files — move behind a binding openXdox supplies; a student install comes up with no gate bar, no dispose tray, no session verbs, and no 404. **Needs an openXdox-spec counterpart** (§ 5.1). | `dispose.js`, `gate.js`, `swb-create.js`, `swb-session.js` | § 4.1 + § 4.2 | assertion 2 green outright | openXdox-code (binding) + openDox-code (removal) |
| **S6** | **Re-home `/source/` per Q4** — the slice that discharges the census's one § 2.2 rule 1 breach. `openxdox/serve_projection.py` drops the `BARE_SOURCE_ROUTE` and `SOURCE_PREFIX` bindings (:57, :61, :375–384) and keeps `/snapshot-index.json` and the three `/projections/*` routes; openDox's `serve.py` declares the read-only pass-through as its own fixed core arm. `views/viewer.js` and `views/wheel.js`:97 become clean. **RULED Q4** (Brett Heap, 2026-09-12, #656 comment 5642758731). | `serve_projection.py`, `serve.py` (+ their tests) | § 4.1 | assertion 2 green for `viewer.js` | openXdox-code + openDox-code |
| **S7** | **Parameterize class C.** The display facet on `/capabilities`, the context hop, and the vocabulary by ROLE across the 13 class-C files PLUS the three declared class-A tails (`docs.js`:18, `grouping.js`:34–41/:51–52, `repo-selector-model.js`:517–522) — `wheel-model.js` and `model.js` first (they are the vocabulary the others import), `styles.css`'s four `--st-*` tokens last. Carries the § 1.1 packet-figure amendment. | 16 files + `serve.py` | § 4.3 | assertion 4 green; both exemptions declared | openDox-code (+ openxFactory for the packet row) |
| **S8** | **Re-home the 48 test files and un-narrow `validate`.** The 23 at openXdox-code pointing at an absent `web/` go to the leg the census says owns each bundle file; the narrowings (RULED Q-L5 (b′) / Q-L8 (b′)) lift for the web suites. All three `xfail(strict=True)` markers from S1 are already gone by S7 — 3 at S2, 2 at S5 and S6, 4 at S7 — so S8 starts from four unmarked assertions and carries none of its own. | 48 test files | — | both legs' `validate` | both |

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

---

## 6. Open questions for Brett Heap

Five, each principle-level, each with a RECOMMENDED answer. The census in § 3.2
is written to the recommendation and is redrawn on any other ruling.

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
