from abc import ABC, abstractmethod
import logging
import psycopg


logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Datastore(ABC):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    

class ImageMetadataStoreHelper(Datastore):
    def __init__(self,table_name,host="127.0.0.1"):
        super().__init__()
        self.host = host
        self.db = "newsfeed"
        self.username = "testuser"
        self.password = "password"
        self.table_name = table_name
  
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
        connection,cursor = self.connectToDb()
        response = None
        try:
            #query = f"SELECT * FROM {self.table_name};"
            query = f"SELECT * FROM {self.table_name} WHERE imageid = '{imageid}';"
            cursor.execute(query)
            queryResult = list(cursor.fetchone())
            response = {
                'imageId' : queryResult[0],
                'postId' : queryResult[1],
                'userId': queryResult[2],
                'createdAt': queryResult[3],
                'location': queryResult[4],
                'tags': queryResult[5]
            }
        except Exception as e:
            print(f"Failed to get Metadata from SQL : {e}")
        finally:
            self.close_connection(connection,cursor)
            return response
    
    def putImageMetadata(self,imageid,postid,userid,createat,location,tags):
        connection,cursor = self.connectToDb()
        
        try:
            cursor.execute("INSERT INTO image (imageId, postId, userId, createdAt, location, tags) VALUES (%s, %s, %s, %s, %s, %s);",
            (imageid,postid, userid,createat,location,tags))
            # Commit the transaction
            connection.commit()
            self.logger.info(f"Record Created into Table: {self.table_name}")
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
        
    