from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.users import User, Subscription
from app.schemas.users import UserCreate, SubscriptionCreate, SubscriptionUpdate


async def get_user_by_email(db: AsyncSession, email: str):
    return (await db.scalars(select(User).where(User.email == email))).first()


async def create_user(db: AsyncSession, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_subscription(
        db: AsyncSession,
        subscription_data: SubscriptionCreate,
        user_id: int
):
    db_subscription = Subscription(**subscription_data.dict(), user_id=user_id)
    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription)
    return db_subscription


async def get_subscription(db: AsyncSession, subscription_id: int):
    subscription = (await db.scalars(select(Subscription).where(Subscription.id == subscription_id))).first()
    return subscription


async def update_subscription(
        db: AsyncSession,
        subscription_data: SubscriptionUpdate,
        subscription: Subscription
):
    for key, value in subscription_data.model_dump(exclude_unset=True).items():
        setattr(subscription, key, value)
    await db.commit()
    await db.refresh(subscription)
    return subscription
