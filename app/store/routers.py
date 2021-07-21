from fastapi import APIRouter

from app.store.views.segment import router as segment_router

router = APIRouter()

router.include_router(segment_router)
