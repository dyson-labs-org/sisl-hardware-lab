"""Version and import smoke tests."""

from sisl_hardware_lab import __version__


def test_version_is_defined() -> None:
    assert __version__ == "0.1.0"
