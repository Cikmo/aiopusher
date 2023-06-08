"""This is a test file for testing the testing framework."""

from aiopusher import __version__


def test_blah():
    """Test for testing purposes."""
    assert True


def test_version():
    """Test version."""
    assert __version__() == "0.1.0"
