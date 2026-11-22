"""Backend API системи FinWise (мінімальна версія для контейнеризації)."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()  # створюємо таблицю, якщо її ще немає
    yield


app = FastAPI(title="FinWise API", lifespan=lifespan)


class ExpenseIn(BaseModel):
    amount: float = Field(gt=0, description="Сума витрати")
    category: str = "Інші витрати"
    description: str = ""


@app.get("/api/health")
def health():
    """Перевірка стану: API живий і бачить базу даних."""
    try:
        db.ping()
    except Exception:
        raise HTTPException(status_code=503, detail="База даних недоступна")
    return {"status": "ok"}


@app.get("/api/transactions")
def list_transactions():
    return db.list_transactions()


@app.post("/api/transactions", status_code=201)
def add_transaction(expense: ExpenseIn):
    return db.add_transaction(expense.amount, expense.category, expense.description)
