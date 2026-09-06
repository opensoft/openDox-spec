# openDox-spec

This is the OpenSpec instance for the **spec leg** of the `opendox` project.

`opensoft/openDox-spec` holds requirements, decisions and acceptance criteria
for openDox — a project split into three repositories under the
[openRepoShape](https://github.com/opensoft/openRepoShape) standard: the
assembly root `opensoft/openDox`, this spec leg, and the code leg
`opensoft/openDox-code`. This repository is normally reached as the `spec/`
submodule of the assembly root; see that repository's `AGENTS-shape.md` for
the rules that span all three.

## Conventions

- Proposals, specs and changes in this instance describe **this leg's**
  scope only: requirements, decisions and acceptance criteria for openDox.
  Implementation work belongs in `opensoft/openDox-code`.
- Follow the standard OpenSpec change lifecycle: `openspec/changes/<id>/`
  while a change is in flight, archived into `openspec/specs/` once landed.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` must pass before
  any change here is merged; the `validate` GitHub Actions workflow runs it
  on every pull request.
