#python libraries
from typing import List
import json
from datetime import datetime, date
from uuid import UUID, uuid4

#fastapi packages
from fastapi import APIRouter, status, HTTPException
from fastapi import Body

#models modules
from models.user import User, UserRegister, UserLogin


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
        user_dict["user_id"] = uuid4()
        if not user_dict["birth_date"] :
            user_dict["birth_date"] = date(1999, 1, 1)
        results.append(user_dict)
        f.seek(0)
        json.dump(results, f, indent=2, default=str)
        return User(**user_dict)


@router.post(
    path = "/login",
    status_code = status.HTTP_200_OK,
    summary = "Log in a new user",
)
def login(
    login : UserLogin = Body(
        ...,
    )
):
    with open("db/users.json", "r+", encoding = 'utf-8') as f:
        results = json.load(f)
        login_dict = login.dict()
        for find in results:
            if find["email"] == login_dict["email"] and find["password"] == login_dict["password"]:
                return {"status" : "log in"}
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User or Password do not match")


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


@router.put(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "update selected user",
)
def update_user():
    pass


@router.delete(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Delete selected user",

)
def delete_user():
    pass
