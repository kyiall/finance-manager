from datetime import datetime
from typing import List

from pydantic import BaseModel, confloat

from app.schemas.categories import CategoryResponse


class TransactionBase(BaseModel):
    amount: confloat(gt=0)
    comment: str | None = None
    is_expense: bool
    category_id: int


class TransactionUpdate(BaseModel):
    amount: confloat(gt=0) | None = None
    comment: str | None = None
    category_id: int | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    category: CategoryResponse

    class Config:
        from_attributes = True


class TransactionList(BaseModel):
    transactions: List[TransactionResponse]
    total_amount: float


class TransactionListParams(BaseModel):
    is_expense: bool
    category_id: int | None = None
    year: int | None = datetime.now().year
    month: int | None = datetime.now().month
