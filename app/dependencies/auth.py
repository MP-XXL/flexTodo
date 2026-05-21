from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import CredentialsException, TokenExpiredException
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    FastAPI dependency: validates JWT Bearer token and returns the authenticated User.

    Raises 401 on invalid/missing token.
    Raises 401 on expired token.
    """
    token = credentials.credentials

    try:
        user_id_str = decode_access_token(token)
    except ExpiredSignatureError:
        raise TokenExpiredException()
    except JWTError:
        raise CredentialsException()

    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise CredentialsException()

    user = db.get(User, user_id)
    if user is None:
        raise CredentialsException("User no longer exists.")

    return user
