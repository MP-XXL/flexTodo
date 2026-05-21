from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.todo import TodoStatus


# ---------------------------------------------------------------------------
# Authenticated Todo schemas
# ---------------------------------------------------------------------------

class TodoCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    body: str = Field(..., min_length=1)
    status: TodoStatus = TodoStatus.PENDING


class TodoUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    body: Optional[str] = Field(None, min_length=1)
    status: Optional[TodoStatus] = None


class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TodoListResponse(BaseModel):
    todos: list[TodoResponse]
    total: int


# ---------------------------------------------------------------------------
# Guest Todo schemas
# ---------------------------------------------------------------------------

class GuestTodoCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    body: str = Field(..., min_length=1)


class GuestTodoResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime

    model_config = {"from_attributes": True}


class GuestTodoListResponse(BaseModel):
    todos: list[GuestTodoResponse]
    total: int
