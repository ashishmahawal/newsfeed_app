from utils.sql_helper import UserProfileHelper
import logging
from dataclasses import asdict
logging.basicConfig()


logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class UserHelper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_profile_helper = UserProfileHelper()
    
    def createUserAccount(self,userid,password,email,contact)->bool:
        try:
            self.user_profile_helper.createUser(userid,password,email,contact)
            return True
        except Exception as e:
            self.logger.error(f"Error Creating Account: {e}")
            return False
    
    def verifyLogin(self,userid,password)->bool:
        try:
            res = self.user_profile_helper.getUser(userid,password)
            self.logger.info(f"Logged in user details: {asdict(res)}")
            if res:
                return True
            else:
                return False
        except Exception as e:
            return False