import logging

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_wtf import CSRFProtectMiddleware

from app.account.routers import router as account_router
from app.auth.views import router as oauth_router
from app.config import get_settings
from app.core.views import router as core_router
from app.store.routers import router as store_router
from app.version import __version__

logging.basicConfig(level=logging.INFO)

settings = get_settings()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=__version__,
    middleware=[
        Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY),
        Middleware(
            CSRFProtectMiddleware,
            csrf_secret=settings.CSRF_SECRET,
            enabled=not settings.TESTING,
        ),
    ],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

api_router = APIRouter()
api_router.include_router(core_router, tags=["core"])
api_router.include_router(account_router, prefix="/account", tags=["account"])
api_router.include_router(oauth_router, prefix="/oauth", tags=["oauth"])
api_router.include_router(store_router, prefix="/store", tags=["store"])
app.include_router(api_router)
