#python libraries
import json
from datetime import date
from uuid import UUID, uuid4
#fastapi packages
from fastapi import APIRouter, Path, status, HTTPException
from fastapi import Body
#Other packages
import bcrypt
#models modules
from models.user import User, UserRegister, UserLogin, UserEdit
#views modules
from views.user import UserHandler
from views.tweet import TweetHandler

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
        ...
    )
):
    '''
    **Sign up**

    Register a new user in the app

    Parameters:
    - Request body parameter
        - user: UserRegister

    Returns a json object with the basic user information:
    - user_id : UUID
    - email : EmailStr,
    - first_name : str,
    - last_name : str,
    - birth_date : Optional[date]
    '''
    user_handler = UserHandler()

    results = user_handler.load_data("users")
    logic = user_handler.load_data("tweets_per_person")

    user_dict = user.dict()
    user_dict, results = user_handler.setup_user(results, user_dict)

    logic = user_handler.setup_register(logic, user_dict)

    user_handler.save_data("users", results)
    user_handler.save_data("tweets_per_person", logic)

    return User(**user_dict)


@router.get(
    path = "/users",
    status_code = status.HTTP_200_OK,
    summary = "Show all users",
)
def show_all_users():
    '''
    **Show all users**

    Show all stored users in the DB

    Parameters: No needed
    
    Returns a a list of json objects of all users in the app with the following keys
    - user_id : UUID
    - email : EmailStr,
    - first_name : str,
    - last_name : str,
    - birth_date : Optional[date]
    '''
    user_handler = UserHandler()
    results = user_handler.load_data("users")
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
    **Show single user**

    Show a single user selected by it ID

    Parameters:
    - Path parameters:
        - user_id : UUID
    
    Returns a json object with the user info in the app with the following keys
    - user_id : UUID
    - email : EmailStr,
    - first_name : str,
    - last_name : str,
    - birth_date : Optional[date],
    '''
    user_handler = UserHandler()
    results = user_handler.load_data("users")
    found = user_handler.find_user(str(user_id), results)
    if found:
        return User(**found)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Update a user",
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
    **Update user**

    Updates the user information

    Parameters:
    - Path parameters:
        - user_id : UUID
    - Body Parameters:
        - user : UserEdit
    
    Returns a json object of the user info with the following keys
    - user_id : UUID
    - email : EmailStr,
    - first_name : str,
    - last_name : str,
    - birth_date : date
    '''
    user_handler = UserHandler()
    results = user_handler.load_data("users")

    user_dict = None

    user_dict = user_handler.edit_user_into(str(user_id), results, edit_user)

    if user_dict:
        user_handler.update_data("users", results)
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
    **Delete user**

    Deletes the selected user from the DataBase

    Parameters:
    - Path parameters:
        - user_id : UUID
    
    Returns a json object with the deleted user info with the following keys:
    - user_id : UUID
    - email : EmailStr,
    - first_name : str,
    - last_name : str,
    - birth_date : date
    '''
    user_handler = UserHandler()
    tweet_handler = TweetHandler()

    results = user_handler.load_data("users")
    logic = user_handler.load_data("tweets_per_person")
    delete_tweets = tweet_handler.load_data("tweets")

    with open("db/users.json", "r+", encoding = 'utf-8') as f, open("db/tweets_per_person.json", "r+", encoding = 'utf-8') as logic_f, open("db/tweets.json", "r+", encoding = 'utf-8') as tweets:
        results = json.load(f)
        logic  = json.load(logic_f)
        delete_tweets = json.load(tweets)

        register_to_delete = None

        user_to_delete, results = user_handler.delete_data(str(user_id), results)

        register_to_delete, logic = user_handler.delete_register(str(user_id), logic)

        delete_tweets = tweet_handler.delete_data(str(user_id), delete_tweets)

        if user_to_delete and register_to_delete:
            user_handler.update_data("users", results)

            user_handler.update_data("tweets_per_person", logic)

            tweet_handler.update_data("tweets", delete_tweets)

            return User(**user_to_delete)
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
