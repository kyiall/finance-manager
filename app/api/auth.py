from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.crud.users import get_user_by_email
from app.schemas import UserCreate
from app.security import verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter()


@router.post("/login")
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
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
