from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import CustomError
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate


async def create_category(
        db: AsyncSession,
        category_data: CategoryCreate,
        user_id: int
):
    db_category = Category(**category_data.dict(), user_id=user_id)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_categories(db: AsyncSession, user_id: int):
    query = select(Category).where(Category.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()


async def update_category(
        db: AsyncSession,
        category_data: CategoryUpdate,
        category_id: int,
        user_id: int
):
    category = (await db.scalars(select(Category).where(Category.id == category_id))).first()
    if not category:
        raise CustomError(status_code=404, name="Категория не найдена")
    if category.user_id != user_id:
        raise CustomError(status_code=403, name="Нет прав для редактирования данной категории")
    for key, value in category_data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category
