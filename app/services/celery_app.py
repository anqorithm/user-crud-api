from datetime import datetime
from typing import Optional
from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.services.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)


@celery_app.task(name="send_email")
def send_email_task(to: str, subject: str, body: str):
    from app.services.email import send_email
    send_email(to=to, subject=subject, body=body)
    return {"status": "sent", "to": to}


@celery_app.task(name="cleanup_expired_cache")
def cleanup_expired_cache_task():
    import redis.asyncio as redis
    import asyncio

    async def cleanup():
        client = redis.from_url(settings.redis_url, decode_responses=True)
        keys = [k async for k in client.scan_iter(match="expired:*")]
        if keys:
            await client.delete(*keys)
        await client.close()

    asyncio.run(cleanup())
    return {"cleaned": len(keys)}


@celery_app.task(name="generate_report")
def generate_report_task(user_id: str, report_type: str):
    return {"user_id": user_id, "type": report_type, "generated_at": datetime.utcnow().isoformat()}