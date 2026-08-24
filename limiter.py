import redis
import time

r = redis.Redis(host = "redis", decode_responses = True)

def is_rate_limited(ip):
    current_time = time.time()
    r.zremrangebyscore(ip, 0, current_time - 60)
    count = r.zcard(ip)
    if count >= 10:
        return True
    r.zadd(ip, {current_time: current_time})
    return False