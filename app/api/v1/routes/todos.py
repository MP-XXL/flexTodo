from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.todo import (
    TodoCreateRequest,
    TodoListResponse,
    TodoResponse,
    TodoUpdateRequest,
)
from app.services import todo_service

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a todo (authenticated users only)",
)
def create_todo(
    payload: TodoCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = todo_service.create_todo(payload, current_user, db)
    return TodoResponse.model_validate(todo)


@router.get(
    "",
    response_model=TodoListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all todos for the authenticated user",
)
def get_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todos = todo_service.get_user_todos(current_user, db)
    return TodoListResponse(
        todos=[TodoResponse.model_validate(t) for t in todos],
        total=len(todos),
    )


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a todo (owner only)",
)
def update_todo(
    todo_id: int,
    payload: TodoUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = todo_service.update_todo(todo_id, payload, current_user, db)
    return TodoResponse.model_validate(todo)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a todo (owner only)",
)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo_service.delete_todo(todo_id, current_user, db)
    return {"message": "Todo deleted successfully."}
