import redis.asyncio as aioredis

from app.core.config import settings

REDIS_URL = settings.REDIS_URL


async def get_redis():
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield redis
    finally:
        await redis.close()
