from fastapi import APIRouter, status

from app.config import get_settings
from app.core.schemas import RootSchema
from app.version import __version__

router = APIRouter()


@router.get(
    "/",
    summary="Application root.",
    status_code=status.HTTP_200_OK,
    response_model=RootSchema,
)
async def root():
    settings = get_settings()
    return {
        "application": settings.APP_NAME,
        "version": __version__,
    }


@router.get(
    "/health-check",
    summary="Application health check.",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def health_check():
    return {"status": "ok"}
