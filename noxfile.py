import nox


# An example nox task definition that runs on many supported Python versions:
@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def test(session: nox.Session):
    session.run("poetry", "install", "--without", "dev", "--no-root", external=True)

    session.run("pytest", "tests/")


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def test_lib_versions(session: nox.Session):
    session.run(
        "poetry",
        "install",
        "--without",
        "dev",
        "--without",
        "lib",
        "--with",
        "lib-test",
        "--no-root",
        external=True,
    )

    session.run("pytest", "tests/")
