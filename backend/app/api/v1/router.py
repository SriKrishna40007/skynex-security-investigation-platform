from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.iam import router as iam_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(iam_router)