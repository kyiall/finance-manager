from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.users import get_user_by_email, create_user, create_subscription, update_subscription, get_current_user
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserCreate, SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate

router = APIRouter()


@router.post("/register/", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user_data)


@router.post("/subscriptions/", response_model=SubscriptionResponse)
def add_subscription(subscription_data: SubscriptionCreate, user_id: int, db: Session = Depends(get_db)):
    return create_subscription(db, subscription_data, user_id)


@router.put("/subscriptions/{id}", response_model=SubscriptionResponse)
def edit_subscription(
        subscription_id: int,
        subscription_data: SubscriptionUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return update_subscription(db, subscription_data, subscription_id)
