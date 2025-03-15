import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.core.redis_conf import get_redis
from app.core.security import get_current_user
from app.crud.users import get_user_by_email, create_user, create_subscription, update_subscription
from app.models import User
from app.schemas import UserResponse, UserCreate, SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate

router = APIRouter()


@router.post("/register/", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user(db, user_data)


@router.post("/subscriptions/", response_model=SubscriptionResponse)
async def add_subscription(
        subscription_data: SubscriptionCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await create_subscription(db, subscription_data, user.id)


@router.put("/subscriptions/{id}", response_model=SubscriptionResponse)
async def edit_subscription(
        subscription_id: int,
        subscription_data: SubscriptionUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await update_subscription(db, subscription_data, subscription_id, user.id)


@router.get("/get-balance/")
async def get_balance(user: User = Depends(get_current_user), redis: aioredis.Redis = Depends(get_redis)):
    balance = await redis.get(user.id)
    return balance if balance else 0
