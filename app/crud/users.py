from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.core.utils import CustomError
from app.models import User, Subscription
from app.schemas import UserCreate, SubscriptionCreate, SubscriptionUpdate


async def get_user_by_email(db: AsyncSession, email: str):
    return (await db.scalars(select(User).where(User.email == email))).first()


async def create_user(db: AsyncSession, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user, ["transactions", "categories", "subscription"])
    return db_user


async def create_subscription(
        db: AsyncSession,
        subscription_data: SubscriptionCreate,
        user_id: int
):
    db_subscription = Subscription(**subscription_data.dict(), user_id=user_id)
    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription, ["subscriber_plan"])
    return db_subscription


async def update_subscription(
        db: AsyncSession,
        subscription_data: SubscriptionUpdate,
        subscription_id,
        user_id: int
):
    subscription = (await db.scalars(select(Subscription).where(Subscription.id == subscription_id))).first()
    if not subscription:
        raise CustomError(status_code=404, name="Подписка пользователя не найдена")
    if subscription.user_id != user_id:
        raise CustomError(status_code=403, name="Нет прав для редактирования данной подписки")
    for key, value in subscription_data.model_dump(exclude_unset=True).items():
        setattr(subscription, key, value)
    await db.commit()
    await db.refresh(subscription)
    return subscription
