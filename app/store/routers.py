from fastapi import APIRouter

from app.store.views.address import router as address_router
from app.store.views.segment import router as segment_router
from app.store.views.store import router as store_router

router = APIRouter()

router.include_router(segment_router)
router.include_router(store_router)
router.include_router(address_router)
