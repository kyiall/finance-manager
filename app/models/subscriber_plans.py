from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.models.users import BaseModel


class SubscriberPlan(BaseModel):
    __tablename__ = "subscriber_plans"

    title = Column(String)
    days = Column(Integer)
    cost = Column(Float)

    subscriptions = relationship("Subscription", back_populates="subscriber_plan", lazy="selectin")
