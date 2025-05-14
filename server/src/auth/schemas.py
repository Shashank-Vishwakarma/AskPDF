from pydantic import BaseModel
from typing import Optional

class RegisterUser(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str
    plan: Optional[str] = "free"

class LoginUser(BaseModel):
    email: str
    password: str