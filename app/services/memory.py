import redis.asyncio as redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def get_chat_history(user_id: str) -> list[str]:
    key = f"chat_history:{user_id}"
    history = await r.lrange(key, 0, -1)
    return history

async def append_chat_history(user_id: str, message: str):
    key = f"chat_history:{user_id}"
    await r.rpush(key, message)
    await r.ltrim(key, -20, -1)  # keep last 20 messages
