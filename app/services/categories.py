from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import CustomError
from app.crud.categories import create_category, count_categories, update_category, get_category
from app.models import User, Category
from app.schemas.categories import CategoryCreate, CategoryUpdate


class CategoryService:
    @staticmethod
    async def add_category(
            category_data: CategoryCreate,
            db: AsyncSession,
            user: User
    ):
        if not user.subscription or not user.subscription.is_active:
            filters = [
                Category.user_id == user.id,
                Category.is_active.is_(True)
            ]
            if category_data.is_expense:
                filters.append(Category.is_expense.is_(True))
                result = await count_categories(db, filters)
                if result >= 10:
                    raise CustomError(
                        status_code=400, name="Для добавления больше 10 категорий расходов оформите подписку"
                    )
            filters.append(Category.is_expense.is_(False))
            result = await count_categories(db, filters)
            if result >= 5:
                raise CustomError(
                    status_code=400, name="Для добавления больше 5 категорий доходов оформите подписку"
                )
        return await create_category(db, category_data, user.id)

    @staticmethod
    async def edit_category(
            db: AsyncSession,
            category_data: CategoryUpdate,
            category_id: int,
            user_id: int
    ):
        category = await get_category(db, category_id)
        if not category:
            raise CustomError(status_code=404, name="Категория не найдена")
        if category.user_id != user_id:
            raise CustomError(status_code=403, name="Нет прав для редактирования данной категории")
        return await update_category(db, category_data, category)
