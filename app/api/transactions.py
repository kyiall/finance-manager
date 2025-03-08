from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import create_transaction, get_transactions
from app.database import get_db
from app.schemas import TransactionResponse, TransactionCreate

router = APIRouter()


@router.post("/transactions/", response_model=TransactionResponse)
def add_transaction(transaction: TransactionCreate, user_id: int, db: Session = Depends(get_db)):
    return create_transaction(db, transaction, user_id)


@router.get("/transactions/", response_model=list[TransactionResponse])
def list_transactions(user_id: int, db: Session = Depends(get_db)):
    return get_transactions(db, user_id)
