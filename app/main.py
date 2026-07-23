"""
FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.logging import log
from app.core.middleware import RequestIDMiddleware, RateLimitMiddleware
from app.core.exceptions import NotFoundException
from app.core.openapi import setup_openapi
from app.db import init_db, close_db, init_redis, close_redis
from app.api.v1.router import api_router

start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f"Starting {settings.app_name} v{settings.app_version}...")
    await init_db()
    await init_redis()
    yield
    await close_redis()
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-ready API with JWT auth, Redis caching, and task management",
    lifespan=lifespan,
)

setup_openapi(app)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

if settings.rate_limit_per_minute:
    app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.rate_limit_per_minute)


@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()})


app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    from app.db import redis_client
    redis_status = "healthy"
    try:
        if redis_client:
            await redis_client.ping()
    except Exception:
        redis_status = "unhealthy"
    return {
        "status": "healthy" if redis_status == "healthy" else "degraded",
        "version": settings.app_version,
        "uptime_seconds": round(time.time() - start_time, 2),
    }


@app.get("/", tags=["Root"])
async def root():
    return {"message": f"Welcome to {settings.app_name}", "version": settings.app_version, "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)