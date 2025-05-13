from fastapi import FastAPI
from src.auth.routes import auth_router

version = 'v1'

app = FastAPI(
    title="AskPDF",
    description="API for PDF assistant",
    version=version
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Authentication"])