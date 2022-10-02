from fastapi import HTTPException
from sqlalchemy.orm.query import Query
from starlette import status

from app import database, models
from app.database.tables import Statuses
from app.services.base import BaseDBService
from app.services.goods_elasticserach_mixin import GoodsElasticsearchMixin


class CategoryService(BaseDBService, GoodsElasticsearchMixin):
    def create_category(self, category_data: models.CategoryCreate) -> database.Category:
        if (
            self.session.query(database.Category).filter(database.Category.name == category_data.name).first()
            is not None
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="This category already exist",
            )

        filters = category_data.filters
        category = database.Category(**category_data.dict(exclude={"filters"}))
        self.session.add(category)
        self.session.commit()

        for _filter in filters:
            category.filters.append(database.CategoryFilter(**_filter.dict()))
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def update_category(self, category_id: int, category_data: models.CategoryUpdate) -> database.Category:
        if self.session.query(database.Category).filter(database.Category.id == category_id).first() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category with such id doesn't exist",
            )
        category: database.Category = (
            self.session.query(database.Category).filter(database.Category.id == category_id).first()
        )
        self.session.bulk_update_mappings(
            database.CategoryFilter, [_filter.dict() for _filter in category_data.filters if _filter.id is not None]
        )
        self.session.bulk_insert_mappings(
            database.CategoryFilter,
            [{**_filter.dict(), "category_id": category_id} for _filter in category_data.filters if _filter.id is None],
        )
        self.session.query(database.Category).filter(database.Category.id == category_id).update(
            category_data.dict(exclude={"filters"})
        )
        self.session.commit()
        self.session.refresh(category)
        return category

    def get_all(self) -> list[database.Category]:
        return self.session.query(database.Category).all()

    def get_categories_by_goods_name(self, name: str) -> list:
        goods_query: Query = (
            self.session.query(database.Good.category_id)
            .filter(database.Good.id.in_(self.es_get_ids_by_q(name)))
            .distinct()
            .subquery()
        )
        return self.session.query(database.Category).filter(database.Category.id.in_(goods_query)).all()

    def update_status(self, category_id: int, new_status: Statuses):
        category: database.Category = self.session.query(database.Category).get(category_id)
        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Good with such id doesn't exist",
            )
        category.status = new_status
        self.session.commit()
        self.session.refresh(category)
        return category
