"""The settings read ``.env`` from the project folder, so commands work without ``uv run --env-file``; variables
set in the real environment (server, systemd, Docker) win over the file."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def currency_in_settings(project: Path, environ: dict[str, str]) -> str:
    """Load the project's settings in a fresh interpreter and return LFS_CURRENCY."""
    result = subprocess.run(
        [sys.executable, "-c", "import project.settings as s; print(s.LFS_CURRENCY)"],
        cwd=project,
        env={**environ, "PYTHONPATH": os.pathsep.join([str(project), os.environ.get("PYTHONPATH", "")])},
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def project_with_env_file(tmp_path: Path, content: str) -> Path:
    """Copy the project's settings to ``tmp_path`` and write ``.env`` next to them."""
    shutil.copytree(PROJECT / "project", tmp_path / "project")
    (tmp_path / ".env").write_text(content)
    return tmp_path


def environ_without(*names: str) -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key not in names}


def test_settings_read_the_env_file(tmp_path):
    project = project_with_env_file(tmp_path, "DJANGO_DEBUG=true\nLFS_CURRENCY=CHF\n")

    assert currency_in_settings(project, environ_without("LFS_CURRENCY", "DJANGO_DEBUG")) == "CHF"


def test_real_environment_variables_win_over_the_env_file(tmp_path):
    project = project_with_env_file(tmp_path, "DJANGO_DEBUG=true\nLFS_CURRENCY=CHF\n")

    environ = {**environ_without("LFS_CURRENCY"), "LFS_CURRENCY": "USD"}
    assert currency_in_settings(project, environ) == "USD"
