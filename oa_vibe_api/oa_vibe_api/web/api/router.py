from fastapi.routing import APIRouter

from oa_vibe_api.web.api import monitoring
from oa_vibe_api.web.api.system import router as system_router
from oa_vibe_api.web.api.oa import router as oa_router

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(system_router.router, prefix="/system", tags=["system"])
api_router.include_router(oa_router.router, prefix="/oa", tags=["oa"])
