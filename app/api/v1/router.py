from fastapi import APIRouter
from app.api.v1.routes import auth_router, users_router, tasks_router, files_router
from app.api.v1.routes.websocket import ws_endpoint

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(tasks_router)
api_router.include_router(files_router)

api_router.add_api_websocket_route("/ws/{user_id}", ws_endpoint)

__all__ = ["api_router"]