import enum
from typing import Optional

from sqlalchemy import Column, Computed, Enum, Float, ForeignKey, Index, Integer, String, Text, TypeDecorator
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR
from sqlalchemy.orm import deferred, query_expression, relationship

from .base import Base


class Roles(str, enum.Enum):
    moderator = "moderator"
    company = "company"
    admin = "admin"


class UsersGoods(Base):
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    good_id = Column(ForeignKey("good.id"), primary_key=True)
    price = Column(Float, nullable=True)
    user = relationship("User", back_populates="goods")
    good = relationship("Good", back_populates="users")


class UserCategory(Base):
    user_id = Column(ForeignKey("user.id"), primary_key=True)
    category_id = Column(ForeignKey("category.id"), primary_key=True)

    user = relationship("User", back_populates="categories")
    category = relationship("Category", back_populates="users")


class User(Base):
    username: str = Column(String, nullable=True)
    password_hash: str = Column(String)
    role: Roles = Column(Enum(Roles))
    # additional
    address: Optional[str] = Column(String, nullable=True, default=None)
    name: Optional[str] = Column(String, nullable=True, default=None)
    phone: Optional[str] = Column(String, nullable=True, default=None)
    site: Optional[str] = Column(String, nullable=True, default=None)
    email: Optional[str] = Column(String, nullable=True, default=None)

    goods = relationship("UsersGoods", back_populates="user")
    categories: list[UserCategory] = relationship("UserCategory", back_populates="user")


class Statuses(str, enum.Enum):
    pending = "pending"
    need_modification = "need modification"
    declined = "declined"
    approved = "approved"


class Category(Base):
    name: str = Column(String, unique=True)
    status: Statuses = Column(Enum(Statuses), default=Statuses.pending, nullable=False)
    goods = relationship("Good", back_populates="category", lazy="select")
    filters: list["CategoryFilter"] = relationship(
        "CategoryFilter", back_populates="category", lazy="joined", join_depth=1
    )
    users = relationship("UserCategory", back_populates="category")


class TSVector(TypeDecorator):
    impl = TSVECTOR
    cache_ok = True


class Good(Base):
    name: str = Column(String, unique=True)
    status: Statuses = Column(Enum(Statuses), default=Statuses.pending)
    category_id: int = Column(Integer, ForeignKey("category.id"))
    description: Optional[str] = Column(Text, nullable=True, default=None)

    category = relationship("Category", back_populates="goods")
    users = relationship("UsersGoods", back_populates="good")
    props: list["GoodFilterValue"] = relationship("GoodFilterValue", back_populates="good", lazy="joined")

    __ts_vector__ = deferred(
        Column(TSVector(), Computed("to_tsvector('russian', name || ' ' || description)", persisted=True))
    )
    __table_args__ = (Index("ix_good___ts_vector__", __ts_vector__, postgresql_using="gist"),)

    price = query_expression()


class Types(str, enum.Enum):
    checkbox = "checkbox"
    radio = "radio"
    range = "range"


class CategoryFilter(Base):
    label = Column(String)
    type = Column(Enum(Types))
    category_id: int = Column(Integer, ForeignKey("category.id"), nullable=False)
    choices: list[str] = Column(ARRAY(String, dimensions=1), nullable=True, default=None)

    category = relationship("Category", back_populates="filters")
    filters = relationship("GoodFilterValue", back_populates="category_filter")


class GoodFilterValue(Base):
    category_filter_id = Column(Integer, ForeignKey("categoryfilter.id"), nullable=False)
    category_filter = relationship("CategoryFilter", back_populates="filters")
    good_id = Column(Integer, ForeignKey("good.id"), nullable=False)
    good = relationship("Good", back_populates="props")
    value = Column(String)
