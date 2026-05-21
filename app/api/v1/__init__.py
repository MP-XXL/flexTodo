from fastapi import APIRouter

from app.api.v1.routes import auth, guest_todos, todos

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(todos.router)
router.include_router(guest_todos.router)
