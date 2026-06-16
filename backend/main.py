import uvicorn
from fastapi import FastAPI

from .api.tweets import tweets_router
from .api.users import users_router
from .api.medias import medias_router

app = FastAPI()


app.include_router(tweets_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(medias_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
