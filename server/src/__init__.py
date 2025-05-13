from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.auth.routes import auth_router
from src.db.main import initdb

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initdb()
    yield
    print("Server is stopping...")

version = 'v1'

app = FastAPI(
    title="AskPDF",
    description="API for PDF assistant",
    version=version,
    lifespan=lifespan
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Authentication"])