import pytest

from app import config


def test_required_returns_value(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "abc")
    assert config._required("TEST_VAR") == "abc"


def test_required_missing_raises(monkeypatch):
    monkeypatch.delenv("TEST_VAR", raising=False)
    with pytest.raises(RuntimeError):
        config._required("TEST_VAR")


def test_required_empty_raises(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "")
    with pytest.raises(RuntimeError):
        config._required("TEST_VAR")
