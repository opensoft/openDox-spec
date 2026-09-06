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
[SECURITY.md](SECURITY.md).
