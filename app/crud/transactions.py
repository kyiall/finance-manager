import redis.asyncio as aioredis
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.balance import update_balance
from app.models import Transaction
from app.schemas import TransactionCreate, TransactionUpdate


async def create_transaction(
        db: AsyncSession,
        transaction_data: TransactionCreate,
        user_id: int,
        redis: aioredis.Redis
):
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
        transaction: Transaction,
        redis: aioredis.Redis,
        user_id,
        balance: float
):
    previous_amount = transaction.amount
    for key, value in transaction_data.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)
    await db.commit()
    await db.refresh(transaction)
    if transaction_data.amount:
        await redis.set(user_id, balance + previous_amount)
        await update_balance(user_id, transaction.amount, transaction.is_expense, redis)
    return transaction


async def delete_transaction(
        db: AsyncSession,
        transaction: Transaction,
        user_id,
        redis: aioredis.Redis,
        balance: float
):
    amount = transaction.amount
    await db.delete(transaction)
    await db.commit()
    await redis.set(user_id, balance + amount)


async def get_transaction(db: AsyncSession, transaction_id: int):
    transaction = (await db.scalars(select(Transaction).where(Transaction.id == transaction_id))).first()
    return transaction
