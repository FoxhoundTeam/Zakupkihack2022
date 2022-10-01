from typing import Optional

from fastapi import HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import with_expression
from starlette import status

from app import database
from app.database.tables import Roles, Statuses
from app.services.base import BaseDBService


class UserService(BaseDBService):
    def get_companies(self) -> list[database.User]:
        return self.session.query(database.User).filter(database.User.role == Roles.company).all()

    def get_company_goods(self, company_id: int):
        query = (
            self.session.query(database.User)
            .filter(database.User.role == Roles.company)
            .filter(database.User.id == company_id)
        )
        company: database.User = query.first()
        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company with such id doesn't exist",
            )

        return (
            self.session.query(database.Good)
            .join(database.Good.users)
            .filter_by(user_id=company.id)
            .options(with_expression(database.Good.price, database.UsersGoods.price))
        )

    def search_companies(self, q: Optional[str], category_id: Optional[int]):
        query = self.session.query(database.User).filter(database.User.role == Roles.company)
        if q:
            query = query.filter(or_(database.User.username.contains(q), database.User.name.contains(q)))
        if category_id:
            query = (
                query.outerjoin(database.UserCategory, database.UserCategory.category_id == category_id)
                .outerjoin(database.UsersGoods)
                .outerjoin(
                    (
                        database.Good,
                        and_(
                            database.UsersGoods.good_id == database.Good.id,
                            database.Good.status == Statuses.approved,
                            database.Good.category_id == category_id,
                        ),
                    )
                )
                .filter(or_(database.Good.id != None, database.UserCategory.id != None))
            )
        return query

    def get_by_id(self, company_id: int) -> database.User:
        return self.session.query(database.User).get(company_id)
