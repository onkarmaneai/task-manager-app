from sqlalchemy.orm import Session

from app.core.errors import AuthenticationError, ConflictError
from app.core.security import hash_password, verify_password
from app.database.models import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, payload: UserCreate) -> User:
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        raise ConflictError(code="USER_EXISTS", message="Email is already registered.")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise AuthenticationError(code="INVALID_CREDENTIALS", message="Invalid email or password.")
    return user
