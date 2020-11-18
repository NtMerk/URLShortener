import random
import string
from redis import Redis
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import RedirectResponse

app = FastAPI()
r = Redis()

class Link(BaseModel):
    url: str

# Generate a random string with length 5
def random_string():
    all_codes = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(all_codes) for i in range(5))
    return result_str

@app.get("/")
async def root():
    return {"message": "This is a basic URL shortener uwu"}

# A URL is passed as data on the body, and stored in the redis server with a shortened version
@app.post("/")
async def shorten_url(link: Link):
    url = link.url
    if r.get(url) == None:
        shortened_url = random_string()
        if r.mset({url: shortened_url}):
            return {"url": url, "shortened": "localhost:8000/" + r.get(url).decode("utf8")}
        else:
            return {"message": "Shorten failed"}

    return {"message", "This URL already exists", "localhost:8000/" + r.get(url).decode("utf8")}

# Keys must be decoded since they're binary encoded
@app.get("/get")
async def get_urls():
    data = []
    for key in r.keys():
        data.append({key.decode("utf8"): r.get(key).decode("utf8")})

    return data

# Redirect to our saved URLs from the shortened ones
@app.get("/{shortened}")
async def redirect_to_url(shortened: str):
    for key in r.keys():
        if r.get(key).decode("utf8") == shortened:
            return RedirectResponse(url=key.decode("utf8"))

    return {"message": "URL not defined"}
