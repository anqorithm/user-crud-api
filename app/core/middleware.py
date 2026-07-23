import time
import uuid
import logging
from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.core.logging import log

request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request_id_ctx_var.set(request_id)
        request.state.request_id = request_id

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        log.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Time: {process_time:.3f}s"
        )
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.client_requests: dict = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_minute = int(time.time() / 60)

        key = f"{client_ip}:{current_minute}"
        self.client_requests[key] = self.client_requests.get(key, 0) + 1

        if self.client_requests[key] > self.requests_per_minute:
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={"X-RateLimit-Limit": str(self.requests_per_minute)}
            )

        self.client_requests = {
            k: v for k, v in self.client_requests.items()
            if k.endswith(str(current_minute))
        }

        return await call_next(request)


async def get_request_id() -> str:
    return request_id_ctx_var.get()


RequestID = get_request_id