from fastapi import APIRouter
from pydantic import BaseModel
from utils.sql_helper import ImageMetadataStoreHelper
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid

post_data_helper = ImageMetadataStoreHelper()

post_api_router = APIRouter(prefix="/v1/post")


@post_api_router.get("/{postId}")
def getPostData(postId):
    response = post_data_helper.getPostData(postId)
    return response