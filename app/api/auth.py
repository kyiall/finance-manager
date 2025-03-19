import redis.asyncio as aioredis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.core.redis_conf import get_redis
from app.schemas import UserLogin, UserLoginResponse
from app.services.users import UserService

router = APIRouter()


@router.post("/login", response_model=UserLoginResponse)
async def login(user_data: UserLogin,
                db: AsyncSession = Depends(get_db),
                redis: aioredis.Redis = Depends(get_redis)):
    return await UserService.login(user_data, db, redis)


@router.post("/refresh")
async def refresh(refresh_token: str):
    return await UserService.refresh(refresh_token)
