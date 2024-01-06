from abc import ABC, abstractmethod
import logging
import psycopg
from dataclasses import dataclass, asdict


logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class ImageMetadata:
    imageId: str
    postId: str
    userId: str
    createdAt: str
    location: str
    tags: str
    
@dataclass
class PostData:
    postId: str
    userId: str
    text:str
    createdat: str
    
class Datastore(ABC):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    

class ImageMetadataStoreHelper(Datastore):
    def __init__(self,host="127.0.0.1"):
        super().__init__()
        self.host = host
        self.db = "newsfeed"
        self.username = "testuser"
        self.password = "password"
  
    def connectToDb(self):
        connection = psycopg.connect(
            host=self.host,
            user=self.username,
            dbname=self.db,
            password=self.password
        )
        # Create a cursor object to interact with the database
        cursor = connection.cursor()

        return connection, cursor

    def close_connection(self,connection, cursor):
        cursor.close()
        connection.close()
    
    def getImageMetadata(self,imageid):
        table_name = "image"
        connection,cursor = self.connectToDb()
        response = None
        try:
            #query = f"SELECT * FROM {self.table_name};"
            query = f"SELECT * FROM {table_name} WHERE imageid = '{imageid}';"
            cursor.execute(query)
            queryResult = list(cursor.fetchone())
            response = asdict(ImageMetadata(queryResult[0],queryResult[1],queryResult[2],queryResult[3],queryResult[4],queryResult[5]))
            
        except Exception as e:
            print(f"Failed to get Metadata from SQL : {e}")
        finally:
            self.close_connection(connection,cursor)
            return response
    
    def putImageMetadata(self,imageid,postid,userid,createat,location,tags):
        connection,cursor = self.connectToDb()
        table_name = "image"
        try:
            cursor.execute("INSERT INTO image (imageId, postId, userId, createdAt, location, tags) VALUES (%s, %s, %s, %s, %s, %s);",
            (imageid,postid, userid,createat,location,tags))
            # Commit the transaction
            connection.commit()
            self.logger.info(f"Record Created into Table: {table_name}")
        except Exception as e:
            connection.rollback()
            print(f"Error: {e}")
        finally:
            # Close the connection
            self.close_connection(connection, cursor)

    def getPostData(self,postId):
        table_name = "post"
        connection,cursor = self.connectToDb()
        response = None
        try:
            query = f"SELECT * FROM {table_name} WHERE postid = '{postId}';"
            cursor.execute(query)
            queryResult = list(cursor.fetchone())
            response = asdict(PostData(queryResult[0],queryResult[1],queryResult[2],queryResult[3]))
            
        except Exception as e:
            print(f"Failed to get Metadata from SQL : {e}")
        finally:
            self.close_connection(connection,cursor)
            return response
    def putPostData(self,postid, userid,text, createat):
        connection,cursor = self.connectToDb()
        table_name = "post"
        try:
            cursor.execute("INSERT INTO post (postid, userid, text, createdat) VALUES (%s, %s, %s, %s);",
            (postid, userid,text, createat))
            # Commit the transaction
            connection.commit()
            self.logger.info(f"Record Created into Table: {table_name}")
        except Exception as e:
            connection.rollback()
            print(f"Error: {e}")
        finally:
            # Close the connection
            self.close_connection(connection, cursor)
    
# t = SqlDB(table_name="image")
# #t.putImageMetadata('ABC12345', '1', '101', '2024-01-01 12:00:00', 'Some Location', 'Tag1, Tag2')
# res = t.getImageMetadata('ABC12345')
# print(res)
        
    