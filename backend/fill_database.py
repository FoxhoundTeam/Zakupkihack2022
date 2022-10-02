import pandas as pd

from app.database import Category, Good, User, UserCategory, UsersGoods, CategoryFilter
from app.database.base import SessionLocal
from app.database.tables import Roles, Statuses
from app.services.category import CategoryService
from app.services.auth import AuthService
from app.services.good import GoodService
from app.models.auth import UserCreate
from app.services.user import UserService


def fill_database(categories_file, companies_file, products_file):
    categories = pd.read_csv(categories_file, delimiter=";", index_col=0)
    companies = pd.read_csv(companies_file, delimiter=";", index_col=0)
    products = pd.read_csv(products_file, delimiter=";", index_col=0).groupby("product_name").first().reset_index()

    with SessionLocal() as session:
        session.add_all(
            [
                User(username=company["inn"], name=company["name"], role=Roles.company, password_hash="")
                for _, company in companies.iterrows()
            ]
        )
        session.commit()
        session.add_all(
            [
                Category(name=category_name, status=Statuses.approved)
                for category_name in categories["okpd2_name"].unique()
            ]
        )
        session.commit()
        u_service = UserService(session)
        c_service = CategoryService(session)
        g_service = GoodService(session)
        companies = {company.username: company for company in u_service.get_companies()}
        categories = {category.name: category for category in c_service.get_all()}
        session.add_all(
            [
                Good(
                    name=good["product_name"],
                    description=good["product_characteristics"],
                    category_id=categories[good["okpd2_name"]].id,
                    status=Statuses.approved,
                )
                for _, good in products[["product_name", "product_characteristics", "okpd2_name"]]
                .drop_duplicates()
                .iterrows()
            ]
        )
        session.commit()

        goods = {(good.name, good.description, good.category_id): good for good in g_service.get_all(None, None)}

        session.add_all(
            [
                UserCategory(user_id=companies[product["inn"]].id, category_id=categories[product["okpd2_name"]].id)
                for _, product in products[["inn", "okpd2_name"]].drop_duplicates().iterrows()
            ]
        )
        session.add_all(
            [
                UsersGoods(
                    user_id=companies[product["inn"]].id,
                    price=product["price"],
                    good_id=goods[
                        (
                            product["product_name"],
                            product["product_characteristics"],
                            categories[product["okpd2_name"]].id,
                        )
                    ].id,
                )
                for _, product in products[["product_name", "product_characteristics", "okpd2_name", "inn", "price"]]
                .drop_duplicates()
                .iterrows()
            ]
        )
        session.commit()
        auth_service = AuthService(session)
        auth_service.register_new_user(UserCreate(username="admin", password="admin"))

        actions = []
        for good in goods.values():
            actions.append({"index": {"_id": good.id}})
            actions.append({"name": good.name, "complete_name": good.name, "description": good.description})

        step = int(len(actions) / 10)
        for i in range(10):
            part = actions[i * step : i * step + step]
            g_service.es.bulk(operations=part, index=g_service.index)

        g_service.es.indices.refresh(index=g_service.index)

