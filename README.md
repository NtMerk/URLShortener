# FastAPI URL Shortener

Barebones URL Shortener made in Python using FastAPI and a locally hosted server using Redis.

## How it works

Generates a random string with length 5 and stores the link that is passed to it on the redis server as a key with value "**localhost:8000/xxxxx**" where the x are the randomly generated string.