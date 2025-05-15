from pydantic import BaseModel


class SubscriberPlanBase(BaseModel):
    title: str
    days: int
    cost: float


class SubscriberPlanUpdate(BaseModel):
    title: str | None = None
    days: int | None = None
    cost: float | None = None


class SubscriberPlanCreate(SubscriberPlanBase):
    pass


class SubscriberPlanResponse(SubscriberPlanBase):
    id: int

    class Config:
        from_attributes = True
