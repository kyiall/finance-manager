from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import create_subscriber_plan, get_subscriber_plans
from app.database import get_db
from app.schemas import SubscriberPlanResponse, SubscriberPlanCreate

router = APIRouter()


@router.post("/subscriber-plans/", response_model=SubscriberPlanResponse)
def add_transaction(subscriber_plan: SubscriberPlanCreate, db: Session = Depends(get_db)):
    return create_subscriber_plan(db, subscriber_plan)


@router.get("/subscriber-plans/", response_model=list[SubscriberPlanResponse])
def list_transactions(db: Session = Depends(get_db)):
    return get_subscriber_plans(db)
