#modules
from typing import Optional, List

#FASTApi
from fastapi import Depends, FastAPI
from fastapi import status

#models
from models.user import User
from models.tweet import Tweet
app = FastAPI()

#Path Operations

#Users

@app.post(
    path = "/signup",
    response_model = User,
    status_code = status.HTTP_201_CREATED,
    summary = "Sign up a new user",
    tags = ["Users"],

)
def signup():
    pass


@app.post(
    path = "/login",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Log in a new user",
    tags = ["Users"],

)
def login():
    pass


@app.get(
    path = "/users",
    response_model = List[User],
    status_code = status.HTTP_200_OK,
    summary = "Show all users",
    tags = ["Users"],

)
def show_all_users():
    pass


@app.get(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Show selected user",
    tags = ["Users"],

)
def show_user():
    pass


@app.delete(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Delete selected user",
    tags = ["Users"],

)
def delete_user():
    pass


@app.put(
    path = "/users/{user_id}",
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "update selected user",
    tags = ["Users"],

)
def update_user():
    pass


#Tweets

@app.get(
    path = "/",
    response_model = List[Tweet],
    status_code = status.HTTP_200_OK,
    summary = "Show all Tweets",
    tags = ["Tweets"],
)
def home():
    return {"Twitter API": "Working"}


@app.post(
    path = "/post",
    response_model = Tweet,
    status_code = status.HTTP_201_CREATED,
    summary = "Post a Tweet",
    tags = ["Tweets"],
)
def post_tweet():
    pass


@app.get(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Show a Tweet",
    tags = ["Tweets"],
)
def show_tweet():
    pass


@app.delete(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Delete a Tweet",
    tags = ["Tweets"],
)
def delete_tweet():
    pass


@app.put(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Update a Tweet",
    tags = ["Tweets"],
)
def update_tweet():
    pass