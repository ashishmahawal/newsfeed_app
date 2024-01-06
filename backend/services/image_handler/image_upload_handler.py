from fastapi import UploadFile

class ImageUploadHandler:
    def __init__(self):
        pass
    
    async def generateImageBlob(image_file:UploadFile):
        image_blob = await image_file.read()
        
    
    def generateImageMetadata():
        pass
    
    