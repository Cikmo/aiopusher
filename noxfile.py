"""Nox configuration file."""

import nox


@nox.session(python=["3.8", "3.9", "3.10", "3.11"], reuse_venv=True)
def test(session: nox.Session):
    """Run the test suite."""
    session.run("poetry", "install", "--without", "dev", "--sync", external=True)

    session.run("pytest", "tests/")


@nox.session(reuse_venv=True)
def lint(session: nox.Session):
    """Run pylint."""
    session.run("poetry", "install", "--sync", external=True)

    session.run("pylint", "src/", "tests/", "noxfile.py")


@nox.session(reuse_venv=True)
def black(session: nox.Session):
    """Run black."""
    session.run("poetry", "install", "--sync", external=True)

    session.run("black", "src/", "tests/", "noxfile.py", "--check")


@nox.session(reuse_venv=True)
def typecheck(session: nox.Session):
    """Run mypy."""
    session.run("poetry", "install", "--sync", external=True)

    session.run("pyright")
