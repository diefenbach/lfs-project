"""The shop refuses to start with DEBUG on for a public host, e.g. when a ``.env`` copied from ``.env.example``
ends up on the server: debug pages would show code and settings, and the development secret key would be live."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def load_settings(tmp_path: Path, **variables: str) -> subprocess.CompletedProcess:
    """Load a copy of the project's settings (without any ``.env``) in a fresh interpreter with ``variables``."""
    shutil.copytree(PROJECT / "shop", tmp_path / "shop")
    environ = {key: value for key, value in os.environ.items() if not key.startswith("DJANGO_")}
    environ["PYTHONPATH"] = os.pathsep.join([str(tmp_path), os.environ.get("PYTHONPATH", "")])
    return subprocess.run(
        [sys.executable, "-c", "import shop.settings as s; print(s.DEBUG)"],
        cwd=tmp_path,
        env={**environ, **variables},
        capture_output=True,
        text=True,
    )


def test_debug_with_a_public_host_refuses_to_start(tmp_path):
    result = load_settings(tmp_path, DJANGO_DEBUG="true", DJANGO_ALLOWED_HOSTS="shop.example.com")

    assert result.returncode != 0
    assert "DJANGO_DEBUG" in result.stderr


def test_debug_on_localhost_starts(tmp_path):
    result = load_settings(tmp_path, DJANGO_DEBUG="true", DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1")

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "True"
