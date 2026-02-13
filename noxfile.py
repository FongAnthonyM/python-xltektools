#!/usr/bin/env python
"""noxfile.py
Nox sessions.
"""

# Header #
__package_name__ = "xltektools"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2022, Anthony Fong"
__license__ = "MIT"

__version__ = "0.6.0"


# Imports #
# Standard Libraries #
import os
import shlex
import shutil
import stat
import sys
from collections.abc import Callable
from pathlib import Path
from textwrap import dedent
from typing import Any

# Third-Party Packages #
import nox
from nox import Session, session


# Definitions #
# Constants #
package = "xltektools"
python_versions = ["3.14"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = (
    "pre-commit",
    "mypy",
    "tests",
    "typeguard",
    "xdoctest",
    "docs-build",
)
nox.options.default_venv_backend = "uv"


# Functions #
def on_rm_error(func: Callable[[str], None], path: str, exc_info: tuple[Any, Any, Any]) -> None:
    """Error handler for shutil.rmtree.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : shutil.rmtree(path, onerror=on_rm_error)
    """
    if not os.access(path, os.W_OK):
        Path(path).chmod(stat.S_IWRITE)
        func(path)
    else:
        raise


def activate_virtualenv_in_precommit_hooks(session: Session) -> None:
    """Activate virtualenv in hooks installed by pre-commit.

    This function patches git hooks installed by pre-commit to activate the session's virtual environment. This allows
    pre-commit to locate hooks in that environment when invoked from git.

    Args:
        session: The Session object.
    """
    assert session.bin is not None  # nosec

    # Only patch hooks containing a reference to this session's bindir. Support quoting rules for Python and bash, but
    # strip the outermost quotes so we can detect paths within the bindir, like <bindir>/python.
    bindirs = [
        bindir[1:-1] if bindir[0] in "'\"" else bindir for bindir in (repr(session.bin), shlex.quote(session.bin))
    ]

    virtualenv = session.env.get("VIRTUAL_ENV")
    if virtualenv is None:
        return

    headers = {
        # pre-commit < 2.16.0
        "python": f"""\
            import os
            os.environ["VIRTUAL_ENV"] = {virtualenv!r}
            os.environ["PATH"] = os.pathsep.join((
                {session.bin!r},
                os.environ.get("PATH", ""),
            ))
            """,
        # pre-commit >= 2.16.0
        "bash": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
        # pre-commit >= 2.17.0 on Windows forces sh shebang
        "/bin/sh": f"""\
            VIRTUAL_ENV={shlex.quote(virtualenv)}
            PATH={shlex.quote(session.bin)}"{os.pathsep}$PATH"
            """,
    }

    hookdir = Path(".git") / "hooks"
    if not hookdir.is_dir():
        return

    for hook in hookdir.iterdir():
        if hook.name.endswith(".sample") or not hook.is_file():
            continue

        if not hook.read_bytes().startswith(b"#!"):
            continue

        text = hook.read_text()

        if not any(Path("A") == Path("a") and (bindir.lower() in text.lower() or bindir in text) for bindir in bindirs):
            continue

        lines = text.splitlines()

        for executable, header in headers.items():
            if executable in lines[0].lower():
                lines.insert(1, dedent(header))
                hook.write_text("\n".join(lines))
                break


# Sessions #
# New Environments
@session(name="pre-commit", python=python_versions[0], tags=["new_venv"])
def precommit(session: Session) -> None:
    """Lint using pre-commit."""
    args = session.posargs or [
        "run",
        "--all-files",
        "--hook-stage=manual",
    ]
    session.run("pre-commit", *args)
    if args and args[0] == "install":
        activate_virtualenv_in_precommit_hooks(session)


@session(python=python_versions, tags=["new_venv"])
def mypy(session: Session) -> None:
    """Static type checking using mypy."""
    args = session.posargs or [".", "docs/conf.py"]
    session.install(".[dev]")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=python_versions, tags=["new_venv"])
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".[dev]")
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage", posargs=[])


