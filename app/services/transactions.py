from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import CustomError
from app.crud.balance import get_user_balance
from app.crud.transactions import get_transactions, get_transaction, update_transaction, create_transaction, \
    delete_transaction
from app.schemas import TransactionUpdate, TransactionCreate
import redis.asyncio as aioredis


class TransactionService:
    @staticmethod
    async def list_transactions(
            db: AsyncSession,
            user_id: int,
            is_expense: bool,
            category_id: int,
            year: int,
            month: int
    ):
        transactions = await get_transactions(db, user_id, is_expense, category_id, year, month)
        total_amount = sum(transaction.amount for transaction in transactions)
        return {"transactions": transactions, "total_amount": total_amount}

    @staticmethod
    async def edit_transaction(
            db: AsyncSession,
            transaction_data: TransactionUpdate,
            transaction_id: int,
            user_id: int,
            redis: aioredis.Redis
    ):
        transaction = await get_transaction(db, transaction_id)
        if not transaction:
            raise CustomError(status_code=404, name="Транзакция не найдена")
        if transaction.user_id != user_id:
            raise CustomError(status_code=403, name="Нет прав для редактирования данной транзакции")
        balance = await get_user_balance(user_id, redis)
        if transaction_data.amount:
            if transaction.is_expense and (float(balance) + transaction.amount) < transaction_data.amount:
                raise CustomError(status_code=400, name="Недостаточно средств")
        return await update_transaction(db, transaction_data, transaction, redis, user_id, float(balance))

    @staticmethod
    async def add_transaction(
            db: AsyncSession,
            transaction_data: TransactionCreate,
            user_id: int,
            redis: aioredis.Redis
    ):
        balance = await get_user_balance(user_id, redis)
        if transaction_data.is_expense and float(balance) < transaction_data.amount:
            raise CustomError(status_code=400, name="Недостаточно средств на балансе")
        return await create_transaction(db, transaction_data, user_id, redis)

    @staticmethod
    async def remove_transaction(
            db: AsyncSession,
            transaction_id: int,
            user_id: int,
            redis: aioredis.Redis
    ):
        transaction = await get_transaction(db, transaction_id)
        if not transaction:
            raise CustomError(status_code=404, name="Транзакция не найдена")
        if transaction.user_id != user_id:
            raise CustomError(status_code=403, name="Нет прав для редактирования данной транзакции")
        balance = await get_user_balance(user_id, redis)
        return await delete_transaction(db, transaction, user_id, redis, float(balance))
