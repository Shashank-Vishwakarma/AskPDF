from fastapi import APIRouter
from . import models

chatRouter = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"]
)

@chatRouter.post("/")
def create_message():
    pass
