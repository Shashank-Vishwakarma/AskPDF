from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

from src.config import Config

password_context = CryptContext(
    schemes=["bcrypt"]
)

def generate_password_hash(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_context.verify(password, hashed_password)

def generate_token(user_data: dict):
    payload = {
        'user': user_data,
        'exp': datetime.now() + timedelta(days=1)
    }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY, 
        algorithm="HS256"
    )

    return token

def verify_token(token: str):
    try:
        decoded_payload = jwt.decode(token, key=Config.JWT_SECRET_KEY, algorithms=["HS256"])
        if decoded_payload["exp"] < datetime.now():
            return None

        return decoded_payload
    except jwt.PyJWTError as jwte:
        print(f"PyJWTError: Error: {jwte}")
        return None
    except Exception as e:
        print("JWT Decode: Error: ", e)
        return None