# FlexTodo API

A production-grade MVP Todo API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **JWT authentication**.

---

## Features

| System | Access |
|---|---|
| Authenticated User Todos | Register → Login → CRUD own todos |
| Guest Todos | Public read/write, no auth required |

---

## Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL 16 (Docker) |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Auth | JWT via python-jose |
| Password Hashing | bcrypt (passlib) |
| Validation | Pydantic v2 |
| Production Server | Gunicorn + Uvicorn workers |
| Containerization | Docker + docker-compose |

---

## Quick Start

### 1. Clone and configure environment

```bash
cp .env.example .env
# Edit .env and set a strong JWT_SECRET_KEY before deploying to production
```

### 2. Start services

```bash
docker-compose up --build -d
```

This starts:
- `db` — PostgreSQL 16 on port `5432`
- `api` — FlexTodo API on port `8000`

### 3. Run database migrations

```bash
docker-compose exec api alembic upgrade head
```

### 4. Verify

```bash
curl http://localhost:8000/health
# {"status":"ok","app":"flextodo"}
```

API docs: http://localhost:8000/docs

---

## API Reference

All routes are prefixed with `/api/v1`.

### Authentication

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | None | Register a new user |
| POST | `/api/v1/auth/login` | None | Login and receive JWT |

### User Todos (Protected)

All endpoints require `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/todos` | Create a todo |
| GET | `/api/v1/todos` | Get all your todos |
| PUT | `/api/v1/todos/{todo_id}` | Update your todo |
| DELETE | `/api/v1/todos/{todo_id}` | Delete your todo |

### Guest Todos (Public)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/guest/todos` | Create a public guest todo |
| GET | `/api/v1/guest/todos` | View all public guest todos |

---

## Example Requests

### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "password": "securepassword"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "ada@example.com", "password": "securepassword"}'
```

### Create Todo (authenticated)

```bash
curl -X POST http://localhost:8000/api/v1/todos \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Build something great", "body": "Start with the MVP."}'
```

---

## Migrations

```bash
# Apply all migrations
docker-compose exec api alembic upgrade head

# Rollback one step
docker-compose exec api alembic downgrade -1

# Generate a new migration after model changes
docker-compose exec api alembic revision --autogenerate -m "describe_your_change"
```

---

## Project Structure

```
flextodo/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── auth.py          # POST /auth/register, /auth/login
│   │       │   ├── todos.py         # CRUD /todos (protected)
│   │       │   └── guest_todos.py   # CRUD /guest/todos (public)
│   │       └── __init__.py          # v1 router aggregator
│   ├── core/
│   │   ├── config.py                # Pydantic settings (env vars)
│   │   ├── exceptions.py            # HTTP exception classes
│   │   └── security.py             # JWT + bcrypt helpers
│   ├── db/
│   │   └── session.py              # SQLAlchemy engine + session + get_db
│   ├── dependencies/
│   │   └── auth.py                 # get_current_user dependency
│   ├── models/
│   │   ├── user.py                 # User ORM model
│   │   └── todo.py                 # Todo, GuestTodo ORM models
│   ├── schemas/
│   │   ├── auth.py                 # Register/Login/Token Pydantic schemas
│   │   └── todo.py                 # Todo/GuestTodo Pydantic schemas
│   ├── services/
│   │   ├── auth_service.py         # Register + login logic
│   │   ├── todo_service.py         # Authenticated todo CRUD
│   │   └── guest_todo_service.py   # Guest todo CRUD
│   └── main.py                     # App factory + exception handlers
├── alembic/
│   ├── versions/
│   │   └── 0001_initial_schema.py  # Initial migration
│   └── env.py                      # Alembic environment config
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | Full PostgreSQL connection string | — |
| `JWT_SECRET_KEY` | Secret for signing JWTs — **change in production** | — |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes | `60` |
| `POSTGRES_USER` | PostgreSQL username | — |
| `POSTGRES_PASSWORD` | PostgreSQL password | — |
| `POSTGRES_DB` | PostgreSQL database name | — |

---

## Security Notes

- Passwords are hashed with **bcrypt** — never stored in plain text.
- JWT tokens expire after **60 minutes**.
- Users can **only access their own todos** — ownership is enforced at the service layer.
- Invalid/expired tokens return `401 Unauthorized`.
- Accessing another user's todo returns `403 Forbidden`.
- Error messages for login are intentionally vague to prevent email enumeration.
- The app runs as a **non-root user** inside the Docker container.
