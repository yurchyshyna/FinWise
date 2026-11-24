import pytest
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_health_ok(monkeypatch):
    monkeypatch.setattr(main.db, "ping", lambda: None)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_db_down(monkeypatch):
    def broken_ping():
        raise RuntimeError("немає з'єднання")

    monkeypatch.setattr(main.db, "ping", broken_ping)
    response = client.get("/api/health")
    assert response.status_code == 503


def test_list_transactions(monkeypatch):
    fake = [{"id": 1, "amount": 100.0, "category": "Їжа", "description": ""}]
    monkeypatch.setattr(main.db, "list_transactions", lambda: fake)
    response = client.get("/api/transactions")
    assert response.status_code == 200
    assert response.json() == fake


def test_add_transaction(monkeypatch):
    saved = {}

    def fake_add(amount, category, description):
        saved["args"] = (amount, category, description)
        return {"id": 1, "amount": amount, "category": category}

    monkeypatch.setattr(main.db, "add_transaction", fake_add)
    response = client.post(
        "/api/transactions",
        json={"amount": 250.5, "category": "Транспорт", "description": "Метро"},
    )
    assert response.status_code == 201
    assert saved["args"] == (250.5, "Транспорт", "Метро")


def test_add_transaction_default_category(monkeypatch):
    saved = {}

    def fake_add(amount, category, description):
        saved["args"] = (amount, category, description)
        return {"id": 2}

    monkeypatch.setattr(main.db, "add_transaction", fake_add)
    response = client.post("/api/transactions", json={"amount": 10})
    assert response.status_code == 201
    assert saved["args"] == (10, "Інші витрати", "")


@pytest.mark.parametrize("amount", [0, -5])
def test_add_transaction_invalid_amount(amount):
    response = client.post("/api/transactions", json={"amount": amount})
    assert response.status_code == 422
