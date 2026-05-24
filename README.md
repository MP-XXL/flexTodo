# FlexTodo

A full-stack Todo application with a production-grade API and modern frontend, featuring both authenticated user todos and public guest todos.

## Overview

FlexTodo consists of two main components:
- **Backend API**: FastAPI-based REST API with PostgreSQL, JWT authentication, and comprehensive CRUD operations
- **Frontend**: Modern single-page application with vanilla JavaScript and TailwindCSS

### Features

| System | Access | Description |
|---|---|---|
| Authenticated User Todos | Register → Login → CRUD own todos | Private todos with JWT authentication, ownership enforcement |
| Guest Todos | Public read/write, no auth required | Public todos accessible without account creation |

## Tech Stack

### Backend
| Layer | Technology |
|---|---|
| Framework | FastAPI 0.111.0 |
| Database | PostgreSQL 16 (Docker) |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Authentication | JWT via python-jose |
| Password Hashing | bcrypt (passlib) |
| Validation | Pydantic v2 |
| Production Server | Gunicorn + Uvicorn workers |
| Containerization | Docker + docker-compose |

### Frontend
| Layer | Technology |
|---|---|
| Framework | Vanilla JavaScript |
| Styling | TailwindCSS 4.3.0 |
| Fonts | DM Sans, DM Mono (Google Fonts) |
| Architecture | Single-page application with tabbed interface |

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### 1. Clone and configure environment

```bash
git clone <repository-url>
cd flextodo
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

### 4. Verify the API

```bash
curl http://localhost:8000/health
# {"status":"ok","app":"flextodo"}
```

API documentation: http://localhost:8000/docs

### 5. Access the Frontend

Open `frontend/index.html` in your browser or serve it with a local web server:

```bash
# Using Python
cd frontend
python -m http.server 3000

# Or using Node.js http-server
npx http-server frontend -p 3000
```

Then visit: http://localhost:3000

---

## API Reference

**Base URL**: `http://localhost:8000`

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

### Health Check

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API health check |

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

### Create Guest Todo (public)

```bash
curl -X POST http://localhost:8000/api/v1/guest/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Public todo", "body": "Anyone can see this."}'
```

---

## Frontend Guide

The frontend is a single-page application built with vanilla JavaScript and TailwindCSS.

### Features
- **Authentication**: Login and register forms with JWT token management
- **User Todos**: Create, read, update, and delete personal todos
- **Guest Todos**: Public todo board accessible without authentication
- **Responsive Design**: Mobile-friendly interface with dark theme

### Frontend Structure
```
frontend/
├── index.html          # Main HTML structure
├── main.js             # JavaScript application logic
├── package.json        # TailwindCSS dependencies
└── src/
    ├── input.css       # TailwindCSS source
    └── output.css      # Compiled TailwindCSS
```

### Running the Frontend

**Option 1: Direct file access**
Simply open `frontend/index.html` in your browser.

**Option 2: Local web server (recommended)**
```bash
# Using Python
cd frontend
python -m http.server 3000

# Using Node.js
npx http-server frontend -p 3000
```

Then visit: http://localhost:3000

### Customizing TailwindCSS

To modify the styling:
1. Edit `frontend/src/input.css`
2. Compile the CSS:
```bash
cd frontend
npx tailwindcss -i ./src/input.css -o ./src/output.css
```

---

## Development Guide

### Local Development (without Docker)

For local development, you can run the backend directly:

**Prerequisites**
- Python 3.10+
- PostgreSQL 16
- pip

**Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your local database settings

# Run migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

```bash
# Docker environment
docker-compose exec api alembic upgrade head
docker-compose exec api alembic downgrade -1
docker-compose exec api alembic revision --autogenerate -m "describe_your_change"

# Local development
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "describe_your_change"
```

---

## Architecture

### Backend Architecture

The backend follows a layered architecture pattern:

```
┌─────────────────────────────────────────┐
│           API Routes Layer             │
│  (app/api/v1/routes/*.py)              │
│  - Request validation                  │
│  - Response formatting                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Services Layer                  │
│  (app/services/*.py)                   │
│  - Business logic                      │
│  - Ownership enforcement               │
│  - Data transformation                 │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Models Layer                   │
│  (app/models/*.py)                     │
│  - SQLAlchemy ORM models                │
│  - Database schema definition          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Database Layer                  │
│  (PostgreSQL)                            │
└─────────────────────────────────────────┘
```

**Key Components:**
- **Routes**: FastAPI route handlers that delegate to services
- **Services**: Business logic layer with ownership validation
- **Schemas**: Pydantic models for request/response validation
- **Dependencies**: Reusable FastAPI dependencies (auth, database)
- **Core**: Configuration, security helpers, custom exceptions

### Frontend Architecture

The frontend is a vanilla JavaScript single-page application:

```
┌─────────────────────────────────────────┐
│         UI Layer                        │
│  (index.html)                           │
│  - Tabbed interface                     │
│  - Forms and lists                      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Application Logic                  │
│  (main.js)                              │
│  - State management                     │
│  - API calls                            │
│  - DOM manipulation                     │
│  - JWT token storage                     │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Styling Layer                   │
│  (TailwindCSS)                          │
│  - Utility-first CSS                    │
│  - Dark theme                           │
└─────────────────────────────────────────┘
```

---

## Project Structure

