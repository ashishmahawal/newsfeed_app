from fastapi import FastAPI
from api.image_api import image_router
from api.post_api import post_api_router
from api.user_api import user_router
from fastapi.middleware.cors import CORSMiddleware
origins = [
   "*"
]

newsfeed_app = FastAPI()
newsfeed_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
newsfeed_app.include_router(image_router)
newsfeed_app.include_router(post_api_router)
newsfeed_app.include_router(user_router)
@newsfeed_app.get("/")
def home():
    return "HomePage......."

