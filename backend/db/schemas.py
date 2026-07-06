from pydantic import BaseModel
from pydantic import EmailStr


class UserRegister(BaseModel):

    username: str

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    class Config:

        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str