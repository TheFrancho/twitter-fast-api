#Native modules
from uuid import UUID
from datetime import datetime
from typing import Optional

#Pydantic modules
from pydantic import BaseModel
from pydantic import Field

#Other models
from .user import User

class CreateTweet(BaseModel):
    content : str = Field(
        ...,
        min_lenght = 1,
        max_lenght = 256,
    )
    by : UUID = Field(...)

class UpdateTweet(BaseModel):
    content : str = Field(
        ...,
        min_lenght = 1,
        max_lenght = 256,
    )

class Tweet(CreateTweet):
    created_at : datetime = Field(default = datetime.now())
    updated_at : Optional[datetime] = Field(default = None)
    tweet_id : UUID = Field(...)