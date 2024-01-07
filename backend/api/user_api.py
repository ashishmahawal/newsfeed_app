from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from utils.sql_helper import UserDataHelper
from utils.user_helper import UserHelper

user_router = APIRouter(prefix="/v1/user")

user_data_helper = UserDataHelper()
user_helper = UserHelper()

class UserLogin(BaseModel):
    userId: str
    password: str

class UserProfile(BaseModel):
    userId: str
    password: str
    email: str
    contact: str
    

@user_router.get("/{userId}")
def getUserPostsData(userId):
    posts = user_data_helper.getUserPosts(userId)
    return {"posts": posts}

@user_router.post("/login")
def userLogin(loginDetail:UserLogin,response:Response):
    isValid = False
    isValid = user_helper.verifyLogin(loginDetail.userId,loginDetail.password)
    if isValid:
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "logged in...."}
    else:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"message": "Incorrect username or password"}

@user_router.post("/create")
def userLogin(userDetail:UserProfile):
    created = False
    created = user_helper.createUserAccount(userDetail.userId,userDetail.password,userDetail.email,userDetail.contact)
    
    if created:
        return {"message":f"UserId : {userDetail.userId} created successfully !!"}
    else:
        return {"error":f"UserId : {userDetail.userId} not created successfully !!"}
    