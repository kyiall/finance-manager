from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.core.security import get_current_user
from app.crud.transactions import create_transaction, get_transactions, update_transaction
from app.models import User
from app.schemas import TransactionResponse, TransactionCreate, TransactionUpdate

router = APIRouter()


@router.post("/transactions/", response_model=TransactionResponse)
async def add_transaction(
        transaction_data: TransactionCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await create_transaction(db, transaction_data, user.id)


@router.get("/transactions/", response_model=dict)
async def list_transactions(
        is_expense: bool,
        category_id: int | None = None,
        year: int | None = None,
        month: int | None = None,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if not year or not month:
        now = datetime.now()
        year = now.year
        month = now.month
    transactions = await get_transactions(db, user.id, is_expense, category_id, year, month)
    serialized_transactions = [
        TransactionResponse.model_validate(transaction).model_dump() for transaction in transactions
    ]
    total_amount = sum(transaction["amount"] for transaction in serialized_transactions)
    return {"transactions": serialized_transactions, "total_amount": total_amount}


@router.put("/transactions/{id}", response_model=TransactionResponse)
async def edit_transaction(
        transaction_id: int,
        transaction_data: TransactionUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await update_transaction(db, transaction_data, transaction_id, user.id)
