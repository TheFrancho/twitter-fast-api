#python libraries
from typing import List
import json
from datetime import datetime

#fastapi packages
from fastapi import APIRouter, status
from fastapi import Body

#models modules
from models.user import User, UserRegister


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post(
    path = "/signup",
    response_model = User,
    status_code = status.HTTP_201_CREATED,
    summary = "Sign up a new user",

)
def signup(
    user : UserRegister = Body(
        ...,
    )
):
    '''
    Sign up

    Register a new user in the app

    Parameters:
        - Request Body Parameters:
            - user: UserRegister

    Returns a json with the basic user information
        - user_id : UUID
        - email : EmailStr,
        - first_name : str,
        - last_name : str,
        - birth_date : Optional[date],
    '''
    with open("db/users.json", "r+", encoding = 'utf-8') as f:
        results = json.load(f)
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        if user_dict["birth_date"] :
            user_dict["birth_date"] = str(user_dict["birth_date"])
        else:
            user_dict["birth_date"] = str(datetime.now())
        results.append(user_dict)
        f.seek(0)
        json.dump(results, f, indent=2, default=str)
        return user


@router.post(
    path = "/login",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Log in a new user",
)
def login():
    pass


@router.get(
    path = "/users",
    status_code = status.HTTP_200_OK,
    summary = "Show all users",
)
def show_all_users():
    '''
    Show all users

    Show all users in the db

    Parameters:
        - 
    
    Returns a json list with all users in the app with the following keys
        - user_id : UUID
        - email : EmailStr,
        - first_name : str,
        - last_name : str,
        - birth_date : Optional[date],
    '''
    with open("db/users.json", "r", encoding = 'utf-8') as f:
        results = json.load(f)
        return results


@router.get(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Show selected user",
)
def show_user():
    pass


@router.delete(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Delete selected user",

)
def delete_user():
    pass


@router.put(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "update selected user",
)
def update_user():
    pass