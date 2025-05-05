from fastapi import APIRouter
from . import models

pdfRouter = APIRouter(
    prefix="/api/v1/pdf",
    tags=["PDF Chat"]
)

@pdfRouter.post("/")
async def upload_pdf():
    pass