from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_db
from app.crud.subscriber_plans import create_subscriber_plan, get_subscriber_plans, update_subscriber_plan
from app.models import User
from app.schemas import SubscriberPlanResponse, SubscriberPlanCreate, SubscriberPlanUpdate
from app.security import get_current_user

router = APIRouter()


@router.post("/subscriber-plans/", response_model=SubscriberPlanResponse)
def add_subscriber_plan(
        subscriber_plan_data: SubscriberPlanCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return create_subscriber_plan(db, subscriber_plan_data)


@router.get("/subscriber-plans/", response_model=list[SubscriberPlanResponse])
def list_subscriber_plans(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_subscriber_plans(db)


@router.put("/subscriber-plan/{id}/", response_model=SubscriberPlanResponse)
def edit_subscriber_plan(
        subscriber_plan_id: int,
        subscriber_plan_data: SubscriberPlanUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return update_subscriber_plan(db, subscriber_plan_data, subscriber_plan_id)
