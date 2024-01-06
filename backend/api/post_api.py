from fastapi import APIRouter
from pydantic import BaseModel
from utils.sql_helper import ImageMetadataStoreHelper
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid

post_data_helper = ImageMetadataStoreHelper()

@dataclass
class PostDataResponse:
    postId: str
    createAt: str
    

class PostData(BaseModel):
    postData: str
    userId: str

post_api_router = APIRouter(prefix="/v1/post")

@post_api_router.post("/")
def postText(post_data:PostData):
    postid = str(uuid.uuid4())
    createdat = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    post_data_helper.putPostData(postid=postid,
                                 userid=post_data.userId,
                                 text=post_data.postData,
                                 createat=createdat)
    response = asdict(PostDataResponse(postid,createdat))
    return response

@post_api_router.get("/{postId}")
def getPostData(postId):
    response = post_data_helper.getPostData(postId)
    return response