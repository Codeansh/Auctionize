from pydantic import BaseModel


class LoginData(BaseModel):
    email: str
    password: str


class UserModel(BaseModel):
    username: str
    email: str
    password: str


