# app/auth/redis.py
try:
    import redis.asyncio as aioredis
except ImportError:
    aioredis = None

from app.core.config import get_settings

settings = get_settings()

async def get_redis():
    if aioredis is None:
        return None
    if not hasattr(get_redis, "redis"):
        get_redis.redis = await aioredis.from_url(
            settings.REDIS_URL or "redis://localhost"
        )
    return get_redis.redis

async def add_to_blacklist(jti: str, exp: int = 3600):
    redis = await get_redis()
    if redis is None:
        return
    await redis.set(f"blacklist:{jti}", "1", ex=exp)

async def is_blacklisted(jti: str) -> bool:
    redis = await get_redis()
    if redis is None:
        return False
    return await redis.exists(f"blacklist:{jti}")
