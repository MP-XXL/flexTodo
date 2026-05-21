from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, ConflictException, CredentialsException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserLoginRequest, UserRegisterRequest


def register_user(payload: UserRegisterRequest, db: Session) -> User:
    """
    Register a new user.

    - Enforces unique email constraint.
    - Hashes the password before persisting.
    """
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise ConflictException("An account with this email already exists.")

    user = User(
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        email=payload.email.lower().strip(),
        password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(payload: UserLoginRequest, db: Session) -> str:
    """
    Authenticate a user with email + password.

    Returns a signed JWT access token on success.
    Raises 401 on invalid credentials (deliberately vague to prevent enumeration).
    """
    user = db.query(User).filter(User.email == payload.email.lower().strip()).first()

    if not user or not verify_password(payload.password, user.password):
        raise CredentialsException("Invalid email or password.")

    return create_access_token(subject=str(user.id))
