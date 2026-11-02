import logging
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, status
from sqlmodel import func, select

from ..database import SessionDep
from ..models import Category, Expense, ExpenseCreate, ExpensePublic, ExpenseUpdate, Summary
from ..security import CurrentUser

router = APIRouter(prefix="/expenses", tags=["expenses"])
log = logging.getLogger("uvicorn.error")

BIG_EXPENSE = 10_000


def alert_big_expense(username: str, amount: float) -> None:
    # Runs after the response is sent. In a real app: send an email or a push notification.
    log.info("Big expense alert: %s spent Rs %.2f", username, amount)


def get_owned_expense(expense_id: int, user: CurrentUser, session: SessionDep) -> Expense:
    expense = session.get(Expense, expense_id)
    if expense is None or expense.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post("", response_model=ExpensePublic, status_code=status.HTTP_201_CREATED)
def create_expense(data: ExpenseCreate, user: CurrentUser, session: SessionDep, background: BackgroundTasks):
    expense = Expense.model_validate(data, update={"owner_id": user.id})
    session.add(expense)
    session.commit()
    session.refresh(expense)
    if expense.amount >= BIG_EXPENSE:
        background.add_task(alert_big_expense, user.username, expense.amount)
    return expense


@router.get("", response_model=list[ExpensePublic])
def list_expenses(
    user: CurrentUser,
    session: SessionDep,
    category: Category | None = None,
    offset: int = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    query = select(Expense).where(Expense.owner_id == user.id)
    if category:
        query = query.where(Expense.category == category)
    query = query.order_by(Expense.spent_on.desc(), Expense.id.desc()).offset(offset).limit(limit)
    return session.exec(query).all()


# Declared before "/{expense_id}", otherwise FastAPI would try to read "summary" as an ID.
@router.get("/summary", response_model=Summary)
def summary(user: CurrentUser, session: SessionDep):
    rows = session.exec(
        select(Expense.category, func.sum(Expense.amount))
        .where(Expense.owner_id == user.id)
        .group_by(Expense.category)
    ).all()
    by_category = {category.value: round(total, 2) for category, total in rows}
    return Summary(total=round(sum(by_category.values()), 2), by_category=by_category)


@router.get("/{expense_id}", response_model=ExpensePublic)
def read_expense(expense_id: int, user: CurrentUser, session: SessionDep):
    return get_owned_expense(expense_id, user, session)


@router.patch("/{expense_id}", response_model=ExpensePublic)
def update_expense(expense_id: int, data: ExpenseUpdate, user: CurrentUser, session: SessionDep):
    expense = get_owned_expense(expense_id, user, session)
    expense.sqlmodel_update(data.model_dump(exclude_unset=True))
    session.add(expense)
    session.commit()
    session.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, user: CurrentUser, session: SessionDep):
    session.delete(get_owned_expense(expense_id, user, session))
    session.commit()
