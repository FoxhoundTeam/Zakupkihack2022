from fastapi import APIRouter

from . import auth, category, companies, good

router = APIRouter(prefix="/api")
router.include_router(auth.router)
router.include_router(category.router)
router.include_router(companies.router)
router.include_router(good.router)
