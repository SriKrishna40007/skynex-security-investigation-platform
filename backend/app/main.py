from fastapi import FastAPI

from app.api.v1.endpoints.health import router as health_router

app = FastAPI(
    title="Security Investigation Workspace",
    version="0.1.0",
)

app.include_router(health_router)