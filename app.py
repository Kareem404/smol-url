from fastapi import FastAPI, status
import uvicorn
from fastapi.responses import RedirectResponse
from utils import generate_url
from base_models import URL
from dotenv import load_dotenv
import os
from db import DB

load_dotenv() 
access_key = os.getenv('ACCESS_KEY')
secret_access_key = os.getenv('SECRET_ACCESS_KEY')

app = FastAPI()

# load database connectivity object
db = DB(access_key=access_key, secret_access_key=secret_access_key)

@app.get("/")
def welcome_message():
    return "Welcome to smol-url"


@app.get("/{short_url}")
def redirect_url(short_url: str):
    long_url = db.get_long_url(short_url=short_url)
    if long_url == 404:
        return status.HTTP_404_NOT_FOUND
    else:
        return RedirectResponse(long_url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/URL")
def add_url(url: URL):
    url_dict = url.model_dump()
    short_url = db.add_long_url(long_url=url_dict['url']) # add the url to the database
    return {"short_url": short_url} 

if __name__ == "__main__":
    uvicorn.run(app=app, port=8001) # run in port 8001 using uvicorn