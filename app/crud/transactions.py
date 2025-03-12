from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.core.utils import CustomError
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionUpdate


def create_transaction(
        db: Session,
        transaction_data: TransactionCreate,
        user_id: int
):
    db_transaction = Transaction(**transaction_data.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(
        db: Session,
        user_id: int,
        is_expense: bool,
        category_id: int,
        year: int,
        month: int
):
    filters = [
        Transaction.user_id == user_id,
        Transaction.is_expense == is_expense,
        extract("year", Transaction.created_at) == year,
        extract("month", Transaction.created_at) == month
    ]
    if category_id:
        filters.append(Transaction.category_id == category_id)
    return db.query(Transaction).filter(*filters).all()


def update_transaction(
        db: Session,
        transaction_data: TransactionUpdate,
        transaction_id: int,
        user_id: int
):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise CustomError(status_code=404, name="Транзакция не найдена")
    if transaction.user_id != user_id:
        raise CustomError(status_code=403, name="Нет прав для редактирования данной транзакции")
    for key, value in transaction_data.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return transaction
