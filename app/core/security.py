from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.errors import AuthenticationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError as exc:
        raise AuthenticationError(code="TOKEN_EXPIRED", message="Token has expired.") from exc
    except jwt.InvalidTokenError as exc:
        raise AuthenticationError(code="INVALID_TOKEN", message="Invalid authentication token.") from exc

    subject = payload.get("sub")
    if not subject:
        raise AuthenticationError(code="INVALID_TOKEN", message="Invalid authentication token.")
    return subject
