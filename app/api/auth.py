from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import get_db
from app.crud.users import get_user_by_email
from app.models import Subscription
from app.schemas import UserCreate
from app.security import verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter()


@router.post("/login")
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    subscription = db.query(Subscription).filter(Subscription.user_id == user.id).first()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "subscription_id": subscription.id,
        "user_id": user.id
    }


@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = decode_token(refresh_token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_access_token({"sub": email})
        return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
