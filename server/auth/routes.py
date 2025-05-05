from fastapi import APIRouter
from . import models

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

@auth_router.post("/login")
def login():
    pass

@auth_router.post("/register")
def signup(user: models.User):
    pass

@auth_router.post("/logout")
def logout():
    pass