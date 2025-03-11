from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from .database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    transactions = relationship("Transaction", back_populates="owner", passive_deletes=True)
    categories = relationship("Category", back_populates="owner", passive_deletes=True)
    subscription = relationship("Subscription", back_populates="owner", uselist=False, passive_deletes=True)


class Transaction(BaseModel):
    __tablename__ = "transactions"

    amount = Column(Float)
    comment = Column(String)
    is_expense = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    category = relationship("Category", back_populates="transactions")
    owner = relationship("User", back_populates="transactions")


class Category(BaseModel):
    __tablename__ = "categories"

    title = Column(String)
    is_expense = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    is_active = Column(Boolean, default=False)
    active_until = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    subscriber_plan_id = Column(Integer, ForeignKey("subscriber_plans.id"))

    owner = relationship("User", back_populates="subscription")
    subscriber_plan = relationship("SubscriberPlan", back_populates="subscriptions")


class SubscriberPlan(BaseModel):
    __tablename__ = "subscriber_plans"

    title = Column(String)
    days = Column(Integer)
    cost = Column(Float)

    subscriptions = relationship("Subscription", back_populates="subscriber_plan")
