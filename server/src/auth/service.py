from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.auth.models import User

async def check_user_exist(session: AsyncSession, email: str) -> bool:
    statement = select(User).where(User.email == email)
    result = await session.exec(statement)
    return result.first()