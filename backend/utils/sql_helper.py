from abc import ABC, abstractmethod
import logging
import psycopg
from dataclasses import dataclass, asdict
from typing import List,Union

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
    text:str
    createdat: str
    userId: str

@dataclass
class UserPostData:
    imageId: str
    text: str
    createAt: str
    postId: str

@dataclass
class UserImageData:
    imageId: str
    postId: str

class Datastore(ABC):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

@dataclass
class UserDetails:
    userId:str
    password: str
    email: str
    contact: str

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
    
 
class UserDataHelper:
    def __init__(self,host="127.0.0.1"):
        self.host = host
        self.db = "newsfeed"
        self.username = "testuser"
        self.password = "password"
    
    def close_connection(self,connection, cursor):
        cursor.close()
        connection.close()
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
    
    def getUserPosts(self,userId)->List[UserPostData]:
        table_name = "post"
        connection,cursor = self.connectToDb()
        response = []
        try:
            query = f"select i.imageid,p.text,i.createdat,p.postid from post as p inner join image i on p.postid = i.postid and p.userid='{userId}';"
            cursor.execute(query)
            postIds = list(cursor.fetchall())
            for queryResult in postIds:
                imageId = queryResult[0]
                text = queryResult[1]
                createdAt = queryResult[2]
                postId = queryResult[3]
                
                response.append(UserPostData(imageId,text,createdAt,postId)) 
            
        except Exception as e:
            print(f"Failed to get User Posts from SQL : {e}")
        finally:
            self.close_connection(connection,cursor)
            return response

class UserProfileHelper:
    def __init__(self,host="127.0.0.1"):
        self.host = host
        self.db = "newsfeed"
        self.username = "testuser"
        self.password = "password"
    
    def close_connection(self,connection, cursor):
        cursor.close()
        connection.close()
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
    
    def getUser(self,userId,password)->Union[UserDetails , None]:
        table_name = "users"
        connection,cursor = self.connectToDb()
        response = None
        try:
            query = f"select * from {table_name} where userid = '{userId}' and password = '{password}';"
            cursor.execute(query)
            userDetail = list(cursor.fetchone())
            userId = userDetail[0]
            password = userDetail[1]
            email = userDetail[2]
            contact = userDetail[3]
            response = UserDetails(userId,password,email,contact)
            return response
            
        except Exception as e:
            print(f"Failed to execute login query : {e}")
        finally:
            self.close_connection(connection,cursor)
            return response
    
    def createUser(self,userid,password,email,contact):
        connection,cursor = self.connectToDb()
        table_name = "users"
        try:
            query = f"INSERT INTO {table_name} (userid, password, email, contact) VALUES ('{userid}','{password}','{email}','{contact}');"
            cursor.execute(query)
            # Commit the transaction
            connection.commit()
            self.logger.info(f"Record Created into Table: {table_name}")
        except Exception as e:
            connection.rollback()
            print(f"Error: {e}")
        finally:
            # Close the connection
            self.close_connection(connection, cursor)
    
    