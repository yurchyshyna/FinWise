"""PostgreSQL."""

import psycopg
from psycopg.rows import dict_row

from .config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id          SERIAL PRIMARY KEY,
    amount      NUMERIC(12, 2) NOT NULL,
    category    TEXT NOT NULL DEFAULT 'Інші витрати',
    description TEXT NOT NULL DEFAULT '',
    source      TEXT NOT NULL DEFAULT 'manual',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


def connect():
    return psycopg.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        row_factory=dict_row,
        connect_timeout=5,
    )


def init_db() -> None:
    with connect() as conn:
        conn.execute(SCHEMA)


def ping() -> None:
    with connect() as conn:
        conn.execute("SELECT 1")


def list_transactions(limit: int = 50) -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, amount, category, description, source, created_at "
            "FROM transactions ORDER BY created_at DESC LIMIT %s",
            (limit,),
        ).fetchall()
    return rows


def add_transaction(amount: float, category: str, description: str) -> dict:
    with connect() as conn:
        row = conn.execute(
            "INSERT INTO transactions (amount, category, description) "
            "VALUES (%s, %s, %s) "
            "RETURNING id, amount, category, description, source, created_at",
            (amount, category, description),
        ).fetchone()
    return row
