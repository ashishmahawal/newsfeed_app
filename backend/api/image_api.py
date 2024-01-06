from fastapi import APIRouter, UploadFile, Request, Response, Form, File
from utils.image_datastore_utils import ImageDataStoreUtils
from utils.sql_helper import ImageMetadataStoreHelper
from models.image_api_models import ImageUploadRequest, ImageUploadResponse
from datetime import datetime
from dataclasses import asdict
import uuid

image_router = APIRouter(prefix="/v1/image")

image_store_util = ImageDataStoreUtils(env="local")
image_metadata_store_helper = ImageMetadataStoreHelper()

@image_router.post("/upload")
async def image_upload(request:Request,
                       file: UploadFile = File(...),
                       userId: str = Form(...),
                       location:str = Form(...),
                       tags:str = Form(...)):
    
    image_data = await file.read()
    imageid = str(uuid.uuid4())
    postid = str(uuid.uuid4())
    createdat = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    # Store image in S3 bucket
    image_store_util.put(objectData=image_data,objectName=imageid)
    # Store image metadata in SQL DB\
    image_metadata_store_helper.putImageMetadata(imageid=imageid,
                                                 postid=postid,
                                                 userid=userId,
                                                 createat=createdat,
                                                 location=location,
                                                 tags=tags)
    
    image_upload_response:ImageUploadResponse = ImageUploadResponse(userId,postid,imageid,createdat)
    json_response = asdict(image_upload_response)
    return json_response


@image_router.get("/metadata/{imageId}")
def get_image_metadata(imageId):
    image_metadata = image_metadata_store_helper.getImageMetadata(imageid=imageId)
    return image_metadata

@image_router.get('/{imageId}')
def getImage(imageId):
    image_bytes = image_store_util.get(objectName=imageId)
    return Response(content=image_bytes, media_type="image/png")