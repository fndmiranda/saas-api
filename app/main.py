import logging

from fastapi import APIRouter, FastAPI

from app.account.views import router as account_router
from app.core.views import router as core_router
from app.oauth.views import router as oauth_router
from app.store.routers import router as store_router
from app.version import __version__

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="PapitoPet API",
    description="Core api of the PapitoPet",
    version=__version__,
)


api_router = APIRouter()
api_router.include_router(core_router, tags=["core"])
api_router.include_router(account_router, prefix="/account", tags=["account"])
api_router.include_router(oauth_router, prefix="/oauth", tags=["oauth"])
api_router.include_router(store_router, prefix="/store", tags=["store"])
app.include_router(api_router)
