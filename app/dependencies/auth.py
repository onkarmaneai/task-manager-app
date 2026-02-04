from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.errors import AuthenticationError
from app.core.security import decode_access_token
from app.database.session import get_db
from app.services import users as user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    subject = decode_access_token(token)
    try:
        user_id = int(subject)
    except ValueError as exc:
        raise AuthenticationError(code="INVALID_TOKEN", message="Invalid authentication token.") from exc

    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise AuthenticationError(code="USER_NOT_FOUND", message="User not found.")
    return user
