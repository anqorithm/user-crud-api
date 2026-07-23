"""
OpenAPI Configuration for Swagger Documentation
"""
from fastapi import FastAPI
from app.core.config import settings

TAGS_METADATA = [
    {"name": "Authentication", "description": "JWT auth endpoints"},
    {"name": "Users", "description": "User CRUD operations"},
    {"name": "Tasks", "description": "Task management with caching"},
    {"name": "Files", "description": "File upload/download"},
    {"name": "WebSocket", "description": "Real-time messaging"},
    {"name": "Health", "description": "Service health check"},
]


def setup_openapi(app: FastAPI):
    """Configure OpenAPI schema with HTTP method visibility"""
    app.title = settings.app_name
    app.version = settings.app_version
    app.description = """
## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | Register new user |
| POST | /api/v1/auth/login | Login and get token |
| GET | /api/v1/users | List all users |
| GET | /api/v1/users/{id} | Get user by ID |
| POST | /api/v1/users | Create user |
| PATCH | /api/v1/users/{id} | Update user |
| DELETE | /api/v1/users/{id} | Delete user |
| GET | /api/v1/tasks | List tasks |
| GET | /api/v1/tasks/{id} | Get task |
| POST | /api/v1/tasks | Create task |
| PATCH | /api/v1/tasks/{id} | Update task |
| DELETE | /api/v1/tasks/{id} | Delete task |
| POST | /api/v1/uploads | Upload file |
| WS | /api/v1/ws/{user_id} | WebSocket |

## Auth

Use `Authorization: Bearer <token>` header for protected routes.
"""
    app.tags_metadata = TAGS_METADATA
    return app