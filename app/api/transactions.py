import redis.asyncio as aioredis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_master, get_db_replica
from app.core.redis_conf import get_redis
from app.core.security import get_current_user
from app.models.users import User
from app.schemas.transactions import TransactionResponse, TransactionCreate, TransactionUpdate, TransactionList, \
    TransactionListParams
from app.services.transactions import TransactionService

router = APIRouter(prefix="/transactions")


@router.post("", response_model=TransactionResponse)
async def add_transaction(
        transaction_data: TransactionCreate,
        db: AsyncSession = Depends(get_db_master),
        user: User = Depends(get_current_user),
        redis: aioredis.Redis = Depends(get_redis),
):
    return await TransactionService.add_transaction(db, transaction_data, user.id, redis)


@router.get("", response_model=TransactionList)
async def list_transactions(
        params: TransactionListParams = Depends(),
        db: AsyncSession = Depends(get_db_replica),
        user: User = Depends(get_current_user)
):
    return await TransactionService.list_transactions(
        db, user.id, params.is_expense, params.category_id, params.year, params.month
    )


@router.put("/{id}", response_model=TransactionResponse)
async def edit_transaction(
        transaction_id: int,
        transaction_data: TransactionUpdate,
        db: AsyncSession = Depends(get_db_master),
        user: User = Depends(get_current_user),
        redis: aioredis.Redis = Depends(get_redis)
):
    return await TransactionService.edit_transaction(db, transaction_data, transaction_id, user.id, redis)


@router.delete("/{id}")
async def remove_transaction(
        transaction_id: int,
        db: AsyncSession = Depends(get_db_master),
        user: User = Depends(get_current_user),
        redis: aioredis.Redis = Depends(get_redis)
):
    await TransactionService.remove_transaction(db, transaction_id, user.id, redis)
