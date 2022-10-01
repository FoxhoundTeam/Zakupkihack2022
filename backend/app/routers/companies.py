from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app import models
from app.services.user import UserService

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.get("/", response_model=list[models.User])
def get_companies(user_service: UserService = Depends()):
    return user_service.get_companies()


@router.get("/search/", response_model=Page[models.User])
def search_companies(q: Optional[str] = None, category_id: Optional[int] = None, user_service: UserService = Depends()):
    return paginate(user_service.search_companies(q, category_id))


@router.get("/{company_id}/", response_model=models.User)
def get_company(company_id: int, user_service: UserService = Depends()):
    return user_service.get_by_id(company_id)


@router.get("/{company_id}/goods/", response_model=Page[models.GoodWithPrice])
def get_company_goods(company_id: int, user_service: UserService = Depends()):
    return paginate(user_service.get_company_goods(company_id))
