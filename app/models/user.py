from pydantic import BaseModel, EmailStr

class UserBody(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_name: str
    password: str

class UserUpdateBody(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    user_name: str | None = None
    email: str | None = None
    password: str | None = None
