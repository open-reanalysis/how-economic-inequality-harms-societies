"""Offline tests and library import path."""

import socket
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    """Fail unexpected network use in ordinary tests."""

    def refused(*args, **kwargs):
        raise AssertionError("Tests must not contact external services")

    monkeypatch.setenv("OFFLINE", "1")
    monkeypatch.setattr(socket, "create_connection", refused)
    monkeypatch.setattr(socket.socket, "connect", refused)
