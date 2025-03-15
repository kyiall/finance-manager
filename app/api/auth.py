import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.core.redis_conf import get_redis
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.crud.balance import get_balance
from app.crud.users import get_user_by_email
from app.schemas import UserResponse, UserLogin

router = APIRouter()


@router.post("/login", response_model=dict)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db), redis: aioredis.Redis = Depends(get_redis)):
    user = await get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    serialized_user_data = UserResponse.model_validate(user).model_dump()
    balance = await get_balance(user.id, redis)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_data": serialized_user_data,
        "balance": balance
    }


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token({"sub": user_id})
        return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
