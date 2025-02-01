from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None #significa que este campo es opcional
    username: str
    email: str


class UserDB(User):
    password: str