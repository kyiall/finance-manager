from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.transactions import create_transaction, get_transactions, update_transaction
from app.database import get_db
from app.schemas import TransactionResponse, TransactionCreate, TransactionUpdate

router = APIRouter()


@router.post("/transactions/", response_model=TransactionResponse)
def add_transaction(transaction_data: TransactionCreate, user_id: int, db: Session = Depends(get_db)):
    return create_transaction(db, transaction_data, user_id)


@router.get("/transactions/", response_model=dict)
def list_transactions(user_id: int, is_expense: bool, category_id: int, db: Session = Depends(get_db)):
    transactions = get_transactions(db, user_id, is_expense, category_id)
    serialized_transactions = [
        TransactionResponse.model_validate(transaction).model_dump() for transaction in transactions
    ]
    total_amount = sum(transaction["amount"] for transaction in serialized_transactions)
    return {"transactions": serialized_transactions, "total_amount": total_amount}


@router.put("/transactions/{id}", response_model=TransactionResponse)
def edit_transaction(transaction_id: int, transaction_data: TransactionUpdate, db: Session = Depends(get_db)):
    return update_transaction(db, transaction_data, transaction_id)
