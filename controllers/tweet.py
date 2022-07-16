#python libraries
from typing import List
from uuid import UUID

#models modules
from models.tweet import Tweet, CreateTweet, UpdateTweet

#views modules
from views.tweet import TweetHandler
from views.user import UserHandler

#fastapi packages
from fastapi import APIRouter, status
from fastapi import Body, Path, HTTPException


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
    '''
    **Show all tweets**

    Show all the tweets stored in the db

    Parameters: No required
    
    Returns a list  of json objects of all tweets in the app with the following keys
    - tweet_id : UUID
    - content : str,
    - created_at : datetime,
    - updated_at : datetime,
    - by : User
    '''
    tweet_handler = TweetHandler()
    results = tweet_handler.load_data("tweets")
    return results


@router.post(
    path = "/post",
    response_model = Tweet,
    status_code = status.HTTP_201_CREATED,
    summary = "Post a Tweet",
)
def post_tweet(
    tweet : CreateTweet = Body(
        ...,
    )
):
    '''
    **Post Tweet**

    Post a Tweet in the app

    Parameters:
    - Request Body Parameters:
        - tweet : CreateTweet

    Returns a json object with the basic tweet information
    - tweet_id : UUID
    - content : str,
    - created_at : datetime,
    - updated_at : Optional[datetime],
    - by : UUID
    '''
    tweet_handler = TweetHandler()
    results = tweet_handler.load_data("tweets")
    user_handler = UserHandler()
    logic = user_handler.load_data("tweets_per_person")

    tweet_dict = tweet.dict()
    tweet_dict, results = tweet_handler.setup_tweet(results, tweet_dict)

    found = False
    found, logic = tweet_handler.find_register(tweet_dict, logic)

    if not found:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Tweet author does not exist")

    tweet_handler.save_data("tweets", results)
    user_handler.save_data("tweets_per_person", logic)

    return Tweet(**tweet_dict)


@router.get(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Show selected Tweet",
)
def show_tweet(
    tweet_id: UUID = Path(
        ...
        )
):
    '''
    **Show single tweet**

    Show a single tweet by it id

    Parameters:
    - Path parameters:
        - tweet_id : UUID
    
    Returns a json object of the tweet info in the app with the following keys
    - tweet_id : UUID,
    - content : str,
    - created_at : datetime,
    - updated_at : datetime,
    - by : User
    '''
    tweet_handler = TweetHandler()
    results = tweet_handler.load_data("tweets")
    find = tweet_handler.find_tweet(tweet_id, results)
    if find:
        return find
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tweet not found")


@router.get(
    path = "/person_tweet/{user_id}",
    response_model = List[Tweet],
    status_code = status.HTTP_200_OK,
    summary = "Show all person Tweets",
)
def show_person_tweets(
    user_id: UUID = Path(
        ...
        )
):
    '''
    **Show all person Tweets**

    Show all the Tweets posted by some person in the app

    Parameters:
    - Path parameters:
        - user_id : UUID
    
    Returns a json object list of the tweet info in the app with the following keys
    - tweet_id : UUID
    - content : str,
    - created_at : datetime,
    - updated_at : datetime,
    - by : User
    '''
    tweet_handler = TweetHandler()
    results = tweet_handler.load_data("tweets")

    tweets_found = tweet_handler.find_all_tweets_user(results, user_id)
    if tweets_found:
        return tweets_found
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Person doesn't have any tweet registered")


@router.put(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Update a Tweet",
)
def update_tweet(
    tweet_id : UUID = Path(
        ...,
    ),
    tweet : UpdateTweet = Body(
        ...,
    )
):
    '''
    **Updates a tweet**

    Updates the content of a Tweet

    Parameters:
    - Path Parameters:
        - tweet_id : UUID
    - Body Parameters:
        - tweet : UpdateTweet
    
    Returns a json object of the tweet info updated with the following keys
    - tweet_id : UUID
    - content : str,
    - created_at : datetime,
    - updated_at : datetime,
    - by : UUID
    '''
    tweet_handler = TweetHandler()
    results = tweet_handler.load_data("tweets")

    tweet_dict, results = tweet_handler.edit_tweet_into(tweet_id, results, tweet)

    if tweet_dict:
        tweet_handler.update_data("tweets", results)
        return Tweet(**tweet_dict)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tweet not found")


@router.delete(
    path = "/tweets/{tweet_id}",
    response_model = Tweet,
    status_code = status.HTTP_200_OK,
    summary = "Delete a Tweet",
)
def delete_tweet(
    tweet_id : UUID = Path(
        ...,
    )
):
    '''
    **Delete Tweet**

    Delete the selected Tweet from the DataBase

    Parameters:
    - Path parameters:
        - tweet_id : UUID
    
    Returns a json object of the deleted Tweet info with the following keys
    - tweet_id : UUID
    - content : str,
    - created_at : datetime,
    - updated_at : Optional[datetime],
    - by : User
    '''
    tweet_handler = TweetHandler()
    user_handler = UserHandler()

    results = tweet_handler.load_data("tweets")
    logic = user_handler.load_data("tweets_per_person")
    with open("db/tweets.json", "r+", encoding = 'utf-8') as f, open("db/tweets_per_person.json", "r+", encoding = 'utf-8') as logic_f:

        to_delete = None

        register_to_delete = None

        to_delete, results = tweet_handler.delete_single_tweet(tweet_id, results)

        register_to_delete, logic = tweet_handler.delete_single_register(tweet_id, logic, to_delete)

        if to_delete and register_to_delete:
            tweet_handler.update_data("tweets", results)
            user_handler.update_data("tweets_per_person", logic)
            return to_delete
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tweet not found")
