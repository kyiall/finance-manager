from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import create_user, create_subscription, get_user_by_email
from app.database import get_db
from app.schemas import UserResponse, UserCreate, SubscriptionCreate, SubscriptionResponse

router = APIRouter()


@router.post("/register/", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)


@router.post("/subscriptions/", response_model=SubscriptionResponse)
def add_subscription(subscription: SubscriptionCreate, user_id: int, db: Session = Depends(get_db)):
    return create_subscription(db, subscription, user_id)
