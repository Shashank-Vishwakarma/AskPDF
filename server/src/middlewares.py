from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status
from src.utils import verify_token

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        if not creds:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token not found")

        token = creds.credentials
        decoded_payload = verify_token(token)
        if not decoded_payload:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

        return decoded_payload

token_bearer = TokenBearer()