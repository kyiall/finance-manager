import enum

from sqlalchemy import Column, Integer, DateTime, func, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default=UserRole.USER.value)

    transactions = relationship(
        "Transaction", back_populates="owner", passive_deletes=True, lazy="selectin"
    )
    categories = relationship(
        "Category", back_populates="owner", passive_deletes=True, lazy="selectin"
    )
    subscription = relationship(
        "Subscription", back_populates="owner", uselist=False, passive_deletes=True, lazy="selectin"
    )


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    is_active = Column(Boolean, default=False)
    active_until = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    subscriber_plan_id = Column(Integer, ForeignKey("subscriber_plans.id"))

    owner = relationship("User", back_populates="subscription", lazy="selectin")
    subscriber_plan = relationship("SubscriberPlan", back_populates="subscriptions", lazy="selectin")
