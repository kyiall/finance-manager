import redis.asyncio as aioredis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.redis_conf import get_redis
from app.core.security import get_current_user
from app.crud.balance import get_user_balance
from app.crud.users import create_subscription
from app.models.users import User
from app.schemas.users import UserResponse, UserCreate, SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from app.services.users import UserService

router = APIRouter()


@router.post("/register/", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService.register(user_data, db)


@router.post("/subscriptions/", response_model=SubscriptionResponse)
async def add_subscription(
        subscription_data: SubscriptionCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await create_subscription(db, subscription_data, user.id)


@router.put("/subscriptions/{id}", response_model=SubscriptionResponse)
async def edit_subscription(
        subscription_data: SubscriptionUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await UserService.edit_subscription(db, subscription_data, user.subscription.id, user.id)


@router.get("/get-balance/")
async def get_balance(user: User = Depends(get_current_user), redis: aioredis.Redis = Depends(get_redis)):
    return await get_user_balance(user.id, redis)
