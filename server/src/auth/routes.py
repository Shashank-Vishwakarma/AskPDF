from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.schemas import RegisterUser, LoginUser
from src.models import User
from src.db.main import get_db_session
from src.utils import generate_password_hash, verify_password, generate_token
from src.middlewares import token_bearer
from src.auth.service import check_user_exist

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
    user = await check_user_exist(session, register_body.email)
    if user is not None:
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

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    login_user_body: LoginUser,
    session: AsyncSession = Depends(get_db_session),
):
    """
    Login a user

    Args:
        login_user_body: LoginUser
        session: AsyncSession
    """

    user = await check_user_exist(session, login_user_body.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist") 
    
    # verify the password
    if not verify_password(login_user_body.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")   

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
        status_code=status.HTTP_200_OK
    )

@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(
    token_details = Depends(token_bearer)
):
    return JSONResponse(
        content={
            "message": "Logout successful"
        }, 
        status_code=status.HTTP_200_OK
    )