#Native modules
from uuid import UUID
from datetime import date
from typing import Optional


#Pydantic modules
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserBase(BaseModel):
    user_id : UUID = Field(
        ...,

    )
    email : EmailStr = Field(
        ...,
    )


class UserLogin(UserBase):
    password : str = Field(
        ...,
        min_lenght = 8,
        max_lenght = 16,
    )


class User(UserBase):
    first_name : str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    last_name : str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    birth_date : Optional[date] = Field(
        default = None,
    )