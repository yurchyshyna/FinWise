"""Тестові значення змінних оточення.

config.py вимагає ці змінні під час імпорту, тому їх задано до імпорту застосунку.
"""

import os

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_NAME", "test")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
