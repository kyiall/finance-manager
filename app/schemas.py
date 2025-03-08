from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class CategoryBase(BaseModel):
    title: str
    is_expense: bool


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    amount: float
    comment: str
    is_expense: bool
    category_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    category: CategoryResponse

    class Config:
        from_attributes = True


class SubscriberPlanBase(BaseModel):
    title: str
    days: int
    cost: float


class SubscriberPlanCreate(SubscriberPlanBase):
    pass


class SubscriberPlanResponse(SubscriberPlanBase):
    id: int

    class Config:
        from_attributes = True


class SubscriptionBase(BaseModel):
    is_active: bool
    active_until: datetime
    subscriber_plan_id: int


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionResponse(SubscriptionBase):
    id: int
    subscriber_plan: SubscriberPlanResponse

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    transactions: List[TransactionResponse] = []
    categories: List[CategoryResponse] = []
    subscription: Optional[SubscriptionResponse] = None

    class Config:
        from_attributes = True
