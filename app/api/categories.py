from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import create_category, get_categories
from app.database import get_db
from app.schemas import CategoryResponse, CategoryCreate

router = APIRouter()


@router.post("/categories/", response_model=CategoryResponse)
def add_category(category: CategoryCreate, user_id: int, db: Session = Depends(get_db)):
    return create_category(db, category, user_id)


@router.get("/categories/", response_model=list[CategoryResponse])
def list_categories(user_id: int, db: Session = Depends(get_db)):
    return get_categories(db, user_id)


