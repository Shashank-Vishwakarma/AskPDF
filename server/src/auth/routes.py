from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.auth.schemas import RegisterUser
from src.auth.models import User
from src.db.main import get_db_session
from src.utils import generate_password_hash, verify_password, generate_token
from src.middlewares import token_bearer

auth_router = APIRouter()

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    register_body: RegisterUser, 
    session: AsyncSession = Depends(get_db_session),
):
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
    hashed_password = generate_password_hash(register_body.password)
    
    # store the user in the database
    user = User(
        name=register_body.name,
        email=register_body.email,
        password=hashed_password,
        plan=register_body.plan
    )
    
    session.add(user)
    await session.commit()
    
    # Create jwt token and send it to the user
    user_data = {
        "name": user.name,
        "email": user.email,
        "plan": user.plan
    }
    token = generate_token(user_data)

    return JSONResponse(
        content={
            **user_data,
            "token": token,
        },
        status_code=status.HTTP_201_CREATED
    )