from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from starlette import status as http_status

from app import models
from app.database.tables import Statuses
from app.models.good import PriceStat
from app.services.category import CategoryService
from app.services.good import GoodService

router = APIRouter(
    prefix="/good",
    tags=["good"],
)


@router.get("/list/", response_model=list[models.Good])
def get_goods_list(
    status: Optional[Statuses] = None,
    category_id: Optional[int] = None,
    good_service: GoodService = Depends(),
):
    return good_service.get_all(status, category_id)


@router.get("/", response_model=Page[models.Good])
def get_goods(
    request: Request,
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    status: Optional[Statuses] = None,
    good_service: GoodService = Depends(),
):
    return paginate(good_service.get_query(name, category_id, status, request))


@router.get("/stats/", response_model=PriceStat)
def get_goods_stats(
    category_id: int,
    name: Optional[str] = None,
    good_service: GoodService = Depends(),
):
    return good_service.get_price_stats(category_id, name)


@router.get("/categories/", response_model=list[models.Category])
def get_categories(
    name: str,
    category_service: CategoryService = Depends(),
):
    return category_service.get_categories_by_goods_name(name)


@router.post("/", response_model=models.Good, status_code=http_status.HTTP_201_CREATED)
def create_good(
    good_data: models.GoodCreate,
    good_service: GoodService = Depends(),
):
    return good_service.create_good(good_data)


@router.put("/{good_id}/")
def update_good(
    good_id: int,
    good_data: models.GoodUpdate,
    good_service: GoodService = Depends(),
):
    return good_service.update_good(good_id, good_data)


@router.get("/autocomplete/", response_model=list[str])
def autocomplete(
    q: str,
    good_service: GoodService = Depends(),
):
    return good_service.get_autocomplete_names(q)


@router.get("/{good_id}/", response_model=models.RetrieveGood)
def retrieve_good(
    good_id: int,
    good_service: GoodService = Depends(),
):
    return good_service.retrieve_good(good_id)


@router.patch("/{good_id}/change_status/", response_model=models.RetrieveGood)
def change_status(
    good_id: int,
    changed_data: models.GoodChangeStatus,
    good_service: GoodService = Depends(),
):
    return good_service.update_status(good_id, changed_data.status)


@router.post("/{good_id}/create_for_company/", status_code=http_status.HTTP_201_CREATED)
def link_company_and_good(
    good_id: int,
    user_link_data: models.GoodUser,
    good_service: GoodService = Depends(),
):
    good_service.link_with_user(good_id, user_link_data)