```
flextodo/
├── app/                          # Backend application
│   ├── api/
│   │   └── v1/
│   │       ├── routes/
│   │       │   ├── auth.py          # Auth endpoints
│   │       │   ├── todos.py         # User todo CRUD
│   │       │   └── guest_todos.py   # Guest todo CRUD
│   │       └── __init__.py
│   ├── core/
│   │   ├── config.py                # Pydantic settings
│   │   ├── exceptions.py            # Custom HTTP exceptions
│   │   └── security.py             # JWT + bcrypt helpers
│   ├── db/
│   │   └── session.py              # SQLAlchemy engine + session
│   ├── dependencies/
│   │   └── auth.py                 # JWT validation dependency
│   ├── models/
│   │   ├── user.py                 # User ORM model
│   │   └── todo.py                 # Todo, GuestTodo models
│   ├── schemas/
│   │   ├── auth.py                 # Auth Pydantic schemas
│   │   └── todo.py                 # Todo Pydantic schemas
│   ├── services/
│   │   ├── auth_service.py         # Auth business logic
│   │   ├── todo_service.py         # Todo CRUD logic
│   │   └── guest_todo_service.py   # Guest todo logic
│   └── main.py                     # FastAPI app factory
├── frontend/                      # Frontend application
│   ├── index.html                  # Main HTML
│   ├── main.js                     # JavaScript logic
│   ├── package.json                # TailwindCSS deps
│   └── src/
│       ├── input.css               # Tailwind source
│       └── output.css              # Compiled CSS
├── alembic/                       # Database migrations
│   ├── versions/
│   │   └── 0001_initial_schema.py
│   └── env.py
├── alembic.ini                    # Alembic config
├── requirements.txt               # Python deps
├── Dockerfile                     # API Docker image
├── docker-compose.yml             # Multi-container setup
├── .env.example                   # Environment template
└── README.md                      # This file
```

---

## Environment Variables

### Application Variables

| Variable | Description | Default |
|---|---|---|
| `APP_ENV` | Application environment | `development` |
| `APP_NAME` | Application name | `flextodo` |
| `DATABASE_URL` | PostgreSQL connection string | — |
| `JWT_SECRET_KEY` | JWT signing secret — **change in production** | — |
| `JWT_ALGORITHM` | JWT signing algorithm | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime | `60` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `*` |

### Docker Compose Variables (not read by app)

| Variable | Description | Default |
|---|---|---|
| `POSTGRES_USER` | PostgreSQL username | — |
| `POSTGRES_PASSWORD` | PostgreSQL password | — |
| `POSTGRES_DB` | PostgreSQL database name | — |
| `POSTGRES_HOST` | PostgreSQL host | `db` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |

### Generating a Secure JWT Secret

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Security Notes

### Authentication & Authorization
- Passwords are hashed with **bcrypt** — never stored in plain text
- JWT tokens expire after **60 minutes** by default
- Users can **only access their own todos** — ownership enforced at service layer
- Invalid/expired tokens return `401 Unauthorized`
- Accessing another user's todo returns `403 Forbidden`
- Login error messages are intentionally vague to prevent email enumeration

### Production Security
- **Always change** `JWT_SECRET_KEY` in production
- Set `ALLOWED_ORIGINS` to your specific frontend domain(s)
- Use environment-specific `DATABASE_URL` (e.g., Supabase for production)
- The app runs as a **non-root user** inside the Docker container
- Database credentials are managed via environment variables

### CORS Configuration
- Development: `ALLOWED_ORIGINS=*` (allows all origins)
- Production: Set to specific frontend URL(s), e.g., `https://yourapp.vercel.app`

---

## Troubleshooting

### Database Connection Issues

**Problem**: API cannot connect to database

**Solutions**:
- Ensure Docker containers are running: `docker-compose ps`
- Check database health: `docker-compose exec db pg_isready -U flextodo_user`
- Verify `DATABASE_URL` in `.env` matches docker-compose settings
- Check PostgreSQL logs: `docker-compose logs db`

### Migration Errors

**Problem**: Alembic migration fails

**Solutions**:
- Ensure database is running: `docker-compose ps`
- Check current migration status: `docker-compose exec api alembic current`
- Reset database (WARNING: deletes data):
  ```bash
  docker-compose exec api alembic downgrade base
  docker-compose exec api alembic upgrade head
  ```

### JWT Token Issues

**Problem**: `401 Unauthorized` errors

**Solutions**:
- Verify `JWT_SECRET_KEY` is set in `.env`
- Check token hasn't expired (default 60 minutes)
- Ensure `Authorization` header format: `Bearer <token>`
- Regenerate secret if needed

### Frontend Issues

**Problem**: Frontend cannot connect to API

**Solutions**:
- Ensure API is running: `curl http://localhost:8000/health`
- Check CORS settings in `.env` (`ALLOWED_ORIGINS`)
- Verify API base URL in `frontend/main.js`
- Check browser console for CORS errors

### Docker Issues

**Problem**: Containers won't start

**Solutions**:
- Rebuild containers: `docker-compose up --build -d`
- Check logs: `docker-compose logs api db`
- Remove volumes and restart (WARNING: deletes data):
  ```bash
  docker-compose down -v
  docker-compose up --build -d
  ```

---

## Deployment

### Production Deployment Checklist

- [ ] Change `JWT_SECRET_KEY` to a strong random value
- [ ] Set `ALLOWED_ORIGINS` to production frontend URL
- [ ] Use production database (e.g., Supabase, RDS)
- [ ] Set `APP_ENV=production`
- [ ] Enable HTTPS
- [ ] Configure backup strategy for database
- [ ] Set up monitoring and logging
- [ ] Review and tighten CORS settings

### Deploying to Production

```bash
# Build and start production containers
docker-compose -f docker-compose.yml up -d

# Run migrations
docker-compose exec api alembic upgrade head

# Verify health
curl https://your-domain.com/health
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Write tests if applicable
5. Commit your changes: `git commit -am 'Add new feature'`
6. Push to the branch: `git push origin feature/my-feature`
7. Submit a pull request

---

## License

This project is provided as-is for educational and commercial use.
