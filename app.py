from fastapi import FastAPI, status
import uvicorn
from fastapi.responses import RedirectResponse
from utils import generate_url
from base_models import URL

app = FastAPI()

@app.get("/{base62_url}")
def redirect_url(base62_url: str):
    # 1. check the database if such a URL exists
    # 2. get the "long" URL
    # 3. redirect if the URL exists
    exists = False
    if exists:
        return RedirectResponse("https://www.amazon.com", status_code=status.HTTP_303_SEE_OTHER) # address SHOULD contain "https" or "http"
    else:
        return status.HTTP_404_NOT_FOUND # URL not found

@app.post("/URL")
def add_url():
    pass


if __name__ == "__main__":
    uvicorn.run(app=app, port=8001) # run in port 8001 using uvicorn