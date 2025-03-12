from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.utils import CustomError
from app.models import User, Subscription
from app.schemas import UserCreate, SubscriptionCreate, SubscriptionUpdate
from app.security import hash_password


async def get_user_by_email(db: AsyncSession, email: str):
    return (await db.scalars(select(User).where(User.email == email))).first()


def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_subscription(
        db: Session,
        subscription_data: SubscriptionCreate,
        user_id: int
):
    db_subscription = Subscription(**subscription_data.dict(), user_id=user_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def update_subscription(
        db: Session,
        subscription_data: SubscriptionUpdate,
        subscription_id,
        user_id: int
):
    subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
    if not subscription:
        raise CustomError(status_code=404, name="Подписка пользователя не найдена")
    if subscription.user_id != user_id:
        raise CustomError(status_code=403, name="Нет прав для редактирования данной подписки")
    for key, value in subscription_data.model_dump(exclude_unset=True).items():
        setattr(subscription, key, value)
    db.commit()
    db.refresh(subscription)
    return subscription
