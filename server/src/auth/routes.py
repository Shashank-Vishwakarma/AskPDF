from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.auth.schemas import RegisterUser
from src.auth.models import User
from src.db.main import get_db_session

auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(register_body: RegisterUser, session: AsyncSession = Depends(get_db_session)):
    """
    Register a new user

    Args:
        register_body: RegisterUser
        session: AsyncSession
    """

    # Compare password and confirm password
    if register_body.password != register_body.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    # Check if user already exists
    statement = select(User).where(User.email == register_body.email)
    result = await session.exec(statement)

    if result.first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # hash the password
    
    # store the user in the database

    return {"message": "User registered successfully"}