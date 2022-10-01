from typing import Optional

from pydantic import BaseModel, constr

from app.database.tables import Statuses


class GoodFilterValue(BaseModel):
    category_filter_id: int
    value: str


class GoodFilterValueWithID(GoodFilterValue):
    id: Optional[int]


class GoodFilterValueORM(GoodFilterValueWithID):
    class Config:
        orm_mode = True


class BaseGood(BaseModel):
    name: constr(min_length=2)
    description: Optional[str] = None
    category_id: int


class GoodCreate(BaseGood):
    props: list[GoodFilterValue]


class GoodUpdate(BaseGood):
    status: Statuses
    props: list[GoodFilterValueWithID]


class Good(BaseGood):
    id: int
    props: list[GoodFilterValueORM]
    status: Statuses

    class Config:
        orm_mode = True


class GoodWithPrice(Good):
    price: Optional[float]


class GoodChangeStatus(BaseModel):
    status: Statuses


class GoodUser(BaseModel):
    user_id: int
    price: Optional[float]


class GoodUserORM(GoodUser):
    class Config:
        orm_mode = True


class RetrieveGood(Good):
    users: list[GoodUserORM]


class GoodSearchResult(BaseModel):
    name: str
    description: str
    url: str


class GoodSearchCompanyResult(BaseModel):
    name: str
    description: str
    url: str
