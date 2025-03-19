from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.security import get_current_user
from app.crud.categories import get_categories
from app.models.users import User
from app.schemas.categories import CategoryResponse, CategoryCreate, CategoryUpdate
from app.services.categories import CategoryService

router = APIRouter(prefix="/categories")


@router.post("", response_model=CategoryResponse)
async def add_category(
        category_data: CategoryCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await CategoryService.add_category(category_data, db, user)


@router.get("", response_model=list[CategoryResponse])
async def list_categories(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await get_categories(db, user.id)


@router.put("/{id}", response_model=CategoryResponse)
async def edit_category(
        category_id: int,
        category_data: CategoryUpdate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return await CategoryService.edit_category(db, category_data, category_id, user.id)
