"""In production the static files get content-hashed names, so a browser or proxy cache never serves an old file
after an update (an old script with new HTML broke the review form); during development the names stay plain."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
CSS = "lfs_theme/css/lfs_theme.css"


def run(tmp_path: Path, code: list[str], **variables: str) -> subprocess.CompletedProcess:
    """Run ``code`` (manage.py arguments, or ``-c`` and Python) in a copy of the project with ``variables``."""
    if not (tmp_path / "project").exists():
        shutil.copytree(PROJECT / "project", tmp_path / "project")
        shutil.copy(PROJECT / "manage.py", tmp_path / "manage.py")
    environ = {key: value for key, value in os.environ.items() if not key.startswith("DJANGO_")}
    environ["PYTHONPATH"] = os.pathsep.join([str(tmp_path), os.environ.get("PYTHONPATH", "")])
    environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
    return subprocess.run(
        [sys.executable, *code], cwd=tmp_path, env={**environ, **variables}, capture_output=True, text=True
    )


STATIC_URL_OF_CSS = ["-c", f"import django; django.setup(); from django.templatetags.static import static; print(static('{CSS}'))"]
PRODUCTION = {"DJANGO_DEBUG": "false", "DJANGO_SECRET_KEY": "test-only", "DJANGO_ALLOWED_HOSTS": "shop.example.com"}


def test_production_serves_static_files_under_hashed_names(tmp_path):
    collected = run(tmp_path, ["manage.py", "collectstatic", "--noinput", "-v0"], **PRODUCTION)
    assert collected.returncode == 0, collected.stderr

    result = run(tmp_path, STATIC_URL_OF_CSS, **PRODUCTION)

    assert result.returncode == 0, result.stderr
    assert re.fullmatch(r"/static/lfs_theme/css/lfs_theme\.[0-9a-f]{12}\.css", result.stdout.strip())


def test_development_serves_static_files_under_their_plain_names(tmp_path):
    result = run(tmp_path, STATIC_URL_OF_CSS, DJANGO_DEBUG="true")

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == f"/static/{CSS}"
