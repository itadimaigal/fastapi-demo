from datetime import date
from enum import StrEnum

from sqlmodel import Field, SQLModel


class Category(StrEnum):
    food = "food"
    travel = "travel"
    bills = "bills"
    shopping = "shopping"
    other = "other"


# ---------- users ----------
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str


class UserCreate(SQLModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)


class UserPublic(SQLModel):
    id: int
    username: str


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# ---------- expenses ----------
class ExpenseBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0, description="Amount in rupees")
    category: Category = Category.other
    spent_on: date = Field(default_factory=date.today)


class Expense(ExpenseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", index=True)


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    amount: float | None = Field(default=None, gt=0)
    category: Category | None = None
    spent_on: date | None = None


class ExpensePublic(ExpenseBase):
    id: int


class Summary(SQLModel):
    total: float
    by_category: dict[str, float]
