from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.users import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    title = Column(String)
    is_expense = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="categories", lazy="selectin")
    transactions = relationship("Transaction", back_populates="category", lazy="selectin")
