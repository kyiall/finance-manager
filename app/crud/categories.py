from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate


def create_category(db: Session, category_data: CategoryCreate, user_id: int):
    db_category = Category(**category_data.dict(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()


def update_category(db: Session, category_data: CategoryUpdate, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    for key, value in category_data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category
