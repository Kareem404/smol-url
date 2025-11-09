import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cache_url(short_url: str, long_url: str) -> None:
    r.setex(name=short_url, value=long_url, time=3600) # expires in an hour
    print(f"added {short_url} to cache")

def check_cache(shorturl: str) -> None | str:
    return r.get(shorturl)

# docker run -t --name redis-container -p 6379:6379 redis:8.2.3