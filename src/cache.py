import redis

r = redis.Redis(host='172.17.0.1', port=6379, decode_responses=True)
# 172.17.0.1 is the default IP address assigned to the docker0 bridge interface within the host machine's network

def cache_url(short_url: str, long_url: str) -> None:
    """
    Function that caches the short url for faster retreival
    Args:
        - short_url(str): the generated URL from the system
        - long_url(str): the URL that the user wants to route to
    Returns:
        - None
    """
    try:
        r.setex(name=short_url, value=long_url, time=3600) # expires in an hour
        print(f"added {short_url} to cache")
    except Exception as e:
        print("unable to cache")

def check_cache(shorturl: str) -> None | str:
    """
    Function that caches the short url for faster retreival
    Args:
        - short_url(str): the generated URL from the system
    Returns:
        - None (if URL is not cached)
        - str (string representing the long_url)
    """
    try:
        return r.get(shorturl)
    except Exception as e:
        return None 

# docker run -t --name redis-container -p 6379:6379 redis:8.2.3
# docker start -t redis-container