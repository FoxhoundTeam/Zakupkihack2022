from typing import Type, cast

from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from starlette import status

from app.database import Base


def get_or_404(session: Session, model: Type[Base], _id: int, entity_name="Entity"):
    obj = session.query(model).get(_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} with such id doesn't exist",
        )
    return cast(type(model), obj)
