import redis.asyncio as redis
from app.core.config import settings

redis_client: redis.Redis | None = None


async def init_redis() -> redis.Redis:
    global redis_client
    redis_client = redis.from_url(settings.redis_url, decode_responses=True, max_connections=10)
    await redis_client.ping()
    return redis_client


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None


async def get_redis() -> redis.Redis:
    if redis_client is None:
        await init_redis()
    return redis_client


async def invalidate_cache(pattern: str = "users:*"):
    client = await get_redis()
    keys = [key async for key in client.scan_iter(match=pattern)]
    if keys:
        await client.delete(*keys)