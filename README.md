# openDox-spec

The **spec leg** of the `opendox` project: requirements, decisions and
acceptance criteria. The implementation lives in
[`opensoft/openDox-code`](https://github.com/opensoft/openDox-code).

**Clone the assembly root, not this repository.** This leg is mounted as a
submodule at `spec/` inside
[`opensoft/openDox`](https://github.com/opensoft/openDox), which
is what pins the commit of this repository that the project currently is:

```sh
git clone --recurse-submodules https://github.com/opensoft/openDox.git
cd openDox
make bootstrap
```

Working here directly is fine — it is an ordinary repository with an ordinary
branch. What advancing this leg does NOT do is advance the project: that is a
commit in the assembly root moving the gitlink, `contracts/spec-pin.yaml` and
any workflow `@<sha>` reference together.

Being the spec leg confers no authority over specifications. The split is
navigation; authority travels in grants, and a project that keeps spec and
code in one repository is reviewed identically.

Topic: `xf-project-opendox`.

## Posture

Contributing guidelines and the code of conduct live in the assembly root,
not here: see
[CONTRIBUTING.md](https://github.com/opensoft/openDox/blob/main/CONTRIBUTING.md)
and
[CODE_OF_CONDUCT.md](https://github.com/opensoft/openDox/blob/main/CODE_OF_CONDUCT.md)
in `opensoft/openDox`. Security reports for this repository go through
[SECURITY.md](SECURITY.md). The `validate` check is a required status check
on `main`, enforced by a repository ruleset — see
[docs/branch-protection.md](docs/branch-protection.md).

## Documentation

The doc index for this repository. Everything under `docs/` is listed here,
and a new document is linked from this table in the same pull request that
adds it — the xFactory family's standing rule, levelled across all six
`openDox`/`openXdox` repositories by the OQ-O scaffold pass
(`opensoft/openxFactory#656`).

| document | what it is |
|---|---|
| [docs/branch-protection.md](docs/branch-protection.md) | the repository ruleset that makes `validate` a required status check on `main`, its `evaluate` → `active` history, and the one policy difference between the two families |
| [docs/front-end-package-boundary.md](docs/front-end-package-boundary.md) | `Status: draft` — the front-end package boundary `split-opendox-two-layer-product` § 3.4 asks openDox to INVENT: the measured `src/opendox/web/` census, the three destination classes and the test each file must pass, the registration mechanism, the code slices, and SIX open questions — Q1–Q5 RULED (2026-09-12, #656 comment 5642758731) and **Q6 OPEN** (amendment #2: slice S8 needs a carve-manifest RE-DESTINATION form). § 7 carries the note's amendment record |
| [docs/ideation-dashboard-session-runbook.md](docs/ideation-dashboard-session-runbook.md) | a draft process runbook for operating the ideation dashboard's branch sessions — the verbs, their CLI parity, where the derived artifacts live, and the rules that must not be broken while testing |
| [docs/stale-citations-erratum-2026-09-10.md](docs/stale-citations-erratum-2026-09-10.md) | BUILD-arc record: the source-path citations the carve left stale in the session runbook, and their live targets, without editing the frozen document |

`openspec/project.md` is not a document in this sense — it is this leg's
OpenSpec instance file, read by the `openspec` CLI and by
`tests/test_leg_shape.py`.
