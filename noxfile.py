"""Nox configuration file."""

import nox


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def test(session: nox.Session):
    """Run the test suite."""
    session.run("poetry", "install", "--without", "dev", "--no-root", external=True)

    session.run("pytest", "tests/")


@nox.session(python="3.11", reuse_venv=True)
def lint(session: nox.Session):
    """Run pylint."""
    session.run("poetry", "install", "--no-root", external=True)

    session.run("pylint", "pusher_client/", "tests/", "noxfile.py")
