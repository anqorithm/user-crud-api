# User CRUD API

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black)](https://github.com/features/actions)
[![Coverage](https://img.shields.io/badge/Coverage-73%25-yellow)](https://coverage.python.org/)

A production-ready FastAPI application with PostgreSQL, Redis, JWT authentication, background tasks, and more.

## Features

- **FastAPI** - Modern, high-performance web framework
- **PostgreSQL** - Robust relational database with async support
- **Redis** - Caching and session management
- **SQLModel** - ORM with type safety (SQLAlchemy + Pydantic)
- **JWT Authentication** - Secure token-based auth with refresh tokens
- **Celery** - Distributed task queue for background jobs
- **WebSocket** - Real-time bidirectional communication
- **Docker Compose** - Containerized development and deployment
- **Pytest** - Testing framework with async support
- **API Versioning** - `/api/v1/` prefix for clean API evolution

## Architecture Diagrams

### System Architecture

```mermaid
flowchart TB
    subgraph Clients
        A[🌐 Web Browser]
        B[📱 Mobile App]
        C[⌨️ CLI Tools]
        D[🔧 Other APIs]
        E[📖 Swagger UI]
    end

    subgraph FastAPI_Application
        subgraph API_Layer
            F[Auth Router<br/>/auth/*]
            G[Users Router<br/>/users/*]
            H[Tasks Router<br/>/tasks/*]
            I[Files Router<br/>/uploads/*]
        end

        subgraph Service_Layer
            F1[AuthService<br/>Register/Login/JWT]
            G1[UserService<br/>CRUD/Search/Page]
            H1[TaskService<br/>CRUD/Filter]
            I1[FileService<br/>Upload/Download]
        end

        subgraph Repository_Layer
            J[BaseRepository<br/>get/create/update/delete]
        end

        F --> F1
        G --> G1
        H --> H1
        I --> I1
        F1 --> J
        G1 --> J
        H1 --> J
        I1 --> J
    end

    subgraph Data_Layer
        K[(PostgreSQL<br/>Users, Tasks, Logs)]
        L[(Redis<br/>Cache, Sessions)]
        M[(Celery<br/>Task Queue)]
    end

    Clients --> FastAPI_Application
    J --> K
    J --> L
    M --> L
```

### Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant M as Middleware
    participant R as Router
    participant S as Service
    participant DB as PostgreSQL
    participant Cache as Redis

    C->>M: POST /api/v1/auth/register
    M->>M: CORS → Request ID → Rate Limit → Log
    M->>R: Request with dependencies
    R->>S: register(session, cache, user_data)
    S->>S: Hash password with bcrypt
    S->>DB: INSERT User
    DB-->>S: User created
    S->>S: Generate JWT token
    S->>Cache: Invalidate users:list:*
    Cache-->>S: Cache invalidated
    S-->>R: return Token
    R-->>M: Response
    M-->>C: HTTP 201 + X-Request-ID
```

### Data Model (ERD)

```mermaid
erDiagram
    USERS {
        string id PK ""
        string name ""
        string email UK ""
        int age ""
        bool is_active ""
        bool is_superuser ""
        string hashed_password ""
        datetime created_at ""
        datetime updated_at ""
    }

    TASKS {
        string id PK ""
        string title ""
        string description ""
        int priority ""
        bool completed ""
        string user_id FK ""
        datetime created_at ""
        datetime updated_at ""
    }

    USERS ||--o{ TASKS : "has"
```

### Caching Strategy

```mermaid
flowchart LR
    A[GET /users] --> B{Cache Hit?}
    B -->|Yes| C[Return cached data]
    B -->|No| D[Query PostgreSQL]
    D --> E[Store in Redis]
    E --> C
    F[POST /users] --> G[Write to PostgreSQL]
    G --> H[Invalidate cache]
```

### Docker Compose Architecture

```mermaid
flowchart TB
    A["API Service<br/>FastAPI :8000"]
    B["PostgreSQL<br/>:5432"]
    C["Redis<br/>:6379"]
    D[Browser]
    E[curl/Postman]
    F[Mobile App]

    D --> A
    E --> A
    F --> A
    A <--> B
    A <--> C
```

### API Versioning

```mermaid
flowchart LR
    V1["v1.0.0<br/>/api/v1"]
    V2["v2.0.0<br/>/api/v2"]
    V3["v3.0.0<br/>/api/v3"]

    V1 -->|deprecated| Old[Old Version]
    V2 -->|deprecated| Old
```

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- uv (recommended) or pip

### Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd user-crud-api

# Install dependencies with uv
uv sync

# Start infrastructure with Docker
docker compose up -d postgres redis

# Run the development server
uv run fastapi dev app/main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Using Docker (Full Stack)

```bash
# Build and start all services
docker compose up --build

# Stop all services
docker compose down

# Rebuild without cache
docker compose build --no-cache
```

## Project Structure

```
app/
├── main.py                 # Application entry point
├── core/                   # Core functionality
│   ├── config.py           # Settings & configuration
│   ├── exceptions.py       # Custom exceptions
│   ├── logging.py          # Logging setup (loguru)
│   ├── middleware.py       # Request ID, rate limiting
│   └── security.py        # JWT, password hashing
├── db/                     # Database layer
│   ├── redis.py            # Redis client & utilities
│   └── session.py          # SQLAlchemy async session
├── models/                 # ORM models
│   └── user_task.py        # User & Task models
├── schemas.py              # Pydantic schemas
├── repositories.py         # Repository pattern
├── api/v1/                 # API version 1
│   ├── router.py          # Main router
│   └── endpoints/         # API endpoints
│       ├── auth.py       # Authentication
│       ├── users.py      # User management
│       ├── tasks.py      # Task management
│       ├── files.py      # File uploads
│       └── websocket.py # WebSocket endpoints
├── services/               # Business logic
│   ├── celery_app.py     # Celery configuration
│   ├── email.py          # Email service
│   └── unit_of_work.py   # Unit of Work pattern
└── tests/                 # Test suite
    ├── unit/            # Unit tests
    └── integration/    # Integration tests
```

## Configuration

All configuration is managed through environment variables. Create a `.env` file:

```env
# Application
APP_NAME="User CRUD API"
APP_VERSION="1.0.0"
DEBUG=true
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/users_db

# Redis
REDIS_URL=redis://redis:6379

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# File Uploads
MAX_UPLOAD_SIZE_MB=10

# Email (optional)
EMAIL_ENABLED=false
SMTP_HOST=localhost
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=noreply@example.com

# Celery (optional)
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# Sentry (optional)
SENTRY_DSN=
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register new user |
| `POST` | `/api/v1/auth/login` | Login and get tokens |
| `POST` | `/api/v1/auth/refresh` | Refresh access token |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/users` | List all users |
| `GET` | `/api/v1/users/me` | Get current user |
| `GET` | `/api/v1/users/{id}` | Get user by ID |
| `POST` | `/api/v1/users` | Create new user |
| `PATCH` | `/api/v1/users/{id}` | Update user |
| `DELETE` | `/api/v1/users/{id}` | Delete user |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/tasks` | List tasks (paginated) |
| `GET` | `/api/v1/tasks/{id}` | Get task by ID |
| `POST` | `/api/v1/tasks` | Create new task |
| `PATCH` | `/api/v1/tasks/{id}` | Update task |
| `DELETE` | `/api/v1/tasks/{id}` | Delete task |

### Files

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/uploads` | Upload file |
| `GET` | `/api/v1/uploads/{filename}` | Download file |
| `DELETE` | `/api/v1/uploads/{filename}` | Delete file |

### WebSocket

| Endpoint | Description |
|----------|-------------|
| `WS /api/v1/ws/{user_id}` | Authenticated WebSocket |
| `WS /api/v1/ws` | Anonymous WebSocket |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/metrics` | Application metrics |

## Authentication

### Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "age": 30
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=securepassword123"
```

### Using the Token

```bash
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Pagination

### Query Parameters

```
GET /api/v1/users?page=1&page_size=10
GET /api/v1/tasks?page=2&page_size=20&completed=true&priority=3
```

### Response Format

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "pages": 10,
  "has_next": true,
  "has_prev": false
}
```

## Caching

Redis caching is enabled by default with a 5-minute TTL:

- User lists: `users:list:{page}:{page_size}`
- Individual users: `users:{user_id}`
- Task lists: `tasks:list:{page}:{page_size}:{filters}`

Cache is automatically invalidated on create, update, or delete operations.

## Background Tasks

Tasks are processed by Celery:

```python
from app.services.celery_app import celery_app

@celery_app.task(name="send_email")
def send_email_task(to: str, subject: str, body: str):
    # Send email asynchronously
    pass
```

Start the Celery worker:

```bash
celery -A app.services.celery_app worker --loglevel=info
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest app/tests/unit/test_api.py

# Run with verbose output
uv run pytest -v
```

## Development

### Code Quality

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy app/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "add users table"

# Apply migrations
alembic upgrade head
```

## Docker Services

| Service | Port | Description |
|---------|------|-------------|
| `api` | 8000 | FastAPI application |
| `postgres` | 5432 | PostgreSQL database |
| `redis` | 6379 | Redis cache |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | User CRUD API | Application name |
| `DATABASE_URL` | postgresql+asyncpg://... | Database connection URL |
| `REDIS_URL` | redis://redis:6379 | Redis connection URL |
| `JWT_SECRET_KEY` | (required) | Secret for JWT signing |
| `CACHE_TTL` | 300 | Cache TTL in seconds |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

- Documentation: `/docs`
- Issues: GitHub Issues
- Email: support@example.com

## Changelog

### v1.0.0 (2026-07-23)

- Initial release
- User CRUD with PostgreSQL
- JWT Authentication
- Redis caching
- Task management
- File uploads
- WebSocket support
- Background tasks with Celery
- Docker Compose setup

---

**Built with FastAPI, PostgreSQL, Redis, and ❤️**