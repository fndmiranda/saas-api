import logging
from datetime import datetime

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.core.schemas import RootSchema
from app.version import __version__

logger = logging.getLogger(__name__)
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


@router.get(
    "/messages",
    summary="Show api messages.",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def show_message(
    *, request: Request, message: str = "message value", color: str = "dark"
):
    from app.main import templates

    logger.info(
        "Starting show message with={}".format(
            {
                "color": color,
                "message": message,
            }
        )
    )

    settings = get_settings()

    return templates.TemplateResponse(
        "show_message.html",
        {
            "request": request,
            "datetime": datetime,
            "color": color,
            "app_title": settings.APP_TITLE,
            "message": message,
        },
    )
