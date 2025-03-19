from pydantic import BaseModel


class CategoryBase(BaseModel):
    title: str
    is_expense: bool
    is_active: bool = True


class CategoryUpdate(BaseModel):
    title: str | None = None
    is_active: bool | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True
