#Native modules
from uuid import UUID
from datetime import datetime
from typing import Optional

#Pydantic modules
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

#Other models
from .user import User

class Tweet(BaseModel):
    tweet_id : UUID = Field(...)
    content : str = Field(
        ...,
        min_lenght = 1,
        max_lenght = 256,
    )
    created_at : datetime = Field(default = datetime.now())
    updated_at : Optional[datetime] = Field(default = None)
    by : User = Field(...)