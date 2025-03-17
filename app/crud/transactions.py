from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import CustomError
from app.crud.balance import update_balance, get_balance
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionUpdate


async def create_transaction(
        db: AsyncSession,
        transaction_data: TransactionCreate,
        user_id: int,
        redis
):
    balance = await get_balance(user_id, redis)
    if transaction_data.is_expense and float(balance) < transaction_data.amount:
        raise CustomError(status_code=400, name="Недостаточно средств на балансе")
    db_transaction = Transaction(**transaction_data.dict(), user_id=user_id)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    await update_balance(user_id, db_transaction.amount, db_transaction.is_expense, redis)
    return db_transaction


async def get_transactions(
        db: AsyncSession,
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
    return (await db.scalars(select(Transaction).where(*filters))).all()


async def update_transaction(
        db: AsyncSession,
        transaction_data: TransactionUpdate,
        transaction_id: int,
        user_id: int,
        redis
):
    transaction = (await db.scalars(select(Transaction).where(Transaction.id == transaction_id))).first()
    if not transaction:
        raise CustomError(status_code=404, name="Транзакция не найдена")
    if transaction.user_id != user_id:
        raise CustomError(status_code=403, name="Нет прав для редактирования данной транзакции")
    balance = await get_balance(user_id, redis)
    if transaction.is_expense and (float(balance) + transaction.amount) < transaction_data.amount:
        raise CustomError(status_code=400, name="Недостаточно средств")
    else:
        await redis.set(user_id, float(balance) + transaction.amount)
    for key, value in transaction_data.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)
    await db.commit()
    await db.refresh(transaction)
    await update_balance(user_id, transaction.amount, transaction.is_expense, redis)
    return transaction


async def delete_transaction(
        db: AsyncSession,
        transaction_id: int,
        user_id: int,
        redis
):
    transaction = (await db.scalars(select(Transaction).where(Transaction.id == transaction_id))).first()
    if not transaction:
        raise CustomError(status_code=404, name="Транзакция не найдена")
    if transaction.user_id != user_id:
        raise CustomError(status_code=403, name="Нет прав для редактирования данной транзакции")
    balance = await get_balance(user_id, redis)
    amount = transaction.amount
    await db.delete(transaction)
    await db.commit()
    await redis.set(user_id, float(balance) + amount)
