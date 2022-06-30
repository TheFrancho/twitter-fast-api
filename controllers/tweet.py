#python libraries
from typing import List
import json
from datetime import datetime
from uuid import UUID, uuid4

#fastapi packages
from fastapi import APIRouter, status
from fastapi import Body, Path, HTTPException

#models modules
from models.tweet import Tweet, CreateTweet, UpdateTweet

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
    with open("db/tweets.json", "r", encoding = 'utf-8') as f:
        results = json.load(f)
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
    with open("db/tweets.json", "r+", encoding = 'utf-8') as f, open("db/tweets_per_person.json", "r+", encoding = 'utf-8') as logic_f:
        results = json.load(f)
        logic  = json.load(logic_f)

        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = uuid4()
        tweet_dict["created_at"] = datetime.now()
        tweet_dict["updated_at"] = tweet_dict["created_at"]

        results.append(tweet_dict)

        found = False

        for find in logic:
            if str(tweet_dict["by"]) == list(find.keys())[0]:
                found = True
                find[str(tweet_dict["by"])].append(tweet_dict["tweet_id"])
                break

        if not found:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Tweet author does not exist")

        f.seek(0)
        json.dump(results, f, indent=2, default=str)
        logic_f.seek(0)
        json.dump(logic, logic_f, indent=2, default=str)

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
    with open("db/tweets.json", "r", encoding = 'utf-8') as f:
        results = json.load(f)
        for find in results:
            if find["tweet_id"] == str(tweet_id):
                return find
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
    with open("db/tweets.json", "r", encoding = 'utf-8') as f, open("db/tweets_per_person.json", "r", encoding = 'utf-8') as logic_f:
        results = json.load(f)
        tweets_found = []
        for find in results:
            if find["by"] == str(user_id):
                tweets_found.append(find)
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
    with open("db/tweets.json", "r+", encoding = 'utf-8') as f:
        tweet_dict = None
        results = json.load(f)
        for find in results:
            if find["tweet_id"] == str(tweet_id):
                tweet_dict = tweet.dict()
                for keys in find.keys():
                    if keys in tweet_dict.keys():
                        find[keys] = tweet_dict[keys]
                tweet_dict["updated_at"] = datetime.now()
                tweet_dict = find.copy()
                break
        if tweet_dict:
            f.truncate(0)
            f.seek(0)
            json.dump(results, f, indent=2, default=str)
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
    with open("db/tweets.json", "r+", encoding = 'utf-8') as f, open("db/tweets_per_person.json", "r+", encoding = 'utf-8') as logic_f:
        results = json.load(f)
        logic  = json.load(logic_f)

        index_to_delete = None

        register_to_delete = None

        for en, find in enumerate(results):
            if find["tweet_id"] == str(tweet_id):
                index_to_delete = en
                to_delete = results.pop(index_to_delete)
                break

        for en, find in enumerate(logic):
            for search in find.values():
                try:
                    register_to_delete = search.index(str(tweet_id))
                    logic[en][to_delete["by"]].pop(register_to_delete)
                except:
                    continue

        if index_to_delete and register_to_delete:
            f.truncate(0)
            f.seek(0)
            json.dump(results, f, indent=2, default=str)

            logic_f.truncate(0)
            logic_f.seek(0)
            json.dump(logic, logic_f, indent=2, default=str)

            return to_delete
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tweet not found")
