from fastapi import APIRouter

from app.account.views.account import router as account_router
from app.account.views.address import router as address_router
from app.account.views.password import router as password_router
from app.account.views.verified import router as verified_router

router = APIRouter()

router.include_router(account_router)
router.include_router(password_router)
router.include_router(verified_router)
router.include_router(address_router)
