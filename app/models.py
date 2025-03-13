import enum

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship

from app.core.config import Base


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


class Transaction(BaseModel):
    __tablename__ = "transactions"

    amount = Column(Float)
    comment = Column(String)
    is_expense = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    category = relationship("Category", back_populates="transactions", lazy="selectin")
    owner = relationship("User", back_populates="transactions", lazy="selectin")


class Category(BaseModel):
    __tablename__ = "categories"

    title = Column(String)
    is_expense = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="categories", lazy="selectin")
    transactions = relationship("Transaction", back_populates="category", lazy="selectin")


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    is_active = Column(Boolean, default=False)
    active_until = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    subscriber_plan_id = Column(Integer, ForeignKey("subscriber_plans.id"))

    owner = relationship("User", back_populates="subscription", lazy="selectin")
    subscriber_plan = relationship("SubscriberPlan", back_populates="subscriptions", lazy="selectin")


class SubscriberPlan(BaseModel):
    __tablename__ = "subscriber_plans"

    title = Column(String)
    days = Column(Integer)
    cost = Column(Float)

    subscriptions = relationship("Subscription", back_populates="subscriber_plan", lazy="selectin")