@session(python=python_versions[0], tags=["new_venv"])
def coverage(session: Session) -> None:
    """Produce the coverage report."""
    args = session.posargs or ["report"]

    session.install("coverage[toml]")

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(python=python_versions[0], tags=["new_venv"])
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    session.install(".[dev]")
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@session(python=python_versions, tags=["new_venv"])
def xdoctest(session: Session) -> None:
    """Run in-line examples with xdoctest."""
    if session.posargs:
        args = [package, *session.posargs]
    else:
        args = [f"--modname={package}", "--command=all"]
        if "FORCE_COLOR" in os.environ:
            args.append("--colored=1")

    session.install(".[dev]")
    session.run("python", "-m", "xdoctest", *args)


@session(name="docs-build", python=python_versions[0], tags=["new_venv"])
def docs_build(session: Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")
    session.install(".[dev]")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir, onerror=on_rm_error)

    session.run("sphinx-build", *args)


@session(python=python_versions[0], tags=["new_venv"])
def docs(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]
    session.install(".[dev]")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir, onerror=on_rm_error)

    session.run("sphinx-autobuild", *args)


# Active Environment
@session(name="pre-commit_active", python=python_versions[0], venv_backend="none", tags=["active_venv"])
def precommit_active(session: Session) -> None:
    """Lint using pre-commit in the active environment."""
    args = session.posargs or [
        "run",
        "--all-files",
        "--hook-stage=manual",
    ]
    session.run("pre-commit", *args)


@session(python=python_versions, venv_backend="none", tags=["active_venv"])
def mypy_active(session: Session) -> None:
    """Static type checking using mypy in the active environment."""
    args = session.posargs or [".", "docs/conf.py"]
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=python_versions, venv_backend="none", tags=["active_venv"])
def tests_active(session: Session) -> None:
    """Run the test suite using the active environment."""
    try:
        session.run("coverage", "run", "--parallel", "-m", "pytest", *session.posargs)
    finally:
        if session.interactive:
            session.notify("coverage_active", posargs=[])


@session(python=python_versions[0], venv_backend="none", tags=["active_venv"])
def coverage_active(session: Session) -> None:
    """Produce the coverage report using the active environment."""
    args = session.posargs or ["report"]

    if not session.posargs and any(Path().glob(".coverage.*")):
        session.run("coverage", "combine")

    session.run("coverage", *args)


@session(python=python_versions[0], venv_backend="none", tags=["active_venv"])
def typeguard_active(session: Session) -> None:
    """Runtime type checking using Typeguard in the active environment."""
    session.run("pytest", f"--typeguard-packages={package}", *session.posargs)


@session(python=python_versions, venv_backend="none", tags=["active_venv"])
def xdoctest_active(session: Session) -> None:
    """Runs in-line examples with xdoctest using the active environment."""
    if session.posargs:
        args = [package, *session.posargs]
    else:
        args = [f"--modname={package}", "--command=all"]
        if "FORCE_COLOR" in os.environ:
            args.append("--colored=1")
    session.run("python", "-m", "xdoctest", *args)


@session(name="docs-build_active", python=python_versions[0], venv_backend="none", tags=["active_venv"])
def docs_build_active(session: Session) -> None:
    """Build the documentation using the active environment."""
    args = session.posargs or ["docs", "docs/_build"]
    if not session.posargs and "FORCE_COLOR" in os.environ:
        args.insert(0, "--color")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir, onerror=on_rm_error)

    session.run("sphinx-build", *args)


@session(python=python_versions[0], venv_backend="none")
def docs_active(session: Session) -> None:
    """Build and serve the documentation with live reloading on file changes using the active environment."""
    args = session.posargs or ["--open-browser", "docs", "docs/_build"]

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir, onerror=on_rm_error)

    session.run("sphinx-autobuild", *args)
