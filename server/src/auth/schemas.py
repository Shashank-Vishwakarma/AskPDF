from pydantic import BaseModel

class RegisterUser(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str