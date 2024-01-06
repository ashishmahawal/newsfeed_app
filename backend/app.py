from fastapi import FastAPI
from api.image_api import image_router
from api.post_api import post_api_router

newsfeed_app = FastAPI()

newsfeed_app.include_router(image_router)
newsfeed_app.include_router(post_api_router)
@newsfeed_app.get("/")
def home():
    return "HomePage......."

