"""Bootstrap-posture shape tests for the openDox-spec leg.

Asserts the files a public, day-one-postured repository must carry (see
openxFactory openspec/changes/split-opendox-two-layer-product/tasks.md
§ 1.3-1.5), and — for this leg specifically — that its OpenSpec instance
validates cleanly.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    ".gitignore",
    "LICENSE",
    "SECURITY.md",
    ".github/CODEOWNERS",
]


@pytest.mark.parametrize("relpath", REQUIRED_FILES)
def test_required_file_exists(relpath: str) -> None:
    path = ROOT / relpath
    assert path.is_file(), f"expected {relpath} to exist at {path}"


def test_license_is_apache() -> None:
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Apache License" in text


def test_role_directory_exists() -> None:
    # This is the spec leg: its role directory is requirements/.
    assert (ROOT / "requirements").is_dir()


def test_openspec_instance_present() -> None:
    assert (ROOT / "openspec").is_dir()
    assert (ROOT / "openspec" / "specs").is_dir()
    assert (ROOT / "openspec" / "changes").is_dir()


def test_openspec_validate() -> None:
    openspec = shutil.which("openspec")
    if openspec is None:
        pytest.skip("openspec CLI is not on PATH")
    proc = subprocess.run(
        [openspec, "validate", "--all", "--strict"],
        cwd=str(ROOT),
        env={**os.environ, "OPENSPEC_TELEMETRY": "0"},
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, (
        f"openspec validate --all --strict exited {proc.returncode}\n"
        f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
    )


def test_branch_protection_evidence_exists() -> None:
    # tasks.md § 1.5's evidence line: a ruleset is a repository SETTING, so
    # the only thing a tree can assert is that the evidence file naming it is
    # present. Levelled across all six repositories by the OQ-O pass
    # (openxFactory#656).
    assert (ROOT / "docs" / "branch-protection.md").is_file()


def test_openspec_project_md_exists() -> None:
    # The instance's own conventions file. openXdox-spec had no
    # openspec/project.md until the OQ-O levelling pass (openxFactory#656);
    # this test is what keeps both spec legs level from here on.
    assert (ROOT / "openspec" / "project.md").is_file()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
