from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine

from src.config import Config
from src.auth.models import User

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)

async def initdb():
    async with engine.begin() as conn:
        await conn.run_sync(
            SQLModel.metadata.create_all
        )