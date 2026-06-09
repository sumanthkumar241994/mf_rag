from fastapi import Request, HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import settings

def extract_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing"
        )
    
    scheme, token = auth_header.split()

    if scheme.lower() != 'bearer':
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid jwt scheme"
        )
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No jwt token"
        )
    
    return token


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SALT,
            algorithms=['HS256']
        )
        return payload
    except ExpiredSignatureError:
        raise ValueError("Token has expired")
    except JWTError:
        raise ValueError("Invalid token")