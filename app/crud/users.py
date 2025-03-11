from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User, Subscription
from app.schemas import UserCreate, SubscriptionCreate, SubscriptionUpdate
from app.security import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_subscription(db: Session, subscription_data: SubscriptionCreate, user_id: int):
    db_subscription = Subscription(**subscription_data.dict(), user_id=user_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def update_subscription(db: Session, subscription_data: SubscriptionUpdate, subscription_id):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Подписка пользователя не найдена")
    for key, value in subscription_data.model_dump(exclude_unset=True).items():
        setattr(subscription, key, value)
    db.commit()
    db.refresh(subscription)
    return subscription
