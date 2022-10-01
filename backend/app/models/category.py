from typing import Optional

from pydantic import BaseModel

from app.database.tables import Statuses, Types


class CategoryFilter(BaseModel):
    label: str
    type: Types
    choices: Optional[list[str]]


class CategoryFilterWithID(CategoryFilter):
    id: Optional[int]


class CategoryFilterORM(CategoryFilterWithID):
    class Config:
        orm_mode = True


class BaseCategory(BaseModel):
    name: str


class BaseCategoryWithStatus(BaseCategory):
    status: Statuses


class CategoryCreate(BaseCategory):
    filters: list[CategoryFilter]


class CategoryUpdate(BaseCategoryWithStatus):
    filters: list[CategoryFilterWithID]
    pass


class CategoryChangeStatus(BaseModel):
    status: Statuses


class Category(BaseCategoryWithStatus):
    id: int
    filters: list[CategoryFilterORM]

    class Config:
        orm_mode = True
