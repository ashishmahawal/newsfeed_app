from minio import Minio
import logging
from io import BytesIO

FORMAT = '%(asctime)s %(message)s'

logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT
                    )

class ImageDataStoreUtils:
    def __init__(self,env):
        self.logger = logging.getLogger(__name__)
        if env == "local":
            # use minio http://127.0.0.1:9000 minioadmin:minioadmin
            self.client = Minio(
                endpoint="127.0.0.1:9001",
                access_key="minioadmin",
                secret_key="minioadmin",
                secure=False
                
            )
            self.bucket_name  = "images"
            found = self.client.bucket_exists(self.bucket_name)
            if not found:
                self.client.make_bucket(self.bucket_name)
                print("Created bucket", self.bucket_name)
            else:
                print("Bucket", self.bucket_name, "already exists")
        else:
            pass
    
    def get(self,objectName):
        bucket_object = self.client.get_object(bucket_name=self.bucket_name,
                                                object_name=objectName)
        return bucket_object.data
    
    def delete(self):
        pass
    
    def put(self,objectData,objectName):
        self.logger.info(f"Checking type ---- {type(objectData)}")
        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=objectName,
                data=BytesIO(objectData),
                length=-1,
                part_size=5*1024*1024
            )
            self.logger.info(f"Image uploaded to bucket :{self.bucket_name} successfully")
        except Exception as e:
            raise Exception(f"Error uploading to bucket : {self.bucket_name}, error: {e}")
    

# t = ImageDataStoreUtils("local")
# t.put(io.BytesIO(b"hello"),"testDoc")
# bucketObjects  = t.get("_e9df59a1-6072-4f93-a946-9b50f915519d.jpeg")
# print(bucketObjects)
