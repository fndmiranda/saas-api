from fastapi import APIRouter, FastAPI

from app.account.views import router as account_router
from app.core.views import router as core_router
from app.oauth.views import router as oauth_router
from app.version import __version__

app = FastAPI(
    title="FastAPI",
    description="Project description",
    version=__version__,
)


api_router = APIRouter()
api_router.include_router(core_router, tags=["core"])
api_router.include_router(account_router, prefix="/account", tags=["accounts"])
api_router.include_router(oauth_router, prefix="/oauth", tags=["oauth"])
app.include_router(api_router)
