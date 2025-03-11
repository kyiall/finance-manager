from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import SubscriberPlan
from app.schemas import SubscriberPlanCreate, SubscriberPlanUpdate


def create_subscriber_plan(db: Session, subscriber_plan_data: SubscriberPlanCreate):
    db_subscriber_plan = SubscriberPlan(**subscriber_plan_data.dict())
    db.add(db_subscriber_plan)
    db.commit()
    db.refresh(db_subscriber_plan)
    return db_subscriber_plan


def get_subscriber_plans(db: Session):
    return db.query(SubscriberPlan).all()


def update_subscriber_plan(db: Session, subscriber_plan_data: SubscriberPlanUpdate, subscriber_plan_id: int):
    subscriber_plan = db.query(SubscriberPlan).filter(SubscriberPlan.id == subscriber_plan_id).first()
    if not subscriber_plan:
        raise HTTPException(status_code=404, detail="Subscriber plan не найден")
    for key, value in subscriber_plan_data.model_dump(exclude_unset=True).items():
        setattr(subscriber_plan, key, value)

    db.commit()
    db.refresh(subscriber_plan)
    return subscriber_plan
