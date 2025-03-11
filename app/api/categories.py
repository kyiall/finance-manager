from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.categories import create_category, get_categories, update_category
from app.database import get_db
from app.models import User, Category
from app.schemas import CategoryResponse, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.post("/categories/", response_model=CategoryResponse)
def add_category(category_date: CategoryCreate, user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user.subscription or not user.subscription.is_active:
        if category_date.is_expense:
            if db.query(Category).filter(
                Category.user_id == user.id,
                Category.is_expense.is_(True),
                Category.is_active.is_(True)
            ).count() >= 10:
                raise HTTPException(
                    status_code=400, detail="Для добавления больше 10 категорий расходов оформите подписку"
                )
        elif db.query(Category).filter(
            Category.user_id == user.id,
            Category.is_expense.is_(False),
            Category.is_active.is_(True)
        ).count() >= 5:
            raise HTTPException(
                status_code=400, detail="Для добавления больше 5 категорий доходов оформите подписку"
            )
    return create_category(db, category_date, user_id)


@router.get("/categories/", response_model=list[CategoryResponse])
def list_categories(user_id: int, db: Session = Depends(get_db)):
    return get_categories(db, user_id)


@router.put("/categories/{id}", response_model=CategoryResponse)
def edit_category(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    return update_category(db, category_data, category_id)
