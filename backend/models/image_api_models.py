from pydantic import BaseModel
from dataclasses import dataclass

class ImageUploadRequest(BaseModel):
    userId: str

@dataclass
class ImageUploadResponse:
    userId: str
    postId: str
    imageId: str
    createAt: str

@dataclass
class PostDataResponse:
    postId: str
    createAt: str