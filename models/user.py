#python libraries
from uuid import UUID
from datetime import date
from typing import Optional

#Pydantic modules
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class PasswordMixin(BaseModel):
    password : str = Field(
        ...,
        min_lenght = 8,
        max_lenght = 256,
        example = "password",
    )


class UserBase(BaseModel):
    email : EmailStr = Field(
        ...,
    )


class User(UserBase):
    _user_id : Optional[UUID] = Field(
        default = None,
    )
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
        default=date(1999,1,1)
    )


class UserRegister(User, PasswordMixin):
    pass


class UserLogin(UserBase, PasswordMixin):
    pass


class UserEdit(BaseModel):
    first_name : Optional[str] = Field(
        default = None,
        min_length=1,
        max_length=50,
    )
    last_name : Optional[str] = Field(
        default = None,
        min_length=1,
        max_length=50,
    )
    birth_date : Optional[date] = Field(
        default=None
    )