from enum import Enum

from pydantic import BaseModel, EmailStr, confloat, field_validator
from datetime import datetime
from typing import List, Optional

# from app.core.utils import CustomError


class CategoryBase(BaseModel):
    title: str
    is_expense: bool
    is_active: bool = True


class CategoryUpdate(BaseModel):
    title: str | None = None
    is_active: bool | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class TransactionBase(BaseModel):
    amount: confloat(gt=0)
    comment: str | None = None
    is_expense: bool
    category_id: int

    # @field_validator('amount', mode='before')
    # def validate_name(cls, value):
    #     if value <= 0:
    #         raise CustomError(status_code=400, name="Сумма должна быть больше 0")
    #     return value


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


class SubscriberPlanBase(BaseModel):
    title: str
    days: int
    cost: float


class SubscriberPlanUpdate(BaseModel):
    title: str | None = None
    days: int | None = None
    cost: float | None = None


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


class SubscriptionUpdate(BaseModel):
    subscriber_plan_id: int


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionResponse(SubscriptionBase):
    id: int
    subscriber_plan: SubscriberPlanResponse

    class Config:
        from_attributes = True


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    transactions: List[TransactionResponse] = []
    categories: List[CategoryResponse] = []
    subscription: Optional[SubscriptionResponse] = None

    class Config:
        from_attributes = True
