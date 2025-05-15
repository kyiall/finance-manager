from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_master, get_db_replica
from app.core.security import check_user_role
from app.crud.subscriber_plans import create_subscriber_plan, get_subscriber_plans, update_subscriber_plan
from app.schemas.subscriber_plans import SubscriberPlanResponse, SubscriberPlanCreate, SubscriberPlanUpdate

router = APIRouter(prefix="/subscriber-plan", dependencies=[Depends(check_user_role)])


@router.post("", response_model=SubscriberPlanResponse)
async def add_subscriber_plan(
        subscriber_plan_data: SubscriberPlanCreate,
        db: AsyncSession = Depends(get_db_master),
):
    return await create_subscriber_plan(db, subscriber_plan_data)


@router.get("", response_model=list[SubscriberPlanResponse])
async def list_subscriber_plans(db: AsyncSession = Depends(get_db_replica)):
    return await get_subscriber_plans(db)


@router.put("/{id}", response_model=SubscriberPlanResponse)
async def edit_subscriber_plan(
        subscriber_plan_id: int,
        subscriber_plan_data: SubscriberPlanUpdate,
        db: AsyncSession = Depends(get_db_master),
):
    return await update_subscriber_plan(db, subscriber_plan_data, subscriber_plan_id)
