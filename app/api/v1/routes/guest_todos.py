from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.todo import (
    GuestTodoCreateRequest,
    GuestTodoListResponse,
    GuestTodoResponse,
)
from app.services import guest_todo_service

router = APIRouter(prefix="/guest/todos", tags=["Guest Todos"])


@router.post(
    "",
    response_model=GuestTodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a public guest todo (no authentication required)",
)
def create_guest_todo(
    payload: GuestTodoCreateRequest,
    db: Session = Depends(get_db),
):
    todo = guest_todo_service.create_guest_todo(payload, db)
    return GuestTodoResponse.model_validate(todo)


@router.get(
    "",
    response_model=GuestTodoListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all public guest todos (no authentication required)",
)
def get_guest_todos(db: Session = Depends(get_db)):
    todos = guest_todo_service.get_all_guest_todos(db)
    return GuestTodoListResponse(
        todos=[GuestTodoResponse.model_validate(t) for t in todos],
        total=len(todos),
    )
