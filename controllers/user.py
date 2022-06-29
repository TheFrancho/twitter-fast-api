#python libraries
from typing import List
import json
from datetime import datetime, date
from uuid import UUID, uuid4

#fastapi packages
from fastapi import APIRouter, Path, status, HTTPException
from fastapi import Body

#models modules
from models.user import User, UserRegister, UserLogin, UserEdit


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
    with open("db/users.json", "r+", encoding = 'utf-8') as f, open("db/tweets_per_person.json", "r+", encoding = 'utf-8') as logic_f:
        results = json.load(f)
        logic  = json.load(logic_f)

        user_dict = user.dict()
        user_dict["user_id"] = uuid4()

        if not user_dict["birth_date"] :
            user_dict["birth_date"] = date(1999, 1, 1)

        results.append(user_dict)
        
        new_register = {str(user_dict["user_id"]) : []}
        logic.append(new_register)

        f.seek(0)
        json.dump(results, f, indent=2, default=str)
        logic_f.seek(0)
        json.dump(logic, logic_f, indent=2, default=str)

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
    '''
    Log in

    Log in the user into the app

    Parameters:
        - Body Parameters:
            - login : UserLogin
    
    Returns the status if the login was successful (to do)
    '''
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
def show_user(
    user_id : UUID = Path(
        ...,
    )
):
    '''
    Show single user

    Show a single user by it id

    Parameters:
        - Path parameters:
            - user_id : UUID
    
    Returns a json list with the user info in the app with the following keys
        - tweet_id : UUID
        - email : EmailStr,
        - first_name : str,
        - last_name : str,
        - birth_date : Optional[date],
    '''
    with open("db/users.json", "r", encoding = 'utf-8') as f:
        results = json.load(f)
        for find in results:
            if find["user_id"] == str(user_id):
                return User(**find)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "update selected user",
)
def update_user(
    user_id : UUID = Path(
        ...,
    ),
    edit_user : UserEdit = Body(
        ...
    )
):
    '''
    Update user

    Updates the user information

    Parameters:
        - Path parameters:
            - user_id : UUID
        - Body Parameters:
            - user : UserEdit
    
    Returns a json list with the user info in the app with the following keys
        - user_id : UUID
        - email : EmailStr,
        - first_name : str,
        - last_name : str,
        - birth_date : date,
    '''
    with open("db/users.json", "r+", encoding = 'utf-8') as f:
        user_dict = None
        results = json.load(f)
        for find in results:
            if find["user_id"] == str(user_id):
                user_dict = edit_user.dict()
                for keys in find.keys():
                    if keys in user_dict.keys():
                        find[keys] = user_dict[keys]
                user_dict = find.copy()
                break
        if user_dict:
            f.truncate(0)
            f.seek(0)
            json.dump(results, f, indent=2, default=str)
            return User(**user_dict)
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")


@router.delete(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Delete selected user",

)
def delete_user(
    user_id : UUID = Path(
        ...,
    )
):
    '''
    Delete user

    Delete the selected user

    Parameters:
        - Path parameters:
            - user_id : UUID
    
    Returns a json object with the deleted user info with the following keys:
        - user_id : UUID
        - email : EmailStr,
        - first_name : str,
        - last_name : str,
        - birth_date : date, 
    '''
    with open("db/users.json", "r+", encoding = 'utf-8') as f, open("db/tweets_per_person.json", "r+", encoding = 'utf-8') as logic_f, open("db/tweets.json", "r+", encoding = 'utf-8') as tweets:
        results = json.load(f)
        logic  = json.load(logic_f)
        delete_tweets = json.load(tweets)

        index_to_delete = None
        register_to_delete = None
        tweets_to_delete = []

        for en, find in enumerate(results):
            if find["user_id"] == str(user_id):
                index_to_delete = en
                to_delete = results.pop(index_to_delete)
                break

        for en, find in enumerate(logic):
            for search in find.keys():
                if search == str(user_id):
                    register_to_delete = logic.pop(en)
                    break

        for en, find in enumerate(delete_tweets):
            if find["by"] == str(user_id):
                tweets_to_delete.append(en)
        
        for deleting in reversed(tweets_to_delete):
            delete_tweets.pop(deleting)

        if to_delete and register_to_delete:
            f.truncate(0)
            f.seek(0)
            json.dump(results, f, indent=2, default=str)

            logic_f.truncate(0)
            logic_f.seek(0)
            json.dump(logic, logic_f, indent=2, default=str)

            tweets.truncate(0)
            tweets.seek(0)
            json.dump(delete_tweets, tweets, indent=2, default=str)

            return User(**to_delete)
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

