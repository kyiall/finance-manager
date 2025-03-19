from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import CustomError
from app.models.subscriber_plans import SubscriberPlan
from app.schemas.subscriber_plans import SubscriberPlanCreate, SubscriberPlanUpdate


async def create_subscriber_plan(
        db: AsyncSession,
        subscriber_plan_data: SubscriberPlanCreate
):
    db_subscriber_plan = SubscriberPlan(**subscriber_plan_data.dict())
    db.add(db_subscriber_plan)
    await db.commit()
    await db.refresh(db_subscriber_plan)
    return db_subscriber_plan


async def get_subscriber_plans(db: AsyncSession):
    return (await db.scalars(select(SubscriberPlan))).all()


async def update_subscriber_plan(
        db: AsyncSession,
        subscriber_plan_data: SubscriberPlanUpdate,
        subscriber_plan_id: int
):
    subscriber_plan = (await db.scalars(select(SubscriberPlan).where(SubscriberPlan.id == subscriber_plan_id))).first()
    if not subscriber_plan:
        raise CustomError(status_code=404, name="Subscriber plan не найден")
    for key, value in subscriber_plan_data.model_dump(exclude_unset=True).items():
        setattr(subscriber_plan, key, value)

    await db.commit()
    await db.refresh(subscriber_plan)
    return subscriber_plan
