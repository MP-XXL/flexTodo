from sqlalchemy.orm import Session

from app.models.todo import GuestTodo
from app.schemas.todo import GuestTodoCreateRequest


def create_guest_todo(payload: GuestTodoCreateRequest, db: Session) -> GuestTodo:
    todo = GuestTodo(
        title=payload.title.strip(),
        body=payload.body.strip(),
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_all_guest_todos(db: Session) -> list[GuestTodo]:
    return db.query(GuestTodo).order_by(GuestTodo.created_at.desc()).all()
