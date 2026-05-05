from app.routers.auth import router as auth_router
from app.routers.jobs import router as jobs_router
from app.routers.predict import router as predict_router

__all__ = ["auth_router", "jobs_router", "predict_router"]
