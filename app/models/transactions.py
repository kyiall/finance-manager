from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.users import BaseModel


class Transaction(BaseModel):
    __tablename__ = "transactions"

    amount = Column(Float)
    comment = Column(String)
    is_expense = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    category = relationship("Category", back_populates="transactions", lazy="selectin")
    owner = relationship("User", back_populates="transactions", lazy="selectin")
