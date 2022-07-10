from typing import List
import json

#fastapi packages
from fastapi import APIRouter, Path, status, HTTPException
from fastapi import Body
from models.user import UserLogin
from views.auth import AuthHandler
from views.user import UserHandler

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post(
    path = "/login",
    status_code = status.HTTP_200_OK,
    summary = "Log in a user",
)
def login(
    login : UserLogin = Body(
        ...,
    )
):
    '''
    **Log in**

    Login the user into the app

    Parameters:
    - Body Parameters:
        - login : UserLogin
    
    Returns the status if the login was successful (to do)
    '''
    auth_handler = AuthHandler()
    user_handler = UserHandler()

    results = user_handler.load_data("users")
    login_dict = login.dict()
    
    found = auth_handler.check_credentials(results, login_dict)
    if found:
        return {'Status': 'Log in'}
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User or Password do not match")
