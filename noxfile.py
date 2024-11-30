"""All the process that can be run using nox.

The nox run are build in isolated environment that will be stored in .nox. to force the venv update, remove the .nox/xxx folder.
"""
from pathlib import Path

import nox


@nox.session(reuse_venv=True)
def docs(session):
    """Build the documentation."""
    session.install(".[doc]")
    b = session.posargs[0] if session.posargs else "html"
    dst = Path(__file__).parent / "docs" / "_build" / b
    session.run("sphinx-build", f"-b={b}", "-a", "-E", "docs", str(dst))


@nox.session(reuse_venv=True)
def lint(session):
    """Apply the pre-commits."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(reuse_venv=True)
def mypy(session):
    """Run a mypy check of the lib."""
    session.install("mypy")
    test_files = session.posargs or ["sphinxcontrib"]
    session.run("mypy", *test_files)


@nox.session(reuse_venv=True)
def test(session):
    """Run all the test using the environment varialbe of the running machine."""
    session.install(".[test]")
    session.install(
        "git+https://github.com/12rambau/sphinx.git@27cb8ead601299e0fba8a98a298ddffc0c482812"
    )
    test_files = session.posargs or ["tests"]
    session.run("pytest", "--color=yes", "--cov", "--cov-report=xml", *test_files)
