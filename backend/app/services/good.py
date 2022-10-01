import re
from collections import defaultdict
from typing import Optional

from fastapi import HTTPException, Request
from sqlalchemy import Integer, and_, cast, func, or_
from sqlalchemy.orm.query import Query
from starlette import status as http_status

from .. import database, models
from ..database.tables import Statuses, Types
from ..models.good import GoodFilterValue
from ..utils import get_or_404
from .base import BaseDBService


class GoodService(BaseDBService):
    def get_all(self, status: Optional[Statuses], category_id: Optional[int]) -> list[database.Good]:
        query = self.session.query(database.Good)
        if status:
            query = query.filter(database.Good.status == status)
        if category_id:
            query = query.filter(database.Good.category_id == category_id)
        return query.all()

    def _get_filtered_query(self, query: Query, request: Request) -> Query:
        category_filters: defaultdict[int, list[tuple[str, Optional[str]]]] = defaultdict(list)
        for key, value in request.query_params.items():
            match = re.match(r"filter_(\d+)_?(lte|gte)?", key)
            if match is None:
                continue
            category_filter_id = int(match.groups()[0])
            condition = match.groups()[1]
            category_filters[category_filter_id].append((value, condition))
        if not category_filters:
            return query
        mapping_id_to_type: dict[int, Types] = dict(
            self.session.query(database.CategoryFilter.id, database.CategoryFilter.type)
            .filter(database.CategoryFilter.id.in_(category_filters.keys()))
            .all()
        )
        good_filters_values_query = self.session.query(database.GoodFilterValue)
        conditions = []
        for k, val in category_filters.items():
            cur_conditions = []
            for v in val:
                if mapping_id_to_type[k] == Types.checkbox:
                    cur_conditions.append(database.GoodFilterValue.value.in_(v[0].split(",")))
                elif mapping_id_to_type[k] == Types.radio:
                    cur_conditions.append(database.GoodFilterValue.value == v[0])
                elif mapping_id_to_type[k] == Types.range:
                    if v[1] == "lte":
                        cur_conditions.append(
                            and_(
                                database.GoodFilterValue.category_filter_id == k,
                                cast(database.GoodFilterValue.value, Integer) <= int(v[0]),
                            )
                        )
                    elif v[1] == "gte":
                        cur_conditions.append(
                            and_(
                                database.GoodFilterValue.category_filter_id == k,
                                cast(database.GoodFilterValue.value, Integer) >= int(v[0]),
                            )
                        )
            if len(cur_conditions) > 1:
                conditions.append(and_(*cur_conditions))
            else:
                conditions.extend(cur_conditions)
        good_filters_values_query = good_filters_values_query.filter(or_(*conditions))
        good_ids = {
            *map(
                lambda t: t[0],
                good_filters_values_query.with_entities(database.GoodFilterValue.good_id)
                .having(func.count(database.GoodFilterValue.good_id) == len(category_filters))
                .group_by(database.GoodFilterValue.good_id),
            )
        }

        return query.filter(database.Good.id.in_(good_ids))

    def get_query(
        self,
        name: Optional[str],
        category_id: Optional[int],
        status: Optional[Statuses],
        request: Request,
    ):
        query: Query = self.session.query(database.Good)
        if request.query_params:
            query = self._get_filtered_query(query, request)
        if name:
            # query = query.filter(database.Good.name.ilike(f"%{name}%"))
            query = query.filter(database.Good.__ts_vector__.match(name, postgresql_regconfig="russian"))
        if category_id:
            query = query.filter(database.Good.category_id == category_id)
        if status:
            query = query.filter(database.Good.status == status)
        return query

    # def get_approved_query(self, name: Optional[str], category_id: Optional[int]):
    #     return self.get_query(name, category_id, Statuses.approved)

    def _update_category_filters(self, props: list[GoodFilterValue]):
        category_filters: list[database.CategoryFilter] = (
            self.session.query(database.CategoryFilter)
            .filter(database.CategoryFilter.id.in_(p.category_filter_id for p in props))
            .filter(database.CategoryFilter.type.in_([Types.checkbox, Types.radio]))
            .all()
        )
        mapping = defaultdict(list)
        for p in props:
            mapping[p.category_filter_id].append(p.value)
        for category_filter in category_filters:
            category_filter.choices = set(category_filter.choices).union(set(mapping[category_filter.id]))
        self.session.add_all(category_filters)
        self.session.commit()

    def create_good(self, good_data: models.GoodCreate) -> database.Good:
        good = database.Good(**good_data.dict(exclude={"props"}))
        self.session.add(good)
        self.session.commit()
        for prop in good_data.props:
            good.props.append(database.GoodFilterValue(**prop.dict()))
        self.session.add(good)
        self.session.commit()
        self._update_category_filters(good_data.props)
        self.session.refresh(good)
        return good

    def update_good(self, good_id: int, good_data: models.GoodUpdate) -> database.Good:
        if self.session.query(database.Good).filter(database.Good.id == good_id).first() is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Good with such id doesn't exist",
            )
        self.session.bulk_insert_mappings(
            database.GoodFilterValue,
            [{**prop.dict(), "good_id": good_id} for prop in good_data.props if prop.id is None],
        )
        self.session.bulk_update_mappings(
            database.GoodFilterValue, [prop.dict() for prop in good_data.props if prop.id is not None]
        )
        self.session.query(database.Good).filter(database.Good.id == good_id).update(good_data.dict(exclude={"props"}))
        self.session.commit()
        self._update_category_filters(good_data.props)
        return self.session.query(database.Good).filter(database.Good.id == good_id).first()

    def retrieve_good(self, good_id: int) -> database.Good:
        good = (
            self.session.query(database.Good).outerjoin(database.UsersGoods).filter(database.Good.id == good_id).first()
        )
        if good is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Good with such id doesn't exist",
            )
        return good

    def get_autocomplete_names(self, substr: str, limit: int = 10) -> list[str]:
        subquery = (
            self.session.query(func.regexp_split_to_table(database.Good.name, r"\s+").label("sub_name"))
            .filter(database.Good.status == Statuses.approved)
            .distinct()
            .subquery()
        )
        query = self.session.query(subquery).filter(subquery.c.sub_name.ilike(f"%{substr}%")).limit(limit).all()
        return [r[0] for r in query]

    def update_status(self, good_id: int, new_status: Statuses):
        good: database.Good = get_or_404(self.session, database.Good, good_id)
        good.status = new_status
        self.session.commit()
        self.session.refresh(good)
        return good

    def link_with_user(self, good_id: int, user_link_data: models.GoodUser):
        good: database.Good = get_or_404(self.session, database.Good, good_id)
        user: database.User = get_or_404(self.session, database.User, user_link_data.user_id)
        user_good: database.UsersGoods = (
            self.session.query(database.UsersGoods)
            .filter(database.UsersGoods.user_id == user.id)
            .filter(database.UsersGoods.good_id == good.id)
            .first()
        )
        if user_good is not None:
            user_good.price = user_link_data.price
        else:
            user_good = database.UsersGoods(good_id=good.id, user_id=user.id, price=user_link_data.price)
            self.session.add(user_good)
        self.session.commit()
