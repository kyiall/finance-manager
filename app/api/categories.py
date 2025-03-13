from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_db
from app.crud.categories import create_category, get_categories, update_category
from app.models import User, Category
from app.schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from app.core.security import get_current_user

router = APIRouter()


@router.post("/categories/", response_model=CategoryResponse)
async def add_category(
        category_data: CategoryCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    user = (await db.scalars(
        select(User)
            .where(User.id == user.id)
            .options(selectinload(User.subscription))
    )).first()
    if not user.subscription or not user.subscription.is_active:
        filters = [
            Category.user_id == user.id,
            Category.is_active.is_(True)
        ]
        if category_data.is_expense:
            filters.append(Category.is_expense.is_(True))
            result = await db.execute(select(func.count()).where(*filters))
            if result.scalar_one() >= 10:
                raise HTTPException(
                    status_code=400, detail="Для добавления больше 10 категорий расходов оформите подписку"
                )
        filters.append(Category.is_expense.is_(False))
        result = await db.execute(select(func.count()).where(*filters))
        if result.scalar_one() >= 5:
            raise HTTPException(
                status_code=400, detail="Для добавления больше 5 категорий доходов оформите подписку"
            )
    return await create_category(db, category_data, user.id)


@router.get("/categories/", response_model=list[CategoryResponse])
async def list_categories(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await get_categories(db, user.id)


@router.put("/categories/{id}", response_model=CategoryResponse)
async def edit_category(
        category_id: int,
        category_data: CategoryUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await update_category(db, category_data, category_id, user.id)
