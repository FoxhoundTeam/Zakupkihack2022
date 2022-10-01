from fastapi import APIRouter, Depends, status

from app import models
from app.services.category import CategoryService

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.post("/", response_model=models.Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: models.CategoryCreate,
    category_service: CategoryService = Depends(),
):
    return category_service.create_category(category_data)


@router.put("/{category_id}/", response_model=models.Category, status_code=status.HTTP_200_OK)
def update_category(
    category_id: int,
    category_data: models.CategoryUpdate,
    category_service: CategoryService = Depends(),
):
    return category_service.update_category(category_id, category_data)


@router.get("/", response_model=list[models.Category])
def get_categories(
    category_service: CategoryService = Depends(),
):
    return category_service.get_all()


@router.patch("/{category_id}/change_status/", response_model=models.Category)
def change_status(
    category_id: int,
    changed_data: models.CategoryChangeStatus,
    category_service: CategoryService = Depends(),
):
    return category_service.update_status(category_id, changed_data.status)
