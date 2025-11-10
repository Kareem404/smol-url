from fastapi import FastAPI, status, Request, Response
import uvicorn
from fastapi.responses import RedirectResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from utils import generate_url
from base_models import URL
from dotenv import load_dotenv
import os
from db import DB
from cache import check_cache, cache_url

load_dotenv() 
access_key = os.getenv('ACCESS_KEY')
secret_access_key = os.getenv('SECRET_ACCESS_KEY')

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# load database connectivity object
db = DB(access_key=access_key, secret_access_key=secret_access_key)

@app.get("/")
def welcome_message():
    return "Welcome to smol-url"

@app.get("/{short_url}")
@limiter.limit("10/minute")
def redirect_url(request: Request, response: Response, short_url: str):
    """
    Function that redirects the user given the short_url. Includes rate limiting logic in decarator to stop the same IP from sending more than 10 reqs per minute
    Args:-
        - request(Request): needed argument to allow rate limiting (does nothing else)
        - response(Response): needed argument since the returned response is not an instance of Response
        - short_url(str): the short_url itself
    """
    long_url = check_cache(shorturl=short_url) # None is returned if cache is not running or shorturl does not exist in cache
    if long_url is not None:
        print(f"cache hit: {long_url}")
        return RedirectResponse(long_url, status_code=status.HTTP_303_SEE_OTHER)
    else:
        long_url = db.get_long_url(short_url=short_url)
        if long_url == 404:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"error": "URL not found"}
            )
        else:
            cache_url(short_url=short_url, long_url=long_url) # cahce the url for fast access
            return RedirectResponse(long_url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/URL")
@limiter.limit("10/minute")
def add_url(request: Request, response: Response, url: URL):
    """
    Function that adds a long_url in the database with a short_url as key and caches it 
    Args:-
        - request(Request): needed argument to allow rate limiting (does nothing else)
        - response(Response): needed argument since the returned response is not an instance of Response
        - url(str): the long url 
    """
    url_dict = url.model_dump()
    short_url = db.add_long_url(long_url=url_dict['url']) # add the url to the database
    cache_url(short_url=short_url, long_url=url_dict['url'])
    return {"short_url": short_url} 

if __name__ == "__main__":
    uvicorn.run(app=app, port=8001) # run in port 8001 using uvicorn