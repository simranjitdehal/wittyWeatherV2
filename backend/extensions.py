import redis
import os

redis_client = redis.Redis(
    host= os.getenv('REDISHOST'),
    port=int(os.getenv('REDISPORT')),
    db=0,
    decode_responses=True  # auto-decode bytes to strings
)