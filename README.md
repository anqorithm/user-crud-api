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
    subgraph Clients["Internet Clients"]
        Browser["Web Browser"]
        MobileApp["Mobile App"]
        ApiClients["API Clients"]
    end

    subgraph Gateway["API Gateway"]
        TLS["TLS Termination"]
    end

    subgraph FastAPI["FastAPI Application"]
        MW["Middleware<br/>CORS, Rate Limit<br/>Request ID, Logging"]
        
        subgraph Routes["API Routes"]
            Auth["/auth/*"]
            Users["/users/*"]
            Tasks["/tasks/*"]
            Files["/uploads/*"]
            WS["/ws/*"]
        end
        
        subgraph Services["Services"]
            AuthS["AuthService"]
            UserS["UserService"]
            TaskS["TaskService"]
            FileS["FileService"]
        end
        
        MW --> Routes --> Services
        Services --> Repo["Repository"]
        Services --> Cache["Cache"]
    end

    subgraph DataStore["Data Stores"]
        PG[("PostgreSQL")]
        RD[("Redis")]
        CB[("Celery")]
    end

    Clients --> TLS --> MW
    Repo --> PG
    Cache --> RD
    CB -.-> RD
```

### Request Flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant API as FastAPI
    participant MW as Middleware
    participant Svc as Services
    participant Repo as Repository
    participant PG as PostgreSQL
    participant Cache as Redis

    C->>API: POST /api/v1/auth/register
    Note over MW: CORS → Rate Limit → Request ID → Logging

    API->>MW: Validate Request
    MW->>Svc: user_data + session
    Svc->>Repo: Hash password

    Repo->>PG: INSERT user
    PG-->>Repo: user created
    Repo-->>Svc: user object

    Svc->>Cache: invalidate("users:list:*")
    Cache-->>Svc: OK

    Svc->>API: Token response
    API-->>C: 201 Created + JWT token

    Note over C: Use token for protected routes

    C->>API: GET /api/v1/users
    API->>MW: Validate Bearer Token
    MW->>Svc: token + session
    Svc->>Cache: get("users:list:1:100")
    
    alt Cache Hit
        Cache-->>Svc: cached data
    else Cache Miss
        Svc->>Repo: fetch users
        Repo->>PG: SELECT users
        PG-->>Repo: user list
        Repo-->>Svc: user list
        Svc->>Cache: setex("users:list:1:100", ttl)
    end

    Svc-->>API: paginated response
    API-->>C: 200 OK
```

### Database Schema

```mermaid
erDiagram
    USERS {
        uuid id PK "Primary Key"
        string name "Required"
        string email UK "Unique"
        int age "Optional"
        bool is_active "Default: true"
        bool is_superuser "Default: false"
        string hashed_password "Required"
        timestamp created_at "Auto"
        timestamp updated_at "Auto"
    }

    TASKS {
        uuid id PK "Primary Key"
        string title "Required"
        string description "Optional"
        int priority "1-5, Default: 1"
        bool completed "Default: false"
        uuid user_id FK "References Users"
        timestamp created_at "Auto"
        timestamp updated_at "Auto"
    }

    USERS ||--o{ TASKS : "creates"
```

### Caching Strategy

```mermaid
flowchart LR
    subgraph ReadOps["Read Operations"]
        A["GET /users<br/>/tasks/{id}"] --> B{Redis Cache}
        B -->|HIT| C["Return Cached"]
        B -->|MISS| D["Query PostgreSQL"]
        D --> E["Store in Redis<br/>TTL: 300s"]
        E --> C
    end

    subgraph WriteOps["Write Operations"]
        F["POST/PATCH/DELETE"] --> G["Write to PostgreSQL"]
        G --> H["Invalidate Cache"]
        H --> I["Return Response"]
    end
```

### Docker Architecture

```mermaid
graph TB
    subgraph Compose["Docker Compose"]
        subgraph Services["Services"]
            API["FastAPI<br/>:8000"]
            PG["PostgreSQL<br/>:5432"]
            RD["Redis<br/>:6379"]
        end
        
        API --> PG
        API --> RD
    end

    subgraph Clients["Clients"]
        Browser["Browser<br/>/docs"]
        Mobile["Mobile App"]
        Client["API Clients"]
    end

    Browser --> API
    Mobile --> API
    Client --> API
```

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- uv (recommended) or pip

### Local Development

```bash
# Clone the repository
git clone https://github.com/anqorithm/user-crud-api
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
│   └── routes/            # API endpoints
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
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | Register new user |
| `POST` | `/api/v1/auth/login` | Login and get tokens |

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

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html
```

## License

MIT License - see LICENSE file for details.

---

**Built with FastAPI, PostgreSQL, Redis**