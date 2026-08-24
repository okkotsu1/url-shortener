import redis

r = redis.Redis(host = "redis",decode_responses = True)

def get_cached_url(short_code):
    return r.get(short_code)

def set_cached_url(short_code, original_url):
    r.set(short_code, original_url, ex = 24 * 60 * 60)
