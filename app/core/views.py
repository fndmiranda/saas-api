from fastapi import APIRouter, status

from app.config import get_settings
from app.version import __version__

router = APIRouter()


@router.get("/", summary="Application root.", status_code=status.HTTP_200_OK)
async def root():
    settings = get_settings()
    return {"application": f"{settings.APP_NAME} - {__version__}"}


@router.get(
    "/health-check",
    summary="Application health check.",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def health_check():
    return {"status": "ok"}
