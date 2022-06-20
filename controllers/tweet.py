from typing import List

from fastapi import APIRouter, status

from models import Tweet

router = APIRouter(
    prefix="/tweets",
    tags=["Tweets"],
)


@router.get(
    path = "/",
    response_model = List[Tweet],
    status_code = status.HTTP_200_OK,
    summary = "Show all Tweets",
)
def home():
    return {"Twitter API": "Working"}


@router.post(
    path = "/post",
    response_model = Tweet,
    status_code = status.HTTP_201_CREATED,
    summary = "Post a Tweet",
)
def post_tweet():
    pass


@router.get(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Show a Tweet",
)
def show_tweet():
    pass


@router.delete(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Delete a Tweet",
)
def delete_tweet():
    pass


@router.put(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Update a Tweet",
)
def update_tweet():
    pass