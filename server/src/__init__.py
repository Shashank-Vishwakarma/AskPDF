from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routes import auth_router
from src.docs_ingestion.routes import documents_router
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Authentication"])
app.include_router(documents_router, prefix=f"/api/{version}/documents", tags=["Documents"])