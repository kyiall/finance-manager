import redis.asyncio as aioredis
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.core.utils import CustomError
from app.crud.balance import get_user_balance
from app.crud.users import get_user_by_email, create_user, update_subscription, get_subscription
from app.schemas import UserCreate, SubscriptionUpdate, UserLogin


class UserService:
    @staticmethod
    async def register(user_data: UserCreate, db: AsyncSession):
        db_user = await get_user_by_email(db, user_data.email)
        if db_user:
            raise CustomError(status_code=400, name="Email already registered")
        return await create_user(db, user_data)

    @staticmethod
    async def edit_subscription(db: AsyncSession, subscription_data: SubscriptionUpdate, subscription_id, user_id):
        subscription = await get_subscription(db, subscription_id)
        if not subscription:
            raise CustomError(status_code=404, name="Подписка пользователя не найдена")
        return await update_subscription(db, subscription_data, subscription)

    @staticmethod
    async def login(user_data: UserLogin, db: AsyncSession, redis: aioredis.Redis):
        user = await get_user_by_email(db, user_data.email)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise CustomError(status_code=400, name="Invalid credentials")

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        balance = await get_user_balance(user.id, redis)
        return {"access_token": access_token, "refresh_token": refresh_token, "balance": balance, "user_data": user}

    @staticmethod
    async def refresh(refresh_token):
        try:
            payload = decode_token(refresh_token)
            user_id = payload.get("sub")
            if not user_id:
                raise CustomError(status_code=401, name="Invalid refresh token")

            new_access_token = create_access_token({"sub": user_id})
            return {"access_token": new_access_token, "refresh_token": refresh_token}
        except jwt.ExpiredSignatureError:
            raise CustomError(status_code=401, name="Refresh token expired")
        except jwt.JWTError:
            raise CustomError(status_code=401, name="Invalid refresh token")
