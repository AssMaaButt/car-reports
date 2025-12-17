from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional

SECRET_KEY = "your-secret-key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  


def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    """
    Generate a JWT token.
    data: dictionary to encode (e.g., {"sub": user_id})
    expires_minutes: override default expiration
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode a JWT token. Returns payload if valid, None if invalid/expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
