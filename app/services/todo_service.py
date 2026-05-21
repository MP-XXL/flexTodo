from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, NotFoundException
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreateRequest, TodoUpdateRequest


def create_todo(payload: TodoCreateRequest, current_user: User, db: Session) -> Todo:
    todo = Todo(
        user_id=current_user.id,
        title=payload.title.strip(),
        body=payload.body.strip(),
        status=payload.status,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_user_todos(current_user: User, db: Session) -> list[Todo]:
    return db.query(Todo).filter(Todo.user_id == current_user.id).all()


def _get_owned_todo(todo_id: int, current_user: User, db: Session) -> Todo:
    """
    Fetch a todo by id, enforcing ownership.

    - 404 if the todo does not exist.
    - 403 if the todo belongs to a different user.
    """
    todo = db.get(Todo, todo_id)
    if todo is None:
        raise NotFoundException("Todo not found.")
    if todo.user_id != current_user.id:
        raise ForbiddenException("You do not have permission to access this todo.")
    return todo


def update_todo(
    todo_id: int,
    payload: TodoUpdateRequest,
    current_user: User,
    db: Session,
) -> Todo:
    todo = _get_owned_todo(todo_id, current_user, db)

    if payload.title is not None:
        todo.title = payload.title.strip()
    if payload.body is not None:
        todo.body = payload.body.strip()
    if payload.status is not None:
        todo.status = payload.status

    # Explicitly set updated_at to guarantee timestamp update even if no column changed.
    todo.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(todo_id: int, current_user: User, db: Session) -> None:
    todo = _get_owned_todo(todo_id, current_user, db)
    db.delete(todo)
    db.commit()
