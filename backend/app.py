from fastapi import FastAPI
from api.image_api import image_router
newsfeed_app = FastAPI()

newsfeed_app.include_router(image_router)

@newsfeed_app.get("/")
def home():
    return "HomePage......."

