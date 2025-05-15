from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from app.schemas.subscriber_plans import SubscriberPlanResponse

from app.schemas.transactions import TransactionResponse

from app.schemas.categories import CategoryResponse


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


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    balance: float
    user_data: UserResponse
