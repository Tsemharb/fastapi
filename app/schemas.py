from pydantic import BaseModel, EmailStr
from pydantic.typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
