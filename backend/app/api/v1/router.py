from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.iam import router as iam_router
from app.api.v1.endpoints.investigation import router as investigation_router
from app.api.v1.endpoints.terraform import router as terraform_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(iam_router)
api_router.include_router(terraform_router)
api_router.include_router(investigation_router)
api_router.include_router(auth_router)
