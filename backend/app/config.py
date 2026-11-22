"""Налаштування беруться лише зі змінних оточення (фактор III з 12-Factor App)."""

import os


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Не задано змінну оточення {name}")
    return value


class Settings:
    db_host = _required("DB_HOST")
    db_port = int(os.environ.get("DB_PORT", "5432"))
    db_name = _required("DB_NAME")
    db_user = _required("DB_USER")
    db_password = _required("DB_PASSWORD")


settings = Settings()
