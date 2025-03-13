from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.core.security import get_current_user
from app.crud.subscriber_plans import create_subscriber_plan, get_subscriber_plans, update_subscriber_plan
from app.models import User
from app.schemas import SubscriberPlanResponse, SubscriberPlanCreate, SubscriberPlanUpdate

router = APIRouter()


@router.post("/subscriber-plans/", response_model=SubscriberPlanResponse)
async def add_subscriber_plan(
        subscriber_plan_data: SubscriberPlanCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await create_subscriber_plan(db, subscriber_plan_data)


@router.get("/subscriber-plans/", response_model=list[SubscriberPlanResponse])
async def list_subscriber_plans(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await get_subscriber_plans(db)


@router.put("/subscriber-plan/{id}/", response_model=SubscriberPlanResponse)
async def edit_subscriber_plan(
        subscriber_plan_id: int,
        subscriber_plan_data: SubscriberPlanUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await update_subscriber_plan(db, subscriber_plan_data, subscriber_plan_id)
