from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    transactions = relationship("Transaction", back_populates="owner")
    categories = relationship("Category", back_populates="owner")
    subscriptions = relationship("Subscription", back_populates="owner")


class Transaction(BaseModel):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    comment = Column(String)
    is_expense = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category", back_populates="transactions")
    owner = relationship("User", back_populates="transactions")


class Category(BaseModel):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    is_expense = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="categories")


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=False)
    active_until = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    subscriber_plan_id = Column(Integer, ForeignKey("subscriber_plans.id"))

    owner = relationship("User", back_populates="subscriptions")
    subscriber_plan = relationship("SubscriberPlan", back_populates="subscriptions")


class SubscriberPlan(BaseModel):
    __tablename__ = "subscriber_plans"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    days = Column(Integer)
    cost = Column(Float)

    subscriptions = relationship("Subscription", back_populates="subscriber_plan")
